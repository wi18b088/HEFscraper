import requests
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename
import os

linklist = [
    "https://medium.com/swlh/why-hybrid-electric-aircraft-will-lead-the-way-in-vtol-c3c1fcec1f6f",
    "https://techxplore.com/news/2020-11-hybrid-electric-fuel-aircraft-green.html",
    "https://newatlas.com/drones/hydrogen-powered-vtol-drone/",
]
outputFolderName = "output/additionalSources"

# Check for output folder
if not os.path.exists(outputFolderName):
    os.mkdir(outputFolderName)

for i, link in enumerate(linklist):
    page = requests.get(link)
    print(page.status_code)
    if page.status_code == 200:
        soup = BeautifulSoup(page.text, 'html.parser')

        with open(f"{outputFolderName}/{i}_{sanitize_filename(soup.find('h1').text.replace(' ', ''))}.txt", "w") as myfile:
                try:
                    # Save contents to file
                    print(f"No: {i}; Content:")
                    myfile.write(soup.text)
                    myfile.write("\n")
                except:
                    pass