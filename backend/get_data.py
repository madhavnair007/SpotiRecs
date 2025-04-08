import pandas as pd

# Load the CSV file
file_path = "/Users/bhuvanhospet/Downloads/spotify_data.csv"  # Update this if needed
df = pd.read_csv(file_path)

# Filter to only songs released before 2000
df_before_2000 = df[df["year"] > 2000]

# Randomly select 300 unique artists from those songs
random_artists = df_before_2000["artist_name"].drop_duplicates().sample(300, random_state=42)

# Get all songs (even after 2000) by those 300 artists — if you want only pre-2000 songs by them, use df_before_2000
df_truncated = df[df["artist_name"].isin(random_artists)]

# Save the truncated dataset
output_path = "/Users/bhuvanhospet/Desktop/projects/SpotiRecs/backend/trunc_songs.csv"
df_truncated.to_csv(output_path, index=False)

print(f"Truncated dataset saved as {output_path} with {df_truncated.shape[0]} songs from 300 random artists before 2000.")
