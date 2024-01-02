import requests
import os
from dotenv import load_dotenv
from classes import ContentCreator

load_dotenv()

DIR = os.getenv('DIR')
DISCORD_WEBHOOK_URL = os.getenv('DISCORD_WEBHOOK_URL')

