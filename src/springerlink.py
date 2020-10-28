import pandas as pd

# Define Keywords
keywords = ["hybrid", "electric", "flying", "aircraft"]

# Get CSV from springerlink search (nice feature provided by Springer Link)
df = pd.read_csv(f'https://link.springer.com/search/csv?showAll=false&query={"+".join(keywords)}')
print(df)