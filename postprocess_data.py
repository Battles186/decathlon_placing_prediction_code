"""
Postprocesses data from web scraping to prepare for analysis.
"""

import numpy as np
import pandas as pd
from pprint import pprint


def get_seconds(x: str):
    """
    Takes a time formatted in mm:ss and returns the total
    seconds.
    """
    return float(x.split(':')[0])*60 + float(x.split(':')[1])


# Load data.
df_mark = pd.read_csv('data/data_mark.csv')

# Drop any rows in which an athlete did not have a placing.
print(df_mark.pos.unique())
drop_idx = df_mark[df_mark['pos'].isna()].index
print(drop_idx)
df_mark.drop(index=drop_idx, inplace=True)

# Drop any rows for which an athlete did not have a mark for
# a certain discipline.
# _ = [
#     print(col, df_mark[col].unique())
#     for col in df_mark.columns
# ]

NA_vals = ['DNF', 'DQ', 'NM']
_ = [
    df_mark.replace(to_replace=NA_val, value=pd.NA, inplace=True)
    for NA_val in NA_vals
]
df_mark.dropna(inplace=True)

# Convert times to speeds.
df_mark['1500_sec'] = df_mark['1500'].apply(get_seconds)

for event in ['100', 'lj', 'sp', 'hj', '400', '110h', 'dt', 'pv', 'jt', '1500_sec']:
    df_mark[event] = df_mark[event].astype(np.float64)

df_mark['100_speed'] = 100.0 / df_mark['100']
df_mark['110h_speed'] = 110.0 / df_mark['110h']
df_mark['400_speed'] = 400.0 / df_mark['400']
df_mark['1500_speed'] = 1500.0 / df_mark['1500_sec']

print(df_mark)
pprint(df_mark.columns)

# Write postprocessed data to disk.
df_mark.to_csv('data/data_mark_postprocessed.csv')

