import pandas as pd
import requests
from bs4 import BeautifulSoup
import logging
import os
import urllib.request
from pathvalidate import sanitize_filename
import runpy
import pathlib

# Define some parameters
ownFileName = os.path.basename(__file__)
# outputFolderName = "output"
outputFolderName = "/mnt/inout/output/scraper/springerlink/pdf"
sourceFolderName = "src"
logFolderName = "/mnt/inout/output/scraper/springerlink/log"
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

### Print information about dataframe
# print(df.columns)                       # Prints the headers
# print(df["Item Title"][0:5])            # Prints the first 5 titles of available papers

# iterate over every URL in CSV and download text
for i, row in df.iterrows():

    # for development & testing purposes only download 10 articles
    if i == maxDownloads:
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