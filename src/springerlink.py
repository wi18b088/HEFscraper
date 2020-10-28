import pandas as pd
import requests
from bs4 import BeautifulSoup

# Define Keywords for one single combined search query
keywords = ["hybrid", "electric", "flying", "aircraft"]

# Get CSV from springerlink search (nice feature provided by Springer Link)
# URL taken from https://link.springer.com/search
# Additional constraints possible
# Download from web disabled for development / debug
# df = pd.read_csv(f'https://link.springer.com/search/csv?showAll=false&query={"+".join(keywords)}')

df = pd.read_csv('src/springerlink_search_results.csv')

# Print information about dataframe
# print(df.columns)                       # Prints the headers
# print(df["Item Title"][0:5])            # Prints the first 5 titles of available papers

# Download first article
page = requests.get(df.at[0, "URL"])
# print(page.status_code)                   # Prints 200 if get worked
soup = BeautifulSoup(page.text, 'html.parser')
articlebody = soup.find('div', attrs={'class': 'c-article-body'})
articlesections = articlebody.find_all('section')

# Print contents of the article and write to file
myfile = open(f"{soup.find('h1').text}.txt", "w")
for sec in articlesections:
    try:
        # Print contents
        print(sec.text)
        print("\n")

        # Save contents to file
        myfile.write(sec.text)
        myfile.write("\n")
    except:
        pass
myfile.close()