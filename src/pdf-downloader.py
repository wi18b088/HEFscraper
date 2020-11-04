import pandas as pd
import requests
from bs4 import BeautifulSoup
import logging
import os
import urllib.request
from pathvalidate import sanitize_filename
import runpy

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
startYear = 2010
endYear = 2021
contentType = "Article"

# Get CSV from springerlink search (nice feature provided by Springer Link)
# URL taken from https://link.springer.com/search
# Additional constraints possible

### Download from web disabled for development / debug
# df = pd.read_csv(f'https://link.springer.com/search/csv?showAll=false&query={"+".join(keywords)}&date-facet-mode=between&facet-start-year={startYear}&facet-end-year={endYear}&facet-content-type="{contentType}"')

### Save query to .csv in source folder.
# df.to_csv(f"{sourceFolderName}/springerlink_articles_newest.csv")
# print(df.head())
df = pd.read_csv(f'{sourceFolderName}/springerlink_articles_newest.csv')

### Print information about dataframe
# print(df.columns)                       # Prints the headers
# print(df["Item Title"][0:5])            # Prints the first 5 titles of available papers

# iterate over every URL in CSV and download text
for i, row in df.iterrows():

    # for development & testing purposes only download 10 articles
    if i == 10:
        break

    # Grabs URL from CSV file
    page = requests.get(row["URL"])
    if page.status_code == 200:
        soup = BeautifulSoup(page.text, 'html.parser')
        
        # Look for paid article button. Seems to be ignored?
        #BuyArticleButton = soup.find('a', attrs={'class': 'c-article-buy-box'})
        #if BuyArticleButton is None:
            # Find PDF button on springerlink website
        
        PDFbutton = soup.find('a', attrs={'class': 'c-pdf-download__link'})
        if PDFbutton is not None:
            URL = PDFbutton.get('href')
        else: # Find alternative PDF download button
            PDFbutton = soup.find('a', attrs={'data-track-action': 'Pdf download'})
            if PDFbutton is not None:
                URL = "https://link.springer.com" + PDFbutton.get('href')
            else:
                logger.info(f"Position {i}: Entry with name '{row['Item Title']}' has no PDF download button.")
                # if there is no PDF button, run springerlink.py to scrape text from the page
                #file_globals = runpy.run_path(f'{sourceFolderName}/springerlink.py')
                continue
        
        #else: #skipping paid articles
         #   print("Skipped article because it's paid")
          #  continue

        local_filename = sanitize_filename(str(i) + "_" +  soup.find('h1').text)
        # Download file to output folder    
        urllib.request.urlretrieve(URL, outputFolderName+"/"+local_filename+".pdf")    