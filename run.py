# Your code goes here.
# You can delete these comments, but do not change the name of this file
# Write your code to expect a terminal of 80 characters wide and 24 rows high

import json
from notion_client import Client

# API-token from creds.json file
with open("creds.json", "r") as file:
    creds = json.load(file)

# set up client with API-token
notion = Client(auth=creds["NOTION_TOKEN"])

# Database IDs
database_id = "168284e4604f8013a728d0aa102775aa"
company_database_id = "168284e4604f80d7acfac51891eb0e3c"

def is_valid_email(email):
    """Check if email is valid"""
    return "@" in email

def find_email_in_database(email):
    """Check if email exists email database."""
    response = notion.databases.query(database_id=database_id)
    for page in response["results"]:
        properties = page["properties"]
        if properties["E-mail"]["title"][0]["text"]["content"] == email:
            return True  # Email does exist in database
    return None  # Email does not exist in database

def is_company_in_sales_list(company):
    """Check if company exists in the sales database."""
    response = notion.databases.query(database_id=company_database_id)
    for page in response["results"]:
        properties = page["properties"]
        if properties["Company"]["title"][0]["text"]["content"].lower() == company.lower():
            return True  # Company does exist in database
    return False  # Company does not exist in database

def add_email_to_database(email, company=None, notes=None):
    """Add email to database."""
    try:
        properties = {
            "E-mail": {"title": [{"text": {"content": email}}]},
        }
        if company:
            properties["Company"] = {"rich_text": [{"text": {"content": company}}]}
        if notes:
            properties["Notes"] = {"rich_text": [{"text": {"content": notes}}]}
        
        notion.pages.create(
            parent={"database_id": database_id},
            properties=properties,
        )
        print(f"🟢 Succes! '{email}' has been added to the database.")
    except Exception as e:
        print(f"Something went wrong: {e}")

def main():
    # Ask user what they want to do
    action = input("Do you want to add or update email? (add/update):\n").strip().lower()

    if action not in ["add", "update"]:
        print("Please choose 'add' or 'update'")
        return

    # Ask for email
    email = input("Enter email: \n").strip()

    # Validate email
    if not is_valid_email(email):
        print(f"Email '{email}' is not valid. Please try again.")
        return

    # Search for email in database
    page_id = find_email_in_database(email)

    if action == "add":
        if page_id:
            print(f"🔴 Email '{email}' already exists. You can not add it again.")
        else:
            print("🟢 Great! Email does not exist in the database. Please provide additional details.")
            company = input("Enter company name (optional):\n").strip()

            # Check if company already exist in sales list
            if company and is_company_in_sales_list(company):
                print(f"🔴 The company '{company}' is already in the sales list. Email will not be added.")
                return

            notes = input("Enter notes (optional):\n").strip()
            add_email_to_database(email, company, notes)

    elif action == "update":
        if page_id:
            print(f"Email '{email}' is in the database.")
            # Add function later
            print("Function coming later...")
        else:
            print(f"🔴 Email '{email}' is not in the database. Can not update.")

if __name__ == "__main__":
    main()