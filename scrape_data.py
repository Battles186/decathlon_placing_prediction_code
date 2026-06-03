"""
Scrapes data for the project.
"""

from bs4 import BeautifulSoup
import certifi
import ssl
import urllib3
import urllib.request
import requests
import pandas as pd
import argparse
import re
import json
from pprint import pprint
from copy import deepcopy
from tqdm import tqdm


def read_request_from_file(file_path):
    """
    Reads a request from a file.
    """
    data_out = {}
    with open(file_path) as f:
        lines = f.readlines()

    # First line is the request.
    request_body = lines[0]

    # Following lines are the variables, given as key-value pairs.
    var_kv = [line.split(': ') for line in lines[1:]]
    variables = {
        key: value
        for key, value in var_kv
    }

    return request_body, variables


def read_page_table(
    url=None,
    context=None,
    data_value_idx=None,
    columns=None,
    event_id=None,
    event_name=None,
    **kwargs
    ):
    """
    Extracts all information from the table on one page.

    url: the URL from which data will be retrieved.

    context: the context for the request to retrieve the data from the specified
    URL.

    data_value_idx: in table cell values that have <div> or <br>, those will
    be split into separate values using those tags. Then, the item with the
    index corresponding to this value will be retrieved.

    columns: if provided, these will override the columns indicated by the
    table header that is found in the page.

    event_id: World Athletics event ID.
    """
    contents = urllib.request.urlopen(url, context=ssl._create_unverified_context())

    soup = BeautifulSoup(contents, 'html.parser')

    tables = soup.find_all("table")
    # print(f"Found {len(tables)} table(s)")
    table = tables[0]

    def process_table_val(td):
        divs = td.find_all('div')
        brs = td.find_all('br')
        # print(f"Found {len(divs)} divs")
        if len(divs) < 2:
            text = td.get_text()
            if len(brs) > 0:
                text = text.split('\n')[data_value_idx]
                if ' (' in text:
                    text = text.split(' (')[0]
        else:
            text = divs[data_value_idx].get_text().split(' (')[0]
        return text.replace("\n", "").strip(" ")

    if table is None:
        return None

    thead = table.find_all('thead')[0]
    # print(thead)
    trows = thead.find_all('tr')
    # print(f"Found {len(trows)} table header row(s)")

    if columns is None:
        columns_out = [
            td.get_text().replace('\n', '').strip(' ').lower()
            for td in trows[0].find_all('th')
        ]
    else:
        columns_out = columns

    # Get table body.
    data = [
        [
            process_table_val(td)
            for td in tr.find_all("td")
        ]
        for tr in table.find_all("tr")
    ]

    # Remove dashes and other values.
    data = [
        [
            val
            for val in row
            if val not in ['-']
        ]
        for row in data
    ]

    print("Sample data row:")
    print(f'{len(data[1])} values')
    pprint(data[1])

    # Compile DataFrame.
    df = pd.DataFrame(data, columns=columns_out)
    df.drop(index=[0], inplace=True)
    df['event_id'] = event_id
    df['event_name'] = event_name
    pprint(df.columns)

    return df


def read_pages(scrape_params, func_postprocess_raw=None):
    """
    Reads the table contents of multiple pages and joins the DataFrames together by stacking vertically.
    """
    context = ssl.create_default_context(cafile=certifi.where())
    dfs = [
        read_page_table(
            context=context,
            event_name=event_name,
            **params,
        )
        for event_name, params in tqdm(scrape_params.items())
    ]
    df_all = pd.concat(dfs, axis=0)
    # Drop rows that indicate individual event performances for the multi-events.
    # df_all.drop(index=(df_all[df_all.Rank == '\xa0']).index, inplace=True)

    print("Sample data:")
    print(df_all.head())

    return df_all


with open('scrape_params.json') as f:
    scrape_params = json.load(f)

if __name__ == '__main__':
    urllib3.disable_warnings()

    print("Reading URL:")
    pprint(scrape_params)

    df_marks = read_pages(
        scrape_params
    )

    print(f"Scraped {df_marks.shape[0]} performances.")

    # print("\nObtaining medals...")
    # 
    # # Now that we have that, scrape all athlete profiles for medals.
    # df_athlete_honors = pd.concat([
    #     collect_athlete_honors(athlete_id=athlete_id)
    #     for athlete_id in tqdm(df_marks.athlete_id.unique())
    # ])

    # pprint(athlete_honors)

    # df_marks['Mark_raw'] = df_marks['Mark']

    # def time_to_s(x):
    #     parts = x.split(':')
    #     n = len(parts)
    #     # print(parts)
    #     seconds = [
    #         float(part.strip('h'))*(60**(n - idx - 1))
    #         for idx, part in enumerate(parts)
    #     ]
    #     out = sum(seconds)
    #     # print(x)
    #     # print(n)
    #     # print(seconds)
    #     # print(out)
    #     return out

    # # If the times for the marks are given in a format that has hours,
    # # minutes, and seconds separated, convert to seconds only.
    # # If more than 90% of the marks have a colon in them, convert.
    # if df_marks['Mark'].str.contains(':').mean() > 0.9:
    #     df_marks['Mark'] = df_marks['Mark'].apply(func=time_to_s)

    # # Ensure that the athlete's nationality is labeled.
    # if "Nat" not in df_marks.columns:
    #     cols_new = 
    #     pprint(df_marks.columns)

    df_marks.to_csv('data/data_mark.csv', index=None)
    # df_athlete_honors.to_csv(args.out.strip(".csv") + "_profiles.csv", index=None)


