import pandas as pd
import numpy as np
import os

df = pd.read_csv("data/trends_clean.csv")
print("Loaded data:", df.shape)
print("\nFirst 5 rows:\n", df.head())
print("\nAverage score:", df['score'].mean().round(2))
print("Average num_comments:", df['num_comments'].mean().round(2))

print("\n--- NumPy Stats ---")
print("Mean score   :", np.mean(df['score']).round(2))
print("Median score :", np.median(df['score']).round(2))
print("Std deviation:", round(np.std(df['score']),2))
print("Max score    :", np.max(df['score']))
print("Min score    :", np.min(df['score']))

category, cnt = np.unique(df['category'], return_counts=True)
max_val_index = np.argmax(cnt)
print(f"\nMost stories in: {category[max_val_index]} ({cnt[max_val_index]} stories)")

most_cmntd_story = np.argmax(df['num_comments'])
print(f"\nMost commented story: \"{df.loc[most_cmntd_story]['title']}\"  — {int(df.loc[most_cmntd_story]['num_comments'])} comments\n")

try:
    os.mkdir('data')
    print("Created folder")
except FileExistsError:
    print("File ALready Exists")

with open("data/trends_analysed.csv", "w", encoding='utf-8') as file:
    df.to_csv(file, index=False)

print("Save to data/trends_analysed.csv")