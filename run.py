import json
from notion_client import Client
import re # For email validation
from datetime import datetime  # Import for current date

# API-token from creds.json file
with open("creds.json", "r") as file:
    creds = json.load(file)

# Set up client with API-token
notion = Client(auth=creds["NOTION_TOKEN"])

# Database ID with potential customer emails
DATABASE_ID = "168284e4604f8013a728d0aa102775aa" 

# Database ID for current customers company
COMPANY_DATABASE_ID = "168284e4604f80d7acfac51891eb0e3c"

# Possible statuses to choose from in database
VALID_STATUSES = ["Not sent", "E-mail 1", "E-mail 2", "E-mail 3", "Meeting", "Not Interested"]

# Import colors from colorama
from colorama import Fore, Back, Style

class Customer:
    """
    This class manages customer data stored in the Notion database.

    Attributes:
        E-mail (str): The customer's email address.
        Company (str): The name of the company where the customer works (optional).
        Status (str): The status of the sales interaction (e.g., 'Email sent', 'Not sent', 'Meeting booked').
        Latest contact (str): The date of the most recent contact with the customer via email.
        Notes (str): Additional notes or comments related to the customer.
    """

    def __init__(self, notion_client, database_id, company_database_id):
        """
        Set the Customer Class with Notion client and database IDs
        """
        self.notion = notion_client
        self.database_id = database_id
        self.company_database_id = company_database_id

    def is_valid_email(self, email):
        """
        Validate the format of an email address.
        """
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return bool(re.match(pattern, email))

    def find_by_email(self, email):
        """
        Search for a customer in the email database by their email.
        """
        response = self.notion.databases.query(database_id=self.database_id)
        for page in response["results"]:
            if page["properties"]["E-mail"]["title"][0]["text"]["content"].lower() == email.lower():
                return page  # Return the full page object
        return None

    def is_company_in_sales_list(self, company):
        """
        Search for company in the current company sales list.
        """
        response = self.notion.databases.query(database_id=self.company_database_id)
        for page in response["results"]:
            if page["properties"]["Company"]["title"][0]["text"]["content"].lower() == company.lower():
                return True
        return False

    def create(self, email, company=None, notes=None):
        """
        Add a new customer to the database.
        """
        properties = {
            "E-mail": {"title": [{"text": {"content": email}}]},
        }
        if company:
            properties["Company"] = {"rich_text": [{"text": {"content": company}}]}
        if notes:
            properties["Notes"] = {"rich_text": [{"text": {"content": notes}}]}
        
        self.notion.pages.create(parent={"database_id": self.database_id}, properties=properties)
        print(Fore.GREEN + f"🟢 Success! Customer '{email}' added to the database." + Style.RESET_ALL)

    def update_notes(self, page_id, action, content=None):
        """
        Update the notes for a specific customer.
        """
        page = self.notion.pages.retrieve(page_id=page_id)
        current_notes = "".join(
            [text["text"]["content"] for text in page["properties"]["Notes"]["rich_text"]]
        ) if "Notes" in page["properties"] and page["properties"]["Notes"]["rich_text"] else ""

        if action == "add":
            updated_notes = f"{current_notes} {content}".strip()
        elif action == "replace":
            updated_notes = content.strip()
        else:
            print(Fore.RED + "🔴 Invalid action. No changes made to notes." + Style.RESET_ALL)
            return

        self.notion.pages.update(
            page_id=page_id,
            properties={
                "Notes": {"rich_text": [{"text": {"content": updated_notes}}]},
            },
        )
        print(Fore.GREEN + f"🟢 Success! Notes updated to: {updated_notes}" + Style.RESET_ALL)

    def update_status(self, page_id, new_status):
        """
        Update the status and latest contact date for a customer.
        """
        current_date = datetime.now().strftime("%Y-%m-%d")
        self.notion.pages.update(
            page_id=page_id,
            properties={
                "Status": {"status": {"name": new_status}},
                "Latest contact": {"date": {"start": current_date}},
            },
        )
        print(Fore.GREEN + f"🟢 Success! Status updated to '{new_status}' and date set to '{current_date}'." + Style.RESET_ALL)

