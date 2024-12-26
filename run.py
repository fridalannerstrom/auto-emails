# Your code goes here.
# You can delete these comments, but do not change the name of this file
# Write your code to expect a terminal of 80 characters wide and 24 rows high

import os
from notion_client import Client

# Notion API token
os.environ["NOTION_TOKEN"] = "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"

# Connect to client
notion = Client(auth=os.environ["NOTION_TOKEN"])

# Set database ID
database_id = "168284e4604f8013a728d0aa102775aa"

def find_email_in_database(email):
    """Search email in database."""
    response = notion.databases.query(database_id=database_id)
    for page in response["results"]:
        properties = page["properties"]
        if properties["E-mail"]["title"][0]["text"]["content"] == email:
            return page["id"]  # Return page ID if email does exist
    return None  # Return None if email does not exist

def add_email_to_database(email):
    """Add email to database."""
    try:
        notion.pages.create(
            parent={"database_id": database_id},
            properties={
                "E-mail": {"title": [{"text": {"content": email}}]},
            },
        )
        print(f"🟢 Succes! '{email}' has been added to the database.")
    except Exception as e:
        print(f"Something went wrong: {e}")

def main():
    # Ask user that they want to do
    action = input("Do you want to add or update email? (add/update):\n").strip().lower()

    if action not in ["add", "update"]:
        print("Please choose 'add' or 'update")
        return

    # Ask for email
    email = input("Enter email: \n").strip()

    # Search for email in database
    page_id = find_email_in_database(email)

    if action == "add":
        if page_id:
            print(f"🔴 Email '{email}' already exists. You can not add it again. ")
        else:
            add_email_to_database(email)

    elif action == "update":
        if page_id:
            print(f"Email '{email}' is in the database.")
            # Add function later
            print("Function coming later...")
        else:
            print(f"🔴 Email '{email}' is not in the database. Can not update. ")

if __name__ == "__main__":
    main()