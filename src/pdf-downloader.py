import pandas as pd
import requests
from bs4 import BeautifulSoup
import logging
import os

# Define some parameters
ownFileName = os.path.basename(__file__)
outputFolderName = "output"
sourceFolderName = "src"
logFolderName = "log"

# Logger configuration

# Check for log folder
if not os.path.exists(logFolderName):
    os.mkdir(logFolderName)

# Check for output folder
if not os.path.exists(outputFolderName):
    os.mkdir(outputFolderName)

# Remove old log file
if os.path.exists(f'{logFolderName}/{ownFileName.split(".")[0]}.log'):
    os.remove(f'{logFolderName}/{ownFileName.split(".")[0]}.log')

logger = logging.getLogger(ownFileName)
stream_handler = logging.StreamHandler()
file_handler = logging.FileHandler(f'{logFolderName}/{ownFileName.split(".")[0]}.log')

logger.setLevel(logging.DEBUG)
stream_handler.setLevel(logging.DEBUG)
file_handler.setLevel(logging.INFO)

stream_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', '%d/%m/%Y %H:%M:%S')
file_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', '%d/%m/%Y %H:%M:%S')
stream_handler.setFormatter(stream_format)
file_handler.setFormatter(file_format)

logger.addHandler(stream_handler)
logger.addHandler(file_handler)

# Define Keywords for one single combined search query
keywords = ["hybrid", "electric", "flying", "aircraft"]

# Get CSV from springerlink search (nice feature provided by Springer Link)
# URL taken from https://link.springer.com/search
# Additional constraints possible
# Download from web disabled for development / debug
# df = pd.read_csv(f'https://link.springer.com/search/csv?showAll=false&query={"+".join(keywords)}')

df = pd.read_csv(f'{sourceFolderName}/springerlink_search_results.csv')

# Print information about dataframe
# print(df.columns)                       # Prints the headers
# print(df["Item Title"][0:5])            # Prints the first 5 titles of available papers

# iterate over every URL in CSV and download text
for i, row in df.iterrows():

    # for development & testing purposes only download 10 articles
    if i == 10:
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
        with open(f"{outputFolderName}/{i}_{soup.find('h1').text}.txt", "w") as myfile:
            for sec in articlesections:
                try:
                    # Save contents to file
                    myfile.write(sec.text)
                    myfile.write("\n")
                except:
                    pass