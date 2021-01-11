import requests
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename
import os
import pathlib

from universalscraperconfig import linklist, outputFolderName

# Check for output folder
if not os.path.exists(outputFolderName):
    # Create folder, if it doesn't exist yet
    pathlib.Path(outputFolderName).mkdir(parents=True, exist_ok=True)

# Step through list of links
for i, link in enumerate(linklist):
    page = requests.get(link)
    print(page.status_code)
    # If request was successful
    if page.status_code == 200:
        soup = BeautifulSoup(page.text, 'html.parser')

        # Create new file named with the counter and a heading from the webpage
        heading = "Article"
        if temp := soup.find('h1'): heading = temp.text
        with open(f"{outputFolderName}/{i}_{sanitize_filename(heading.replace(' ', ''))}.txt", "w") as myfile:
                try:
                    # Save contents to file
                    print(f"No: {i}")
                    # myfile.write(soup.text)
                    myfile.write(soup.text)
                    myfile.write("\n")
                except:
                    pass