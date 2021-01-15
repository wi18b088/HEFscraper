import requests
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename
import os
import pathlib


outputFolderName = "/mnt/inout/output/scraper/txt"
external_config_file_path = "/mnt/inout/config"
external_config_file_name = "universalscraperconfig.py"

if pathlib.Path( external_config_file_path + "/" + external_config_file_name).is_file():
    import importlib.util
    spec = importlib.util.spec_from_file_location("universal_config", external_config_file_path + "/" + external_config_file_name)
    config_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(config_module)

    try:
        linklist = config_module.linklist
    except AttributeError:
        from universalscraperconfig import linklist
else:
    from universalscraperconfig import linklist

if not os.path.exists(outputFolderName):
    pathlib.Path(outputFolderName).mkdir(parents=True, exist_ok=True)

# Step through list of links
for i, link in enumerate(linklist):
    page = requests.get(link)
    print(f"HTTP Status Code: {page.status_code}")
    # If request was successful
    if page.status_code == 200:
        soup = BeautifulSoup(page.text, 'html.parser')

        # Create new file named with the counter and a heading from the webpage
        heading = "Article"
        if temp := soup.find('h1'): heading = temp.text
        with open(f"{outputFolderName}/{i}_{sanitize_filename(heading.replace(' ', ''))}.txt", "w") as myfile:
                try:
                    # Save contents to file
                    print(f"Downloading entry No: {i}")
                    myfile.write(soup.text)
                    myfile.write("\n")
                except:
                    pass