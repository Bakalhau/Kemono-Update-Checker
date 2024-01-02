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