def main():
    """
    Main function to manage customer data in the Notion database.
    """

    customer_manager = Customer(notion_client=notion, database_id=DATABASE_ID, company_database_id=COMPANY_DATABASE_ID)

    while True:  # Infinite loop to keep this running

        # Ask user to add or update email
        action = input(Fore.CYAN + "Do you want to add or update email? (add/update):\n" + Style.RESET_ALL).strip().lower()
        if action not in ["add", "update"]:
            print(Fore.RED + "🔴 Invalid choice. Please choose 'add' or 'update'." + Style.RESET_ALL)
            continue

        while True:  # Loop for email input
            email = input(Fore.CYAN + "Enter email:\n" + Style.RESET_ALL).strip()

            # Check if email is valid
            if not customer_manager.is_valid_email(email):
                print(Fore.RED + f"🔴 Email '{email}' is not valid. Please try again." + Style.RESET_ALL)
                continue

            if action == "add":
                # Check if email is in database
                if customer_manager.find_by_email(email):
                    print(Fore.RED + f"🔴 Email '{email}' already exists in the database. Please enter a new email." + Style.RESET_ALL)
                    continue
                else:
                    print(Fore.GREEN + f"Good to go! '{email}' does not exist in the database." + Style.RESET_ALL)

                # Ask for company and check company sales list
                company = input(Fore.CYAN + "Enter company name (optional):\n" + Style.RESET_ALL).strip()
                if company and customer_manager.is_company_in_sales_list(company):
                    print(Fore.RED + f"🔴 Company '{company}' is already in the sales list. Cannot add this email." + Style.RESET_ALL)
                    continue
                else:
                    print(Fore.GREEN + f"Good to go! '{company}' is not in the sales list." + Style.RESET_ALL)

                # Ask for notes and add customer
                notes = input(Fore.CYAN + "Enter notes (optional):\n" + Style.RESET_ALL).strip()
                customer_manager.create(email, company, notes)
                break

            elif action == "update":
                # Check if email is in database
                page = customer_manager.find_by_email(email)
                if not page:
                    print(Fore.RED + f"🔴 Email '{email}' not found in the database. Please enter a valid email." + Style.RESET_ALL)
                    continue
                else:
                    print(Fore.GREEN + f"Good to go! '{email}' was found in the database." + Style.RESET_ALL)

                # Get the current notes in database
                current_notes = "".join(
                    [text["plain_text"] for text in page["properties"]["Notes"]["rich_text"]]
                    ) if "Notes" in page["properties"] and page["properties"]["Notes"]["rich_text"] else "No notes available."

                # Ask for update notes or status
                page_id = page["id"]
                update_action = input(Fore.CYAN + "Do you want to update status or notes? (status/notes):\n" + Style.RESET_ALL).strip().lower()

                # Update status
                if update_action == "status":
                    print(Fore.CYAN + f"Current status: {page['properties']['Status']['status']['name']}" + Style.RESET_ALL)
                    new_status = None
                    while not new_status:
                        print(Fore.CYAN + f"Enter the new status. Valid options are: {', '.join(VALID_STATUSES)}" + Style.RESET_ALL)
                        new_status_input = input(Fore.CYAN + "New status:\n" + Style.RESET_ALL).strip()
                        if new_status_input in VALID_STATUSES:
                            new_status = new_status_input
                        else:
                            print(Fore.RED + f"🔴 Invalid status '{new_status_input}'. Please try again." + Style.RESET_ALL)
                    customer_manager.update_status(page_id, new_status)

                    # Add notes after status update
                    add_notes = input(Fore.CYAN + "Do you want to add or update notes as well? (yes/no):\n" + Style.RESET_ALL).strip().lower()
                    if add_notes == "yes":
                        while True:
                            print(Fore.CYAN + f"Current notes: {current_notes}" + Style.RESET_ALL)
                            note_action = input(Fore.CYAN + "What do you want to do with the notes? (add/replace):\n" + Style.RESET_ALL).strip().lower()
                            if note_action in ["add", "replace"]:
                                content = input(Fore.CYAN + "Enter your notes:\n" + Style.RESET_ALL).strip()
                                customer_manager.update_notes(page_id, note_action, content)
                                break
                            else:
                                print(Fore.RED + "🔴 Invalid choice for notes. Please try again." + Style.RESET_ALL)

                # Update notes
                elif update_action == "notes":
                    print(Fore.CYAN + f"Current notes: {current_notes}" + Style.RESET_ALL)
                    note_action = input(Fore.CYAN + "What do you want to do with the notes? (add/replace):\n" + Style.RESET_ALL).strip().lower()
                    if note_action in ["add", "replace"]:
                        content = input(Fore.CYAN + "Enter your notes:\n" + Style.RESET_ALL).strip()
                        customer_manager.update_notes(page_id, note_action, content)
                    else:
                        print(Fore.RED + "🔴 Invalid choice for notes. Please try again." + Style.RESET_ALL)

                else:
                    print(Fore.RED + "🔴 Invalid update choice. Please choose 'status' or 'notes'." + Style.RESET_ALL)
                break


if __name__ == "__main__":
    main()
