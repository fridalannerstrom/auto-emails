# Your code goes here.
# You can delete these comments, but do not change the name of this file
# Write your code to expect a terminal of 80 characters wide and 24 rows high

import os
from notion_client import Client
from pprint import pprint

# Sätt din Notion-token som en miljövariabel i koden
os.environ["NOTION_TOKEN"] = "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"

# Initiera klienten
notion = Client(auth=os.environ["NOTION_TOKEN"])

# Gör en förfrågan för att lista användare
list_users_response = notion.users.list()
pprint(list_users_response)