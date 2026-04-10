import pandas as pd
import os

df = pd.read_json('data/trends_20240115.json')
df.shape

df = df.drop_duplicates(subset="post_id", keep="first") # Dropping rows with same post_id expect first occurence
df = df[df['post_id'].notna()].reset_index(drop=True) # Dropping rows containing null values in post_id

# Making sure the below list of columns are always integer
int_cols = ['score', 'num_comments']
df[int_cols] = df[int_cols].apply(pd.to_numeric, errors='coerce')

df = df[df['score'] > 5] # Dropping rows with score less than 5
print(df.shape)

df['title'] = df['title'].str.strip()

try:
    os.mkdir('data')
    print("Created folder")
except FileExistsError:
    print("File ALready Exists")

with open("data/trends_clean.csv", "w", encoding='utf-8') as file:
    df.to_csv(file, index=False)

print("Saved to data/trends_clean.csv")