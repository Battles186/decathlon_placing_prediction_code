# Decathlon International Championship Placing Prediction

This is a project which aims to forecast international competition placing
in the track and field decathlon based on event performances during said
competition. It is part of the thesis work "Mathematical Characterization
of Elite Performance and Optimal Training in the Track & Field Decathlon"
by Perry Battles.

## Replication

This can be replicated in principle using any recent versions of R or
Python. However, for best results, the following are recommended:

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
    - ggplot2
    - fitdistrplus
    - DescTools
    - car
    - randomForest
    - boot

To replicate the analysis herein, perform the following steps:

1. First, feel free to remove the contents of the `output/` folder.
2. Run `scrape_data.py` to scrape the competition data from the web.
3. Run `postprocess_data.py` to postprocess the data.
4. Run `fit_model.r` to get modeling output.
    - This will take a while to run.
5. Run `CI_matrix_graph_maker.py` to generate the plotting output.

Exact replication of the results is not guaranteed.

## File Inventory

+ `CI_matrix_graph_maker.py` is a Python script which visualizes the confidence
intervals of the coefficient differences.
+ `data/` contains all the data
    - `data_mark.csv` are the competition marks obtained by scraping the
    web pages for each of the competitions.
    - `data_mark_postprocessed.csv` is the post-processed competition mark
    data. See manuscript for information concerning the postprocessing, or
    `postprocess_data.py` for details.
    - `event_data.csv` contains the information for the events for which
    data was obtained.
+ `fit_model.r` fits the model to the data.
+ `output/` contains plotting outputs.
+ `postprocess_data.py` is a Python script which processes the raw competition
mark data scraped from the internet.
+ `README.md` is this readme.
+ `scrape_data.py` is a Python script which retrieves the data from the source.
+ `scrape_params.json` contains parameters for the web scraping process.

