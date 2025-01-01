# Streamlining Sales Email Management in Notion ✉️

Welcome to my project for simplifying email management in Notion!

I work at a B2B company where I support the sales team by collecting leads, sending tailored emails, and tracking follow-ups to book meetings. While I rely on Notion to manage these workflows, it often feels clunky and slow, especially with large datasets.

To simplify and speed up my workflow, I developed a Python tool to streamline email list management. It’s made handling sales emails smoother, more efficient, and far less repetitive — saving me time and eliminating daily frustrations.

# Table of content

1. [Title](#title)
   - [Title](#title)
   - [Title](#title)
   - [Title](#title)
   - [Title](#title)
   - [Title](#title)

# Background

I work at a B2B company, supporting the sales team by managing email outreach to leads. My role includes responsibilities like social media, website management, and marketing, which naturally brings in a steady stream of leads. My primary tasks involve collecting these leads (email addresses) from various channels, following up with tailored emails based on pre-defined templates, and tracking progress.

I rely on Notion to manage this workflow, including tracking which leads have been contacted, what email templates were sent, responses received, follow-up reminders, and the dates of contact. The ultimate goal is to convert leads into booked meetings with the sales team.

While Notion is an excellent tool that I use extensively for many tasks, I’ve found it somewhat cumbersome and inefficient for managing this specific process. Despite its limitations, I chose Notion to centralize all my data, but I’m fully aware it’s not the ideal platform for email workflow management.

With this Python project, my goal is to build a tool that simplifies, automates, and enhances this workflow, saving me time and effort while addressing Notion’s limitations for email management.

## Workflows

I have two main workflows in Notion; collecting leads, and managing leads. I designed my Python program to align seamlessly with these workflows, optimizing the processes I already have in place and rely on daily. By building on my existing structure, the program enhances efficiency without disrupting familiar routines.

These workflows are described in more detail below.

### Workflow 1: Collecting Leads

I typically start my workday by spending around 30 minutes gathering email addresses from channels where potential leads can be found, such as social media, our CRM system, the company website, or other platforms frequented by our target audience. These email addresses are then added to a list of potential leads to be contacted.

**📋 Workflow step by step**

1. Find email that I find relevant to contact.
2. Check if email is in database already.
3. Add email to database if email isn't already there.
4. Add information about company and notes (if any)

**🤯 Issues with this workflow**

When a Notion database becomes very full, I’ve noticed it tends to become sluggish and laggy, making data handling unnecessarily time-consuming. This is especially challenging in my case, where I need to view the entire database, which contains hundreds of data points. Beyond the performance issues, however, there is a significant limitation in Notion’s functionality: the lack of automatic duplicate detection for databases.

This shortcoming requires me to manually ensure that an email doesn’t already exist in the database before adding it. To do so, I must load all database rows — clicking "load more" repeatedly — and then manually search (Ctrl + F) for every email I want to add. Additionally, I need to verify that the company associated with the email is not already in our sales list. This involves switching to a separate database, loading its data in a similar manner, and manually searching for the company name. These extra steps, while manageable in isolation, become highly repetitive and time-consuming when performed daily.

Despite my diligence in double-checking, duplicates occasionally slip through — whether it’s the same email added twice or contacting a lead from a company that’s already in our sales list. This has resulted in scenarios where emails were sent redundantly, even to leads who had previously declined. An automated solution for detecting duplicates across both databases would save significant time, reduce errors, and streamline the entire workflow.

### Workflow 2: Updating existing emails

In my leads database, I keep track of each lead’s status and the dates of contact. When I send an email, I update the status to something like "E-mail 1," showing that the lead received an email using that template. I use several templates in my workflow. If a lead replies and we start a conversation, I change their status to something like "Meeting Booked" or "Not Interested" and note the date of the update.

If a lead doesn’t respond within a week, I send a reminder email, updating their status to something like "Reminder E-mail 1" and recording the date it was sent. I also update notes in the database regularly, adding details such as if a lead wants to be contacted later or has shown interest in a specific product. This helps me stay on top of all interactions.

My workflow isn’t fixed but adapts based on when I send emails or receive responses. As soon as a lead replies, I update the database immediately to ensure the information is always accurate. Since my sales team depends on this database, keeping it up-to-date is essential.

**🤯 Issues with this workflow**

When I send an email to a lead, or receive a reply from a lead, I have to open the database, repeatedly click "load more" to access all the rows, and wait for everything to load — a process that becomes slow with larger datasets.

Once the database is fully loaded, I use Ctrl+F to search for the specific email and update the information. While this process is relatively straightforward, repeating it multiple times a day quickly becomes tedious. Constantly reopening the database, waiting for it to load, and searching for emails disrupts the workflow and makes the process feel unnecessarily time-consuming.

Of course, keeping the database open all the time would help streamline this process. However, since I use Notion extensively for various tasks, I often navigate elsewhere and forget to keep the leads database ready, adding another layer of inefficiency to my daily workflow.

## Databases in Notion

I have two databases in Notion, one for emails to potential new leads and one for current customers.

⚠️ This project uses dummy databases with fictional data to ensure privacy. The real database I work with daily includes additional columns like source (where the lead was found), SNI code (a Swedish industry classification), and interest (indicating which sales offers are relevant based on factors like website activity). It also has more statuses, such as additional email templates and options like "Do not contact" or "Need to book a meeting." For simplicity, this project only includes the essential columns and basic statuses.

### Database 1: Email list

![Email list database](images/email-database.png)

[SEE DATABASE LIVE HERE](https://sedate-molybdenum-41d.notion.site/auto-emails-168284e4604f806eb9a7dcdc7e005e9b?pvs=4)

This is a list of email addresses. While the emails here are fictional, they accurately represent the structure of my real leads database. This is where I gather all the leads I identify and track their status, notes, and other relevant details. The database consists of five columns, which are described below.

| Column | Description | 
| ------- | ---------- | 
| **E-mail** | The email address of the potential lead. | 
| **Company** | The company where the lead works. This is important for our B2B operations as we check it against the company sales list database. More details provided below. |
| **Status** | Tracks the lead's status, such as whether an email has been sent, if they’ve responded, or if a meeting has been booked. Additional details are outlined below. | 
| **Latest Contact** | Records the date of the most recent interaction with the lead. This is key for scheduling reminder emails to leads who haven’t replied. | 
| **Notes** | A space to log additional information about the lead, such as specific preferences or follow-up actions. | 

The status column has specific options to choose from. The status can only be one of the following statuses:

| Status | Description | Tag |
| ------- | ----------- | --------------- |
| **Not sent** | Indicates that no email has been sent to the lead yet. | ![Not sent tag](images/not-sent.png) |
| **E-mail 1** | Shows that an email based on template 1 has been sent to the lead. | ![E-mail 1 tag](images/e-mail-1.png) |
| **E-mail 2** | Reflects that a follow-up email based on template 2 has been sent to the lead. | ![E-mail 2 tag](images/e-mail-2.png) |
| **E-mail 3** | Indicates that another follow-up email, this time based on template 3, has been sent to the lead. | ![E-mail 3 tag](images/e-mail-3.png) |
| **Meeting** | Means that a meeting has been successfully booked with the lead. | ![Meeting tag](images/meeting.png) |
| **Not Interested** | Indicates that the lead has explicitly expressed they are not interested in the offer or product. | ![Not interested tag](images/not-interested.png) |

### Database 2: Company sales list

PRINTSCREEN

See database live here: (LINK)

This database is intentionally simple, containing only the companies that are our current customers. As a B2B company, we focus on tracking companies rather than individual contacts within them. The primary purpose of this database is to ensure that leads in the email list are not already existing customers. Since it serves a specific function, it is not updated frequently.

# Flowchart

I use Notion daily to manage sales emails, which is a part of my role in supporting the sales team. My workflow includes finding emails, sending emails and keeping track of email activity. The ultimate goal of these emails is to help the sales team book meetings for product demos. 

While Notion is an excellent tool for many purposes, it lacks the flexibility and automation I need for these specific tasks. To address this, I built a Python-based solution that integrates seamlessly with Notion, making email management faster, easier, and more reliable.

Include:
- Introduction to the project
- My work flow in Notion
- Flowchart
- Code: Notion API
- Code: Change to classes, code before and after
- Testing
    - All inputs
- Colorama
- Trouble with notes
- Future: Connection with outlook to update status automatically. A way to send lots of emails at the same time, to a bunch of emails. Auto send reminder emails to those that haven't answered. 