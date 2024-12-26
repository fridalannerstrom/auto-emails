# Your code goes here.
# You can delete these comments, but do not change the name of this file
# Write your code to expect a terminal of 80 characters wide and 24 rows high

import os
from notion_client import Client
from pprint import pprint

# Notion API token
os.environ["NOTION_TOKEN"] = "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"

# Connect to client
notion = Client(auth=os.environ["NOTION_TOKEN"])

# Set database ID
database_id = "168284e4604f8013a728d0aa102775aa"

def find_email_in_database(email):
    """Search through the database for email"""
    response = notion.databases.query(database_id=database_id)
    for page in response["results"]:
        properties = page["properties"]
        if properties["E-mail"]["title"][0]["text"]["content"] == email:
            return True  # Returnera True om e-posten finns
    return False  # Returnera False om e-posten inte finns

def main():
    # Ask user för an email
    email = input("Enter the email you want to search: ")

    # Sök efter e-posten i databasen
    email_found = find_email_in_database(email)

    if email_found:
        print(f"The email '{email}' is already in the database.")
    else:
        print(f"The email '{email}' is not in the database. ")

if __name__ == "__main__":
    main()