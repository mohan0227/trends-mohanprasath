import pandas as pd
import matplotlib.pyplot as plt
import os

df = pd.read_csv("data/trends_analysed.csv")

try:
    os.mkdir('output')
    print("Created folder")
except FileExistsError:
    print("File ALready Exists")

top_ten_stories = df.sort_values(by='score', ascending=False).head(10)

def shorten_title(title):
    if len(title) <= 50:
        return title
    else:
        return title[:50] + "..."

# Chart 1
top_ten_stories['shortened_text'] = top_ten_stories['title'].apply(shorten_title)

plt.figure()
plt.barh(top_ten_stories["shortened_text"], top_ten_stories["score"])
plt.xlabel("Score")
plt.ylabel("Story Title")
plt.title("Top 10 Stories by score")
plt.savefig("output/chart1_top_stories.png", bbox_inches='tight')
plt.show()
plt.close()

# Chart 2
category_counts = df["category"].value_counts()

plt.figure()
plt.bar(category_counts.index, category_counts.values)
plt.xlabel("Category")
plt.ylabel("Number of Stories")
plt.title("Number of Stories per Category")
plt.savefig("output/chart2_categories.png", bbox_inches='tight')
plt.show()
plt.close()

# Chart 3
if "is_popular" not in df.columns:
    df["is_popular"] = df["score"] > 100

popular = df[df["is_popular"] == True]
non_popular = df[df["is_popular"] == False]

plt.figure()

plt.scatter(popular["score"], popular["num_comments"], label="Popular")
plt.scatter(non_popular["score"], non_popular["num_comments"], label="Non Popular")

plt.xlabel("Score")
plt.ylabel("Number of Comments")
plt.title("Popular vs Non Popular stories")
plt.legend()

plt.savefig("output/chart3_scatter.png", bbox_inches='tight')
plt.show()
plt.close()

# Dashborad
img1 = plt.imread("output/chart1_top_stories.png")
img2 = plt.imread("output/chart2_categories.png")
img3 = plt.imread("output/chart3_scatter.png")

fig, axes = plt.subplots(1, 3, figsize=(18, 5))

# Display images
axes[0].imshow(img1)
axes[1].imshow(img2)
axes[2].imshow(img3)

for ax in axes:
    ax.axis("off")

axes[0].set_title("Top Stories")
axes[1].set_title("Category Distribution")
axes[2].set_title("Score vs Comments")

plt.suptitle("TrendPulse Dashboard", fontsize=16)

plt.savefig("output/dashboard.png", bbox_inches='tight')
plt.show()
plt.close()
