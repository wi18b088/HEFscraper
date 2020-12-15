import requests
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename
import os

# Collection of links to be downloaded (Newspaper / blog articles)
linklist = [
    "https://medium.com/swlh/why-hybrid-electric-aircraft-will-lead-the-way-in-vtol-c3c1fcec1f6f",
    "https://techxplore.com/news/2020-11-hybrid-electric-fuel-aircraft-green.html",
    "https://newatlas.com/drones/hydrogen-powered-vtol-drone/",
]

# Name of the output folder and subfolder
outputFolderName = "output/additionalSources"

# Check for output folder
if not os.path.exists(outputFolderName):
    # Create folder, if it doesn't exist yet
    os.mkdir(outputFolderName)

# Step through list of links
for i, link in enumerate(linklist):
    page = requests.get(link)
    print(page.status_code)
    # If request was successful
    if page.status_code == 200:
        soup = BeautifulSoup(page.text, 'html.parser')

        # Create new file named with the counter and a heading from the webpage
        with open(f"{outputFolderName}/{i}_{sanitize_filename(soup.find('h1').text.replace(' ', ''))}.txt", "w") as myfile:
                try:
                    # Save contents to file
                    print(f"No: {i}; Content:")
                    myfile.write(soup.text)
                    myfile.write("\n")
                except:
                    pass