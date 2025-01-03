import json
from notion_client import Client
import re # For email validation
from datetime import datetime  # Import for current date

# API-token from creds.json file
with open("creds.json", "r") as file:
    creds = json.load(file)

# Set up client with API-token
notion = Client(auth=creds["NOTION_TOKEN"])

# Database ID with lead emails
DATABASE_ID = "168284e4604f8013a728d0aa102775aa" 

# Database ID for current customers company
COMPANY_DATABASE_ID = "168284e4604f80d7acfac51891eb0e3c"

# Possible statuses to choose from in database
VALID_STATUSES = ["Not sent", "E-mail 1", "E-mail 2", "E-mail 3", "Meeting", "Not Interested"]

# Import colors from colorama
from colorama import Fore, Back, Style

def format_text(text, color="cyan"):
    """
    Format text with bold style and specified color.
    """
    colors = {
    "cyan": Fore.CYAN,
    "red": Fore.RED,
    "green": Fore.GREEN
    }

    selected_color = colors.get(color.lower(), Fore.RESET) 
    bold_prefix = "\033[1m"  
    reset_suffix = Style.RESET_ALL + "\033[0m"  
    return f"{bold_prefix}{selected_color}{text}{reset_suffix}"

class Lead:
    """
    This class manages lead data stored in the Notion database.

    Attributes:
        E-mail (str): The lead's email address.
        Company (str): The name of the company where the lead works (optional).
        Status (str): The status of the sales interaction (e.g., 'Email sent', 'Not sent', 'Meeting booked').
        Latest contact (str): The date of the most recent contact with the lead via email.
        Notes (str): Additional notes or comments related to the lead.
    """

    def __init__(self, notion_client, database_id, company_database_id):
        """
        Set the Lead Class with Notion client and database IDs
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
        Search for a lead in the email database by their email.
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
        Add a new lead to the database.
        """
        properties = {
            "E-mail": {"title": [{"text": {"content": email}}]},
        }
        if company:
            properties["Company"] = {"rich_text": [{"text": {"content": company}}]}
        if notes:
            properties["Notes"] = {"rich_text": [{"text": {"content": notes}}]}
        
        self.notion.pages.create(parent={"database_id": self.database_id}, properties=properties)
        print(format_text(f"🟢 Success! Lead '{email}' added to the database.", color="green"))

    def update_notes(self, page_id, action, content=None):
        """
        Update the notes for a specific lead.
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
            print(format_text("🔴 Invalid action. No changes made to notes.", color="red"))
            return

        self.notion.pages.update(
            page_id=page_id,
            properties={
                "Notes": {"rich_text": [{"text": {"content": updated_notes}}]},
            },
        )
        print(format_text(f"🟢 Success! Notes updated to: {updated_notes}", color="green"))

    def update_status(self, page_id, new_status):
        """
        Update the status and latest contact date for a lead.
        """
        current_date = datetime.now().strftime("%Y-%m-%d")
        self.notion.pages.update(
            page_id=page_id,
            properties={
                "Status": {"status": {"name": new_status}},
                "Latest contact": {"date": {"start": current_date}},
            },
        )
        print(format_text(f"🟢 Success! Status updated to '{new_status}' and date set to '{current_date}'.", color="green"))

def main():
    """
    Main function to manage lead data in the Notion database.
    """

    lead_manager = Lead(notion_client=notion, database_id=DATABASE_ID, company_database_id=COMPANY_DATABASE_ID)

    while True:  # Infinite loop to keep this running

        # Ask user to add or update email
        action = input(format_text("Let's get started! Do you want to add or update email? (add/update):\n", color="cyan")).strip().lower()
        if action not in ["add", "update"]:
            print(format_text("🔴 Invalid choice. Please choose 'add' or 'update'.", color="red"))
            continue

        while True:  # Loop for email input
            email = input(format_text("Enter email:\n", color="cyan")).strip()

            # Check if email is valid
            if not lead_manager.is_valid_email(email):
                print(format_text(f"🔴 Email '{email}' is not valid. Please try again.", color="red"))
                continue

            if action == "add":
                # Check if email is in database
                if lead_manager.find_by_email(email):
                    print(format_text(f"🔴 Email '{email}' already exists in the database. Please enter a new email.", color="red"))
                    continue
                else:
                    print(format_text(f"Good to go! '{email}' does not exist in the database.", color="green"))

                # Ask for company and check company sales list
                company = input(format_text("Enter company name (optional):\n", color="cyan")).strip()

                # Only run the company check if a company is provided
                if company:
                    if company and lead_manager.is_company_in_sales_list(company):
                        print(format_text(f"🔴 Company '{company}' is already in the sales list. Cannot add this email.", color="red"))
                        continue
                    else:
                        print(format_text(f"Good to go! '{company}' is not in the sales list.", color="green"))

                # Ask for notes and add lead
                notes = input(format_text("Enter notes (optional):\n", color="cyan")).strip()
                lead_manager.create(email, company, notes)
                break

            elif action == "update":
                # Check if email is in database
                page = lead_manager.find_by_email(email)

                if not page:
                    print(format_text(f"🔴 Email '{email}' not found in the database. Please enter a valid email.", color="red"))
                    continue
                else:
                    page_id = page["id"]
                    print(format_text(f"Good to go! '{email}' was found in the database.", color="green"))

                # Get the current notes in database
                current_notes = "".join(
                    [text["plain_text"] for text in page["properties"]["Notes"]["rich_text"]]
                    ) if "Notes" in page["properties"] and page["properties"]["Notes"]["rich_text"] else "No notes."

                # Ask for update notes or status
                while True:
                    update_action = input(format_text("Do you want to update status or notes? (status/notes):\n", color="cyan")).strip().lower()

                    # Update status
                    if update_action == "status":
                        print(format_text(f"Current status: {page['properties']['Status']['status']['name']}", color="cyan"))
                        new_status = None
                        while not new_status:
                            print(format_text(f"Enter the new status. Valid options are: {', '.join(VALID_STATUSES)}", color="cyan"))
                            new_status_input = input(format_text("New status:\n", color="cyan")).strip()
                            if new_status_input in VALID_STATUSES:
                                new_status = new_status_input
                            else:
                                print(format_text(f"🔴 Invalid status '{new_status_input}'. Please try again.", color="red"))
                        lead_manager.update_status(page_id, new_status)

                        # Add notes after status update
                        while True:
                            add_notes = input(format_text("Do you want to add or update notes as well? (yes/no):\n", color="cyan")).strip().lower()
                            if add_notes == "yes":
                                while True:
                                    print(format_text(f"Current notes: {current_notes}", color="cyan"))
                                    note_action = input(format_text("What do you want to do with the notes? (add/replace):\n", color="cyan")).strip().lower()
                                    if note_action in ["add", "replace"]:
                                        content = input(format_text("Enter your notes:\n", color="cyan")).strip()
                                        lead_manager.update_notes(page_id, note_action, content)
                                        main()
                                        break
                                    else:
                                        print(format_text("🔴 Invalid choice for notes. Please try again.", color="red"))
                                break
                            elif add_notes == "no":
                                print(format_text("No notes were added or updated.", color="cyan"))
                                main()
                                break
                            else:
                                print(format_text("🔴 Invalid input. Please enter 'yes' or 'no'.", color="red"))
                        break

                    # Update notes
                    elif update_action == "notes":
                        print(format_text(f"Current notes: {current_notes}", color="cyan"))

                        while True: 
                            note_action = input(format_text("What do you want to do with the notes? (add/replace):\n", color="cyan")).strip().lower()

                            if note_action in ["add", "replace"]:
                                content = input(format_text("Enter your notes:\n", color="cyan")).strip()
                                lead_manager.update_notes(page_id, note_action, content)
                                main()
                                break
                            else:
                                print(format_text("🔴 Invalid choice for notes. Please try again.", color="red"))
                                note_action = None  # Reset note_action to stay in the loop
                        break

                    else:
                        print(format_text("🔴 Invalid update choice. Please choose 'status' or 'notes'.", color="red"))


if __name__ == "__main__":
    main()
