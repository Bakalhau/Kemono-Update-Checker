import requests
import os
from dotenv import load_dotenv
from classes import ContentCreator

load_dotenv()

DIR = os.getenv('DIR')
DISCORD_WEBHOOK_URL = os.getenv('DISCORD_WEBHOOK_URL')

def main():
    ContentCreator.read_csv(DIR)
    for creator in ContentCreator.all:
        if creator.cached_posts == None:
            creator.rewrite_logs()
            continue
        if creator.new_posts == None:
            print(f"No changes in {creator.name}'s gallery since {creator.present_posts[0]['date']}")
        elif len(creator.new_posts) > 0:
            for post in creator.new_posts:
                print(f"New: {post['title']}, date: {post['date']}, url: {post['url']}")

            while True: 
                creator.rewrite_logs()
                break

if __name__ == "__main__": 
    main()