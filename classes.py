import csv
import requests
from bs4 import BeautifulSoup
import re


class ContentCreator:
    all = list()
    services = ("patreon", "fanbox")
    
    def __init__(self, name, service, id):
        self.name = name
        self.service = service
        self.id = id
        self.present_posts = self.get_posts()
        self.cached_posts = self.read_posts()
        self.new_posts = self.get_new_posts()
        
        ContentCreator.all.append(self)
    
    @classmethod
    def read_csv(cls, path=""):
        if path != "" and path[-1] != "/":
            path += "/"
        
        with open(path + "creators.csv") as f:
            creators = tuple(csv.DictReader(f))
            for i in range(len(creators)):
                creator = creators[i]
                
                if creator["service"].lower() not in cls.services:
                    raise ValueError(f"Invalid service: \"{creator['service']}\" for creator: \"{creator['name']}\" at line {i+2}")
                
                cls(creator["name"], creator["service"], creator["id"])
    
    def __str__(self): 
        return f"name: {self.name}, service: {self.service}, id: {self.id}"
    
    def get_posts(self): 
        posts = list()
        
        homepage_file = requests.get(f"https://kemono.party/{self.service}/user/{self.id}")
        
        homepage_code = BeautifulSoup(homepage_file.text, "html.parser")
        
        brute_posts = homepage_code.find_all("article", {"class": "post-card"})

        for brute_post in brute_posts:
            # Post title
            title = brute_post.find("header").string.strip()
            
            # Post date
            date = brute_post.find("time").string.strip()
            
            # Post image
            image_container = brute_post.find("div", {"class": "post-card__image-container"})
            image_element = image_container.find("img") if image_container else None
            image = "https:" + image_element.get("src", "") if image_element else ""
            
            # Post url
            url = "https://kemono.party" + brute_post.find("a")["href"]
            
            posts.append({
                "title": title,
                "date": date,
                "url": url,
                "image": image,
            })
        
        return tuple(posts)
    
    def get_profile(self):
            profile = list()
            
    def read_posts(self, path=""):
        posts = []
        try: 
            with open(path + f"logs/{self.name}_{self.service}.csv") as f:
                posts = tuple(csv.DictReader(f))
                return posts
        except FileNotFoundError:
            return None
    
    def get_new_posts(self): 
        posts = []
        if self.present_posts == self.cached_posts: return None
        
        for post in self.present_posts:
            if self.cached_posts and post in self.cached_posts: 
                break
            posts.append(post)
        
        return tuple(posts)
    
    def rewrite_logs(self, path=""):
        if path != "" and path[-1] != "/":
            path += "/"
        
        with open(path + f"logs/{self.name}_{self.service}.csv", "w") as f:
            fieldnames = ["title", "date", "url", "image"]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            
            writer.writeheader()
            for post in self.present_posts:
                writer.writerow(post)