# Decathlon International Championship Placing Prediction

This is a project which aims to forecast international championship placing
in the track and field decathlon using competition-day event performances.
It is part of the thesis work "Mathematical Characterization
of Elite Performance and Optimal Training in the Track & Field Decathlon"
by Perry Battles.

## Replication

To repeat the analysis performed in the thesis, it is recommended to use the following
software:

+ Python 3.14.5
    - beautifulsoup4     4.14.3
    - bs4                0.0.2
    - certifi            2026.5.20
    - charset-normalizer 3.4.7
    - contourpy          1.3.3
    - cycler             0.12.1
    - fonttools          4.63.0
    - idna               3.18
    - kiwisolver         1.5.0
    - matplotlib         3.10.9
    - numpy              2.4.6
    - packaging          26.2
    - pandas             3.0.3
    - pillow             12.2.0
    - pip                26.1.1
    - pyparsing          3.3.2
    - python-dateutil    2.9.0.post0
    - requests           2.34.2
    - six                1.17.0
    - soupsieve          2.8.4
    - tqdm               4.67.3
    - typing_extensions  4.15.0
    - urllib3            2.7.0
+ R version 4.5.0
    - ggplot2 4.0.0
    - fitdistrplus 1.2-4
    - DescTools 0.99.60
    - car 3.1-3
    - randomForest 4.7-1.2
    - boot

To attempt to replicate the analysis conducted in the thesis work,
perform the following steps:

1. First, feel free to remove the contents of the `output/` folder.
2. Run `python scrape_data.py` to scrape the competition data from the web.
3. Run `python postprocess_data.py` to postprocess the scraped competition data.
4. Run `Rscript fit_model.r` to get modeling output.
    - This will take a while to run.
5. Run `python CI_matrix_graph_maker.py` to generate the plotting output.

Exact replication of the results is not guaranteed.

## File Inventory

+ `CI_matrix_graph_maker.py` is a Python script which visualizes the confidence
intervals of the bootstrapped coefficient differences.
+ `data/` contains all the information used in the analysis.
    - `data_mark.csv` holds the competition marks obtained by scraping the
    web pages for all the competitions.
    - `data_mark_postprocessed.csv` contains the post-processed competition mark
    data. See the dissertation work mentioned above for information concerning
    the postprocessing, or consult
    `postprocess_data.py` for details.
    - `event_data.csv` contains the information for competitions that fall under the
    scope of the study.
+ `fit_model.r` performs the data analysis in R.
+ `output/` contains plotting outputs.
+ `postprocess_data.py` is a Python script which processes the raw competition
mark data scraped from the internet.
+ `README.md` is this document.
+ `scrape_data.py` is a Python script which retrieves the data from the source.
+ `scrape_params.json` contains parameters for the web scraping process.

