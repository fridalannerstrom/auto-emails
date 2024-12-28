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
DATABASE_ID = "168284e4604f8013a728d0aa102775aa"
COMPANY_DATABASE_ID = "168284e4604f80d7acfac51891eb0e3c"

# Set possible statuses to choose from
VALID_STATUSES = ["Not sent", "E-mail 1", "E-mail 2", "E-mail 3", "Meeting", "Not Interested"] 

class Customer:
    def __init__(self, notion_client, database_id, company_database_id):
        self.notion = notion_client
        self.database_id = database_id
        self.company_database_id = company_database_id

    def is_valid_email(self, email):
        """Check if email is valid."""
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return bool(re.match(pattern, email))

    def find_by_email(self, email):
        """Find a customer by email in the database."""
        response = self.notion.databases.query(database_id=self.database_id)
        for page in response["results"]:
            if page["properties"]["E-mail"]["title"][0]["text"]["content"].lower() == email.lower():
                return page  # Return the full page object
        return None

    def is_company_in_sales_list(self, company):
        """Check if company exists in the sales database."""
        response = self.notion.databases.query(database_id=self.company_database_id)
        for page in response["results"]:
            if page["properties"]["Company"]["title"][0]["text"]["content"].lower() == company.lower():
                return True
        return False

    def create(self, email, company=None, notes=None):
        """Add a new customer to the database."""
        properties = {
            "E-mail": {"title": [{"text": {"content": email}}]},
        }
        if company:
            properties["Company"] = {"rich_text": [{"text": {"content": company}}]}
        if notes:
            properties["Notes"] = {"rich_text": [{"text": {"content": notes}}]}
        
        self.notion.pages.create(parent={"database_id": self.database_id}, properties=properties)
        print(f"🟢 Success! Customer '{email}' added to the database.")

    def update_notes(self, page_id, action, content=None):
        """Update the notes for a specific email."""
        page = self.notion.pages.retrieve(page_id=page_id)
        current_notes = "".join(
            [text["text"]["content"] for text in page["properties"]["Notes"]["rich_text"]]
        ) if "Notes" in page["properties"] and page["properties"]["Notes"]["rich_text"] else ""

        if action == "add":
            updated_notes = f"{current_notes} {content}".strip()
        elif action == "replace":
            updated_notes = content.strip()
        elif action == "remove":
            updated_notes = current_notes.replace(content, "").strip()
        else:
            print("🔴 Invalid action. No changes made to notes.")
            return

        self.notion.pages.update(
            page_id=page_id,
            properties={
                "Notes": {"rich_text": [{"text": {"content": updated_notes}}]},
            },
        )
        print(f"🟢 Success! Notes updated to: {updated_notes}")

    def update_status(self, page_id, new_status):
        """Update the status and latest contact date for a specific email."""
        current_date = datetime.now().strftime("%Y-%m-%d")
        self.notion.pages.update(
            page_id=page_id,
            properties={
                "Status": {"status": {"name": new_status}},
                "Latest contact": {"date": {"start": current_date}},
            },
        )
        print(f"🟢 Success! Status updated to '{new_status}' and date set to '{current_date}'.")

def main():
    customer_manager = Customer(notion_client=notion, database_id=DATABASE_ID, company_database_id=COMPANY_DATABASE_ID)

    while True: # Infinite loop to keep the program running
        action = input("Do you want to add or update email? (add/update):\n").strip().lower()
        if action not in ["add", "update"]:
            print("🔴 Invalid choice. Please choose 'add' or 'update'.")
            continue

        email = input("Enter email:\n").strip()
        if not customer_manager.is_valid_email(email):
            print(f"🔴 Email '{email}' is not valid. Please try again.")
            continue

        if action == "add":
            if customer_manager.find_by_email(email):
                print(f"🔴 Email '{email}' already exists in the database.")
                continue

            company = input("Enter company name (optional):\n").strip()
            if company and customer_manager.is_company_in_sales_list(company):
                print(f"🔴 Company '{company}' is already in the sales list. Cannot add this email.")
                continue

            notes = input("Enter notes (optional):\n").strip()
            customer_manager.create(email, company, notes)

        elif action == "update":
            page = customer_manager.find_by_email(email)
            if not page:
                print(f"🔴 Email '{email}' not found in the database. Cannot update.")
                continue

            page_id = page["id"]
            update_action = input("Do you want to update status or notes? (status/notes):\n").strip().lower()
            if update_action == "status":
                print(f"Current status: {page['properties']['Status']['status']['name']}")
                new_status = None
                while not new_status:
                    print(f"Enter the new status. Valid options are: {', '.join(VALID_STATUSES)}")
                    new_status_input = input("New status:\n").strip()
                    if new_status_input in VALID_STATUSES:
                        new_status = new_status_input
                    else:
                        print(f"🔴 Invalid status '{new_status_input}'. Please try again.")
                customer_manager.update_status(page_id, new_status)

            elif update_action == "notes":
                print(f"Current notes: {page['properties']['Notes']['rich_text']}")
                action = input("What do you want to do with the notes? (add/remove/replace):\n").strip().lower()
                if action in ["add", "replace", "remove"]:
                    content = input("Enter the content:\n").strip()
                    customer_manager.update_notes(page_id, action, content)
                else:
                    print("🔴 Invalid choice for notes. Please try again.")

            else:
                print("🔴 Invalid update choice. Please choose 'status' or 'notes'.")

if __name__ == "__main__":
    main()