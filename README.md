# Decathlon International Championship Placing Prediction

This is a project which aims to forecast international competition placing
in the track and field decathlon based on event performances during said
competition. It is part of the thesis work "Mathematical Characterization
of Elite Performance and Optimal Training in the Track & Field Decathlon"
by Perry Battles.

## File Inventory

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

