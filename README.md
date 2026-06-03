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
    - cloudpickle        3.1.2
    - contourpy          1.3.3
    - cycler             0.12.1
    - filelock           3.20.0
    - fonttools          4.61.1
    - fsspec             2025.12.0
    - importlib_metadata 8.7.1
    - Jinja2             3.1.6
    - kiwisolver         1.4.9
    - MarkupSafe         2.1.5
    - matplotlib         3.10.8
    - mpmath             1.3.0
    - networkx           3.6.1
    - numpy              2.3.5
    - packaging          26.0
    - pandas             3.0.1
    - pillow             12.0.0
    - pip                25.3
    - pyparsing          3.3.2
    - python-dateutil    2.9.0.post0
    - pyvers             0.2.2
    - setuptools         70.2.0
    - six                1.17.0
    - sympy              1.14.0
    - tensordict         0.11.0
    - tqdm               4.67.3
    - typing_extensions  4.15.0
    - zipp               3.23.0
+ R version 4.6.0 (2026-04-24) -- "Because it was There"

To replicate the analysis herein, perform the following steps:

1. First, feel free to remove any plotting output, although the
folder structure should be left intact.
2. Run `scrape_data.py` to scrape the competition data from the web.
3. Run `postprocess_data.py` to postprocess the data.
4. Run `fit_model.r` to get modeling output.
5. Run `CI_matrix_graph_maker.py` to generate the plotting output.

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
+ `requirements.txt` provide requirements for creating a virtual environment
to replicate the analysis.
+ `Rplots.pdf` contains miscellaneous plotting output.
+ `scrape_data.py` is a Python script which retrieves the data from the source.
+ `scrape_params.json` contains parameters for the web scraping process.

