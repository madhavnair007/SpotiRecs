
import pandas as pd

# Load the CSV file
file_path = file_path = "/Users/bhuvanhospet/Downloads/spotify_data.csv"  # Change this to your actual file path
df = pd.read_csv(file_path)

# Randomly select 1000 unique artists
random_artists = df["artist_name"].drop_duplicates().sample(1000, random_state=42)

# Filter the dataset to keep only songs from the selected artists
df_truncated = df[df["artist_name"].isin(random_artists)]

# Save the truncated dataset
output_path = "/Users/bhuvanhospet/Desktop/projects/SpotiRecs/src/backend/truncated_songs.csv"
df_truncated.to_csv(output_path, index=False)

print(f"Truncated dataset saved as {output_path} with {df_truncated.shape[0]} songs from 1000 random artists.")

