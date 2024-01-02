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
