import pandas as pd

df = pd.read_csv("spotify_playlist_data.csv")

# View dataset structure
print(df.head())

# Check column names
print(df.columns)

# Summary statistics of numerical features
print(df.describe())

