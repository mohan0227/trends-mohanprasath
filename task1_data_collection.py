import json
import requests
import time
import datetime
import os

headers = {"User-Agent": "TrendPulse/1.0"}

categories = {
    "technology": ["ai", "software", "tech", "code", "computer", "data", "cloud", "api", "gpu", "llm"],
    "worldnews": ["war", "government", "country", "president", "election", "climate", "attack", "global"],
    "sports": ["nfl", "nba", "fifa", "sport", "game", "team", "player", "league", "championship"],
    "science": ["research", "study", "space", "physics", "biology", "discovery", "nasa", "genome"],
    "entertainment": ["movie", "film", "music", "netflix", "game", "book", "show", "award", "streaming"]
}

data = []

def get_story_ids(category):
    url = "https://hacker-news.firebaseio.com/v0/topstories.json"
    response = requests.get(url, headers=headers)
    return response.json()

def get_story_details(story_id):
    url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.Timeout:
        print(f"TImeout error {story_id}. Skipping this story.")
    except requests.exceptions.RequestException as e:
        print(f"Error while fetching story {story_id}. Skipping this story.")
  
def classify_text(text, keywords):
    text = str(text).lower()
    if any(keyword in text for keyword in keywords):
        return True
    else:
        return False

for category, keywords in categories.items():
    story_ids = get_story_ids(category)
    cnt = 0
    for story_id in story_ids:
        if(cnt >= 25):
            break

        story_details = get_story_details(story_id)

        if not story_details:
            continue

        if "title" not in story_details:
            continue
        
        if classify_text(story_details["title"], keywords):
            entry = {
                "post_id": story_details.get('id'),
                "title": story_details.get('title'),
                "category": category,
                "score": story_details.get("score"),
                "num_comments": story_details.get("descendants", None),
                "author": story_details.get("by"),
                "collected_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            cnt += 1
            data.append(entry)

    print("Count for each category", cnt, category)
    time.sleep(2)

print("Total count", len(data))

try:
    os.mkdir("data")
    print("Created folder")

except FileExistsError:
    print("Folder already exists")

with open('data/trends_20240115.json', 'w') as file:
    json.dump(data, file)
print("File saved")