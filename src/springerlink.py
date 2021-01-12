#!/usr/bin/env python3
import pandas as pd
import requests
from bs4 import BeautifulSoup
import logging
import os
from pathvalidate import sanitize_filename
import pathlib

# Define some parameters
ownFileName = os.path.basename(__file__)
# outputFolderName = "output"
outputFolderName = "/mnt/inout/output/scraper/springerLink/txt"
logFolderName = "/mnt/inout/output/scraper/springerLink/log"
external_config_file_path = "/mnt/inout/config"
external_config_file_name = "scraper_config.py"

# Logger configuration

# Check for log folder
if not os.path.exists(logFolderName):
    pathlib.Path(logFolderName).mkdir(parents=True, exist_ok=True)

# Check for output folder
if not os.path.exists(outputFolderName):
    pathlib.Path(outputFolderName).mkdir(parents=True, exist_ok=True)

# Remove old log file
if os.path.exists(f'{logFolderName}/{ownFileName.split(".")[0]}.log'):
    os.remove(f'{logFolderName}/{ownFileName.split(".")[0]}.log')

logger = logging.getLogger(ownFileName)
stream_handler = logging.StreamHandler()
file_handler = logging.FileHandler(f'{logFolderName}/{ownFileName.split(".")[0]}.log')

logger.setLevel("DEBUG")
stream_handler.setLevel("DEBUG")
file_handler.setLevel("INFO")

stream_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', '%d/%m/%Y %H:%M:%S')
file_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', '%d/%m/%Y %H:%M:%S')
stream_handler.setFormatter(stream_format)
file_handler.setFormatter(file_format)

logger.addHandler(stream_handler)
logger.addHandler(file_handler)

# if no config exists in /mnt/inout/in/hef-scraper/config/springerlinkconfig
if pathlib.Path( external_config_file_path + "/" + external_config_file_name).is_file():
    logger.info("External Configuration found.")
    import importlib.util
    spec = importlib.util.spec_from_file_location("scraper_config", external_config_file_path + "/" + external_config_file_name)
    config_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(config_module)

    try:
        keywords = config_module.keywords
    except AttributeError:
        from springerlinkconfig import keywords
    try:
        startYear = config_module.startYear
    except AttributeError:
        from springerlinkconfig import startYear
    try:
        endYear = config_module.endYear
    except AttributeError:
        from springerlinkconfig import endYear
    try:
        contentType = config_module.contentType
    except AttributeError:
        from springerlinkconfig import contentType
    try:
        maxDownloads = config_module.maxDownloads
    except AttributeError:
        from springerlinkconfig import maxDownloads
else:
    logger.info("Using default configuration.")
    from springerlinkconfig import keywords, startYear, endYear, contentType, maxDownloads

df = pd.read_csv(f'https://link.springer.com/search/csv?showAll=false&query={"+".join(keywords)}&date-facet-mode=between&facet-start-year={startYear}&facet-end-year={endYear}&facet-content-type="{contentType}"')

# Print information about dataframe
# print(df.columns)                       # Prints the headers
# print(df["Item Title"][0:5])            # Prints the first 5 titles of available papers

# iterate over every URL in CSV and download text
for i, row in df.iterrows():

    if i == maxDownloads:
        break

    page = requests.get(row["URL"])
    if page.status_code == 200:
        soup = BeautifulSoup(page.text, 'html.parser')
        articlebody = soup.find('div', attrs={'class': 'c-article-body'})

        # No Article Contents
        if articlebody is None:
            logger.info(f"Position {i}: Entry with name '{row['Item Title']}' has no article body content.")
            continue

        articlesections = articlebody.find_all('section')
        with open(f"{outputFolderName}/{i}_{sanitize_filename(soup.find('h1').text)}.txt", "w") as myfile:
            for sec in articlesections:
                try:
                    # Save contents to file
                    myfile.write(sec.text)
                    myfile.write("\n")
                except:
                    pass