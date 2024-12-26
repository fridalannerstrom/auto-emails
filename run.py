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

# Databasens ID
database_id = "168284e4604f8013a728d0aa102775aa"

try:
    # Fråga databasen
    response = notion.databases.query(database_id=database_id)
    pprint(response)
except Exception as e:
    print(f"Ett fel inträffade: {e}")