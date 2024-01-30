import requests
import os
import random
from time import sleep
from dotenv import load_dotenv
from datetime import datetime
from classes import ContentCreator

load_dotenv()

DIR = os.getenv('DIR')
DISCORD_WEBHOOK_URL = os.getenv('DISCORD_WEBHOOK_URL')
EMBED_COLOR = os.getenv('EMBED_COLOR')

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

                if DISCORD_WEBHOOK_URL:
                    # Get post title, url, date and image
                    post_title = post['title']
                    post_url = post['url']
                    post_date = post['date']
                    post_image = post['image']

                    # Get profile link, icon and name from creator    
                    profile_link = (f"https://coomer.party/{creator.service}/user/{creator.id}")
                    profile_icon = (f"https://img.coomer.su/icons/{creator.service}/{creator.id}")
                    profile_name = (f"{creator.name}")

                    # Convert date to discord format
                    post_date = post_date.split(".")[0]

                    discord_date = datetime.strptime(post_date, "%Y-%m-%d %H:%M:%S")

                    post_date = discord_date.strftime("%Y-%m-%dT%H:%M:%S.000Z")

                    embed_color = EMBED_COLOR

                    if not embed_color:
                        # Generate a random hexadecimal color
                        color = "%06x" % random.randint(0, 0xFFFFFF)

                        # Format the values as decimal string
                        embed_color = int(color, 16)

                    # Create discord embed
                    embed = {
                            "embeds": [
                                {
                                "title": post_title,
                                "url": post_url,
                                "color": embed_color,
                                "author": {
                                    "name": profile_name,
                                    "url": profile_link,
                                    "icon_url": profile_icon
                                },
                                "timestamp": post_date,
                                "image": {
                                    "url": post_image
                                }
                                }
                            ],
                            }
                    # Make webhook request to discord    
                    request = requests.post(DISCORD_WEBHOOK_URL,json=embed)
                    print(request)
                    sleep(10)
            while True: 
                creator.rewrite_logs()
                break

if __name__ == "__main__": 
    main()