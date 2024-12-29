# Handeling sales emails in Notion ✉️

Welcome to my project for simplifying email management in Notion!

This project is based on my personal workflow for managing my database with emails to new leads. This has been a game-changer in streamlining these processes, and has saved me a significant amount of time and effort, allowing me to focus on more meaningful tasks while automating the repetitive ones.

# Table of content

1. [Title](#title)
   - [Title](#title)
   - [Title](#title)
   - [Title](#title)
   - [Title](#title)
   - [Title](#title)

# Background

I work at a B2B company, supporting the sales team by managing email outreach to leads. My role encompasses responsibilities like social media, website management, and marketing, which naturally brings in a steady stream of leads. My primary tasks involve collecting these leads (email addresses) from various channels, following up with tailored emails based on pre-defined templates, and tracking progress.

I rely on Notion to manage this workflow, including tracking which leads have been contacted, what email templates were sent, responses received, follow-up reminders, and the dates of contact. The ultimate goal is to convert leads into booked meetings with the sales team.

While Notion is an excellent tool that I use extensively for many tasks, I’ve found it somewhat cumbersome and inefficient for managing this specific process. Despite its limitations, I chose Notion to centralize all my data, but I’m fully aware it’s not the ideal platform for email workflow management.

To streamline and enhance this process, I developed a Python program to automate and simplify my workflows. This solution has made managing email outreach faster, smoother, and far less tedious, addressing the limitations of using Notion for this purpose.

## Workflows

I have two main workflows in Notion; collecting leads, and managing leads. I designed my Python program to align seamlessly with these workflows, optimizing the processes I already have in place and rely on daily. By building on my existing structure, the program enhances efficiency without disrupting familiar routines.

These workflows are described in more detail below.

### Workflow 1: Collecting Leads

I typically start my workday by spending around 30 minutes gathering email addresses from channels where potential leads can be found, such as social media, our CRM system, the company website, or other platforms frequented by our target audience. These email addresses are then added to a list of potential leads to be contacted.

**📋 Workflow step by step**

1. Find email that I find relevant to contact.
2. Check if email is in database already.
3. Add email to database if email isn't already there.
4. Add company where this person works (important as we are a B2B company).
5. Select status "Not sent".
6. Enter notes, if any.

**🤯 Issues with this workflow**

When a Notion database becomes very full, I’ve noticed it tends to become sluggish and laggy, making data handling unnecessarily time-consuming. This is especially challenging in my case, where I need to view the entire database, which contains hundreds of data points. Beyond the performance issues, however, there is a significant limitation in Notion’s functionality: the lack of automatic duplicate detection for databases.

This shortcoming requires me to manually ensure that an email doesn’t already exist in the database before adding it. To do so, I must load all database rows — clicking "load more" repeatedly — and then manually search (Ctrl + F) for every email I want to add. While this may seem like a small inconvenience, it quickly becomes repetitive and time-consuming, especially with larger datasets.

Despite my diligence in double-checking, duplicates occasionally slip through. This has resulted in situations where the same email was sent twice, even to leads who had previously declined. An automated duplicate-checking feature would not only save time but also prevent unnecessary errors, making the workflow far more efficient.

### Workflow 2: Updating existing emails

I update existing emails in the list with a new status, mostly, when I've sent an email or recieved an answer. There are different statuses to choose from. I sent the date when status is changed. I also add notes.

## Databases in Notion

I have two databases in Notion, one for emails to potential new leads and one for current customers.

⚠️ This project uses dummy databases with fictional data to ensure privacy. The real database I work with daily includes additional columns like source (where the lead was found), SNI code (a Swedish industry classification), and interest (indicating which sales offers are relevant based on factors like website activity). It also has more statuses, such as additional email templates and options like "Do not contact" or "Need to book a meeting." For simplicity, this project only includes the essential columns and basic statuses.

### Database 1: Email list

PRINTSCREEN

See database live here: (LINK)

This database is a list over emails to new leads. These emails are people that might be intreseted in our product and we want to send an email to them and keep track if they answer. This database consists of 5 columns as described below:

| Column | Description | 
| ------- | ---------- | 
| **E-mail** | E-mail to the potential lead | 
| **Company** | Company where this lead works. This is important because we are a B2B company and we need to match this with the company sales list database. More information in here. |
| **Status** | The status of the lead, to see if we've sent any email, if the person has answererd, if we have booked a meeting etc. More information below. | 
| **Latest Contact** | The date for the last contact of this lead. This is important because we send reminder e-mails to leads that haven't answered our emails. | 
| **Notes** | This is a place to write notes about this lead. | 

The status column has specific options to choose from. The status can only be one of the following statuses:

| Status | Description | Tag |
| ------- | ----------- | --------------- |
| **Not sent** | Is for... | IMAGE |
| **E-mail 1** | Is for... | IMAGE |
| **E-mail 2** | Is for... | IMAGE |
| **E-mail 3** | Is for... | IMAGE |
| **Meeting** | Is for... | IMAGE |
| **Not Interested** | Is for... | IMAGE |

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