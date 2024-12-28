# Your code goes here.
# You can delete these comments, but do not change the name of this file
# Write your code to expect a terminal of 80 characters wide and 24 rows high

import json
from notion_client import Client
import re # For email validation
from datetime import datetime  # Import for current date

# API-token from creds.json file
with open("creds.json", "r") as file:
    creds = json.load(file)

# Set up client with API-token
notion = Client(auth=creds["NOTION_TOKEN"])

# Database IDs
database_id = "168284e4604f8013a728d0aa102775aa"
company_database_id = "168284e4604f80d7acfac51891eb0e3c"

def is_valid_email(email):
    """Check if email is valid."""
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(pattern, email))

def find_email_in_database(email):
    """Check if email exists email database."""
    response = notion.databases.query(database_id=database_id)
    for page in response["results"]:
        properties = page["properties"]
        if properties["E-mail"]["title"][0]["text"]["content"] == email:
            return page["id"] 
    return None  

def is_company_in_sales_list(company):
    """Check if company exists in the sales database."""
    response = notion.databases.query(database_id=company_database_id)
    for page in response["results"]:
        properties = page["properties"]
        if properties["Company"]["title"][0]["text"]["content"].lower() == company.lower():
            return True  
    return False 

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
        print(f"🔴 Something went wrong: {e}")

def update_email_notes(page_id):
    """Update the notes for a specific email dynamically."""
    try:
        # Get the relevant page
        page = notion.pages.retrieve(page_id=page_id)
        current_notes = ""

        # Get the current notes
        if "Notes" in page["properties"] and page["properties"]["Notes"]["rich_text"]:
            current_notes = "".join(
                [text["text"]["content"] for text in page["properties"]["Notes"]["rich_text"]]
            )
            print(f"Current notes: {current_notes}")
        else:
            print("No current notes found.")

        # Ask user what to do
        action = input("What do you want to do with the notes? (add/remove/replace/skip):\n").strip().lower()

        if action == "add":
            new_notes = input("Enter new notes to add:\n").strip()
            updated_notes = f"{current_notes} {new_notes}".strip()
            print(f"Updating notes...")

        elif action == "remove":
            if not current_notes:
                print("There are no notes to remove.")
                return
            print(f"Current notes: {current_notes}")
            remove_text = input("Enter the text you want to remove:\n").strip()
            updated_notes = current_notes.replace(remove_text, "").strip()
            print(f"Updating notes...")

        elif action == "replace":
            new_notes = input("Enter new notes to replace existing ones:\n").strip()
            updated_notes = new_notes
            print(f"Updating notes...")

        elif action == "skip":
            print("No changes made to notes.")
            return

        else:
            print("🔴 Invalid choice. No changes made to notes.")
            return

        # Update notes
        notion.pages.update(
            page_id=page_id,
            properties={
                "Notes": {"rich_text": [{"text": {"content": updated_notes}}]},
            },
        )
        print(f"🟢 Success! Notes updated to: {updated_notes}")

    except Exception as e:
        print(f"🔴 Something went wrong during the notes update: {e}")

VALID_STATUSES = ["Not sent", "E-mail 1", "E-mail 2", "E-mail 3", "Meeting", "Not Interested"] # User can only select these statuses

def update_email_status(page_id):
    """Update the status and latest contact date for a specific email."""
    try:
        # Get current status
        page = notion.pages.retrieve(page_id=page_id)
        current_status = page["properties"]["Status"]["status"]["name"]
        print(f"Current status: {current_status}")

        # Ask for new status
        new_status = None
        while not new_status:
            print(f"Enter the new status. Can only be: {', '.join(VALID_STATUSES)}")
            user_input = input("New status: \n").strip()
            
            if user_input in VALID_STATUSES:
                new_status = user_input
            else:
                print(f"🔴 Invalid status '{user_input}'. Please try again.")

        # Get the current date
        current_date = datetime.now().strftime("%Y-%m-%d")

        # Update database
        notion.pages.update(
            page_id=page_id,
            properties={
                "Status": {"status": {"name": new_status}},  
                "Latest contact": {"date": {"start": current_date}}, 
            },
        )
        print(f"🟢 Success! Status updated to '{new_status}' and date set to '{current_date}'.")

        # Ask if user wants to add notes
        add_notes = input("Do you want to add or update notes? (yes/no): \n").strip().lower()
        if add_notes == "yes":
            update_email_notes(page_id)

    except Exception as e:
        print(f"🔴 Something went wrong during the update: {e}")

def main():
    while True:
        # Ask user what they want to do
        action = input("Do you want to add or update email? (add/update):\n").strip().lower()

        if action not in ["add", "update"]:
            print("🔴 Please choose 'add' or 'update'")
            continue

        # Ask for email
        email = input("Enter email: \n").strip()

        # Validate email
        if not is_valid_email(email):
            print(f"Email '{email}' is not valid. Please try again.")
            continue

        # Search for email in database
        page_id = find_email_in_database(email)

        # Add email 
        if action == "add":
            if page_id:
                print(f"🔴 Email '{email}' already exists. You can not add it again.")
                continue
            else:
                print("🟢 Great! Email does not exist in the database. Please provide additional details.")
                company = input("Enter company name (optional):\n").strip()

                # Check if company already exist in sales list
                if company and is_company_in_sales_list(company):
                    print(f"🔴 The company '{company}' is already in the sales list. Email will not be added.")
                    continue

                notes = input("Enter notes (optional):\n").strip()
                add_email_to_database(email, company, notes)

        # Update e-mail
        elif action == "update":
            if page_id:
                print(f"🟢 Success! Found '{email}' in the database.")
                update = input("Do you want to update status or notes? (status/notes): \n").strip().lower()
                if update == "status":
                    update_email_status(page_id)
                elif update == "notes":
                    update_email_notes(page_id)
                else:
                    print("🔴 Invalid choice. Please choose 'status' or 'notes'.")
            else:
                print(f"🔴 Email '{email}' is not in the database. Can not update.")

if __name__ == "__main__":
    main()