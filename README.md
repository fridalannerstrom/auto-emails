# Streamlining Sales Email Management in Notion ✉️

Welcome to my project for simplifying email management in Notion!

I work at a B2B company where I support the sales team by collecting leads, sending tailored emails, and tracking follow-ups to book meetings. While I rely on Notion to manage these workflows, it often feels clunky and slow, especially with large datasets.

To simplify and speed up my workflow, I developed a Python tool to streamline email list management. It’s made handling sales emails smoother, more efficient, and far less repetitive — saving me time and eliminating daily frustrations.

# Table of content

1. [Introduction](#introduction)
    - [Background](#background)
    - [Workflows](#workflows)
    - [Databases Overview](#databases-overview)
    - [Project Goals](#project-goals)

2. [Project Overview](#project-overview)
    - [Requirements](#requirements)
    - [Flowchart](#flowchart)
    - [Key Features](#key-features) (berätta vad man faktiskt kan göra i programmet)
    - [How To Use The Program](#how-to-use-the-program)
    - [User Experience](#user-experience) (prata om colorama, att jag vill ha tydliga färger eftersom jag jobbar snabbt osv... berätta om hur jag valt att lägga upp feedbacken osv) 

2. [Program Structure](#program-structure)
    - [Notion API Integration](#notion-api-integration)
    - [Lead Class](#lead-class)
    - [Main Function](#main-function)

3. [Tools and Technologies](#tools-and-technologies)
    - [Languages](#languages)
    - [Libraries](#libraries)
    - [Development Tools](#development-tools)
    - [Other Tools](#other-tools)

4. [Testing](#testing)
    - [Code Validation](#code-validation)
    - [Workflow Testing](#workflow-testing)
    - [Input Testing](#input-testing)
    - [Known Bugs and Limitations](#known-bugs-and-limitations)

5. [Future Improvements](#future-improvments)
    - [Automated Email Sending](#automated-email-sending)
    - [Integration with CRM Systems](#integration-with-crm-systems)
    - [Automated Reminders](#automated-reminders)

6. [Deployment](#deployment)
    - [Local Deployment](#local-deployment)
    - [GitHub Deployment](#github-deployment)

7. [Credits](#credits)
    - [Content](#content)
    - [Other](#other)
    - [Acknowledgements](#acknowledgements)

# Introduction

## Background

I work at a B2B company, supporting the sales team by managing email outreach to leads. My role includes responsibilities like social media, website management, and marketing, which naturally brings in a steady stream of leads. My primary tasks involve collecting these leads (email addresses) from various channels, following up with tailored emails based on pre-defined templates, and tracking progress.

I rely on Notion to manage this workflow, including tracking which leads have been contacted, what email templates were sent, responses received, follow-up reminders, and the dates of contact. The ultimate goal is to convert leads into booked meetings with the sales team.

While Notion is an excellent tool that I use extensively for many tasks, I’ve found it somewhat cumbersome and inefficient for managing this specific process. Despite its limitations, I chose Notion to centralize all my data, but I’m fully aware it’s not the ideal platform for email workflow management.

With this Python project, my goal is to build a tool that simplifies, automates, and enhances this workflow, saving me time and effort while addressing Notion’s limitations for email management.

## Workflows

I have two main workflows in Notion; collecting leads, and managing leads. I designed my Python program to align seamlessly with these workflows, optimizing the processes I already have in place and rely on daily. By building on my existing structure, the program enhances efficiency without disrupting familiar routines.

These workflows are described in more detail below.

### Workflow 1: Collecting Leads

I typically start my workday by spending around 30 minutes gathering email addresses from channels where potential leads can be found, such as social media, our CRM system, the company website, or other platforms frequented by our target audience. These email addresses are then added to a list of potential leads to be contacted.

#### 📋 **Workflow step by step**

1. Find email that I find relevant to contact.
2. Check if email is in database already.
3. Add email to database if email isn't already there.
4. Add information about company and notes (if any)

#### 🤯 **Issues with this workflow**

When a Notion database becomes very full, I’ve noticed it tends to become sluggish and laggy, making data handling unnecessarily time-consuming. This is especially challenging in my case, where I need to view the entire database, which contains hundreds of data points. Beyond the performance issues, however, there is a significant limitation in Notion’s functionality: the lack of automatic duplicate detection for databases.

This shortcoming requires me to manually ensure that an email doesn’t already exist in the database before adding it. To do so, I must load all database rows — clicking "load more" repeatedly — and then manually search (Ctrl + F) for every email I want to add. Additionally, I need to verify that the company associated with the email is not already in our sales list. This involves switching to a separate database, loading its data in a similar manner, and manually searching for the company name. These extra steps, while manageable in isolation, become highly repetitive and time-consuming when performed daily.

Despite my diligence in double-checking, duplicates occasionally slip through — whether it’s the same email added twice or contacting a lead from a company that’s already in our sales list. This has resulted in scenarios where emails were sent redundantly, even to leads who had previously declined. An automated solution for detecting duplicates across both databases would save significant time, reduce errors, and streamline the entire workflow.

----

### Workflow 2: Updating existing emails

In my leads database, I keep track of each lead’s status and the dates of contact. When I send an email, I update the status to something like "E-mail 1," showing that the lead received an email using that template. I use several templates in my workflow. If a lead replies and we start a conversation, I change their status to something like "Meeting Booked" or "Not Interested" and note the date of the update.

If a lead doesn’t respond within a week, I send a reminder email, updating their status to something like "Reminder E-mail 1" and recording the date it was sent. I also update notes in the database regularly, adding details such as if a lead wants to be contacted later or has shown interest in a specific product. This helps me stay on top of all interactions.

My workflow isn’t fixed but adapts based on when I send emails or receive responses. As soon as a lead replies, I update the database immediately to ensure the information is always accurate. Since my sales team depends on this database, keeping it up-to-date is essential.

#### **🤯 Issues with this workflow**

When I send an email to a lead, or receive a reply from a lead, I have to open the database, repeatedly click "load more" to access all the rows, and wait for everything to load — a process that becomes slow with larger datasets.

Once the database is fully loaded, I use Ctrl+F to search for the specific email and update the information. While this process is relatively straightforward, repeating it multiple times a day quickly becomes tedious. Constantly reopening the database, waiting for it to load, and searching for emails disrupts the workflow and makes the process feel unnecessarily time-consuming.

Of course, keeping the database open all the time would help streamline this process. However, since I use Notion extensively for various tasks, I often navigate elsewhere and forget to keep the leads database ready, adding another layer of inefficiency to my daily workflow.

## Databases Overview

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

![Company list database](images/company-database.png)

[SEE DATABASE LIVE HERE](https://sedate-molybdenum-41d.notion.site/company-database-168284e4604f80aca775d10d51bce604?pvs=4)

This database showcases all the companies we are already selling to. These are businesses where our Key Account Managers are actively engaged in conversations or ongoing sales. As such, I don’t need to include these companies in my lead management process, ensuring my focus remains on new opportunities.

This database is intentionally simple, containing only the companies that are our current customers. As a B2B company, we focus on tracking companies rather than individual contacts within them. The primary purpose of this database is to ensure that leads in the email list are not already existing customers.

There have been discussions about complementing this database with additional information, such as contact persons and which salesperson is responsible for the account. However, this information serves no purpose for me in my role. My primary concern is determining whether a company is already in our sales list, ensuring I don’t contact individuals at companies we are already selling to. This database is critical for preventing overlap between leads and existing customers, ensuring our email outreach is efficient and focused.

This list isn’t updated frequently, and when updates are needed, I can handle them manually. For now, I’ve chosen not to include this database in the Python program, as there are other areas where Python automation provides far greater efficiency and impact.

## Project Goals

Now that we've outlined the databases, workflows, and current issues with the workflow, let's focus on what we aim to achieve with this project. The goal is to streamline and simplify the process of managing leads while addressing the inefficiencies and limitations of the current system. This tool should enable a quick and seamless workflow, allowing for efficient handling of leads without unnecessary complexity or delays.

**Below is an overview of the primary goals for the project:**

| Goal | Description | 
| ------- | ---------- | 
| **Add New Leads** | Provide a quick and easy way to add new email leads to the database with minimal effort. | 
| **Automatic Duplicate Checker** | Ensure no duplicate emails are added by automatically checking if the email already exists. | 
| **Company Sales List Checker** | Automatically check if the lead belongs to a company we already sell to, avoiding redundant outreach. |
| **Update Email Status** | Simplify the process of updating the status and contact date of an email lead. |
| **Update Notes** | Make it easy to update or add notes for existing leads to keep track of relevant details. |
| **Minimal Options and Text** | Keep the workflow simple and to the point, avoiding unnecessary text or options for a fast UX. |
| **Clear Feedback** | Provide immediate and clear feedback to instantly confirm whether the expected action was successful or if an issue, like a duplicate, occurred. |

The overarching goal is to create a tool that integrates seamlessly into the current workflow, saving time and effort while providing the necessary features to manage leads effectively. This project aims to prioritize simplicity, speed, and usability for daily tasks.

# Project Overview

## Requirements

This requirements list outlines the specific functionality and features that this program must deliver to meet the project goals. Each requirement has been tailored to address the challenges described in the project's background and workflow, focusing on simplicity, speed, and accuracy. This list of requirements serves as the foundation for the program's development.

| Requirement | Description | 
| ------- | ---------- | 
| **Notion API Integration** | Use the Notion API to interact with two separate databases (leads and company sales list). This includes searching, retrieving, adding, and updating data efficiently. | 
| **Add New Leads** | The program must allow the user to input a new email address, company name, and optional notes, and add these to the leads database. | 
| **Duplicate Email Check** | Before adding a new email, the program must automatically search the leads database for the email. If the email is there, don't add the email to leads database. | 
| **Block Invalid Emails** | Validate email addresses using a predefined format and reject invalid entries with a clear error message. | 
| **Handle Optional Company Input** | Allow the user to optionally input a company name when adding a new lead, and verify against the company sales list database if provided. |
| **Company Sales List Check** | The program must automatically search the company sales list database to check if the lead’s company is already a customer. If it is, don't add the email to leads database. |
| **Update Lead Status** | The program must allow users to update the status field of a lead with predefined options. |
| **Update Notes** | The program must provide an option to either add to or completely replace the notes field for an existing lead. |
| **Immediate Feedback** | After every action, the program must display a message confirming success or failure. |
| **Error Handling for Inputs** | If the user inputs an invalid email, status, or note action, the program must display a clear error message and prompt the user to retry. |
| **Date Auto-Update** | When updating a lead's status, the program must automatically update the "Latest Contact" field with the current date. |
| **Efficient Database Loading** | The program must bypass Notion’s "load more" limitation by directly querying the full database via the API. |
| **Seamless Database Switching** | If a company check is required, the program must automatically switch to the company sales list database and return to the leads database afterward. |
| **Predefined Status Options** | The program must restrict status updates to a fixed set of options (e.g., "Not Sent," "E-mail 1," "Meeting Booked") to maintain data consistency. |
| **Minimal User Interaction** | If the user inputs an invalid email, status, or note action, the program must display a clear error message and prompt the user to retry. |
| **Prevent Duplicate Companies** | The program must prevent users from adding leads whose companies are already in the sales list database. |
| **Error Handling for Inputs** | If the user inputs an invalid email, status, or note action, the program must display a clear error message and prompt the user to retry. |

## Flowchart

![Flowchart](images/flowchart.png)

This flowchart, created in Adobe XD, illustrates the basic process for adding or updating leads in the program. The focus is on minimizing steps and creating an efficient, user-friendly flow. Using a flowchart as a visual representation allows me to clearly see the logical flow of the program, helping me break down workflows into manageable steps. 

| Shape/Color | Meaning | 
| ------- | ---------- | 
| **Circle** | Represents the start or end of the flow. | 
| **Diamond** | Represents a decision point in the workflow, such as yes/no or multiple choices. | 
| **Rectangle** | Represents an input or print step. | 
| **Purple** | Represents a program action, such as checking the database or displaying a message. | 
| **Grey** | Represents a user action, such as entering an email or selecting a status. | 

### Key aspects to note

| Feature | Description | 
| ------- | ---------- | 
| **Seamless Workflow** | The program is designed to loop in a way that aligns with my workflow. For example, if I try to add an email that already exists in the leads database, I want the program to prompt me to re-enter a new email instead of sending me back to the start. This ensures continuity in the "add leads" process. | 
| **Error Handling** | Similarly, if I for example add an email associated with a company already in the sales list or attempt to update a lead that doesn’t exist in the database, I want clear error messages and the ability to quickly retry without disrupting the workflow. | 
| **No Hard Stops** | The program is intentionally designed to never "stop" or "end". Once I successfully complete an action — such as adding a new lead or updating a lead’s information — the program should seamlessly return to the beginning, ready for the next input. | 

## Key Features

This program was built to simplify and streamline the workflow of managing leads in Notion. Below are the key features that have been implemented, highlighting what the program can do and how it aligns with the initial requirements and flowchart. Any deviations or additions have been noted.

| Feature | Description | 
| ------- | ---------- | 
| **Adding New Leads** | 1. Easily add new leads to the leads database with minimal input required.<br>2. Includes optional fields for company name and notes. <br>3. Automatically set status "Not sent" and leave date field empty. | 
| **Automatic Leads Duplicate Check** | 1. Automatically checks for duplicate emails in the leads database when adding new leads.<br>2. Prevents duplicates from being added.<br>3. Shows clear error messages if duplicates are detected.<br>4. Displays success messages for non-duplicates. | 
| **Automatic Company Sales List Check** | 1. Verifies whether a company associated with a lead already exists in the sales list database. <br>2. Prevents leads from being added if their company is an existing customer.<br>3. Shows clear error messages if a company is already in the sales list.<br>4. Displays success messages when the company is not in the sales list. | 
| **Update Status for Existing Leads** | 1. Allows users to update the status of a lead (e.g., "E-mail 1," "Meeting") based on predefined options. <br>2. Displays the current status before updating.<br>3. Shows possible statuses to choose from. <br>4. Allows users to immediately update notes after status updates to fit the normal workflow. | 
| **Date Auto-Update** | 1. Automatically updates the "Latest Contact" field whenever a lead's status changes. <br>2. Uses the current date dynamically for updates. | 
| **Update Notes for Existing Leads** | 1. Enables users to add or replace notes for existing leads.<br>2. Displays current notes before input for clarity. | 
| **Clear and Immediate Feedback** | 1. Provides clear, concise feedback for all actions, such as successful updates, errors, or duplicate detections.<br>2. Ensures users always know whether the intended action was successful or requires adjustments. | 
| **Minimal User Interaction** | 1. Designed to minimize inputs and steps, aligning with the quick workflow needed for sales management. <br>2. Loops processes to allow users to fix errors without restarting the workflow. | 
| **Enhanced User Experience** | 1. Uses color-coded feedback (via Colorama, more information below) to highlight important information. <br>2. Error messages and success confirmations are designed to provide all necessary information without overwhelming the user. <br>3. Emojis enhance feedback, making it easier to recognize successes or issues.| 
| **Colored Messages** | 1. Differentiates program output from user input by using cyan for program messages and white for user input. <br>2. Error messages are displayed in red for immediate attention. <br>3. Success messages are displayed in green to confirm successful actions. |
| **Input Error Handeling** | 1. Prevents invalid inputs, such as missing "@" in email addresses.<br>2. Prompts users to try again if an input is invalid. <br>3. Skips unnecessary inputs without generating errors. | 
| **Avioding Breaks** | 1. Ensures the program never stops abruptly or loops back to the beginning when errors happen. | 

----

### Changes from Initial Requirements or Flowchart

✅ **More Feedback Messages**<br>Additional confirmation and error messages were added to enhance user clarity.

✅ **Improved Error Handling**<br>The program ensures smooth loops when invalid inputs occur, rather than requiring users to start over.

✅ **Focus on UX**<br>The color-coded system and reduced steps were optimized beyond the initial requirements to ensure the program feels intuitive and fast.

✅ **Enhanced Input Validation**<br>The program ensures that user inputs are accurate by verifying key details, such as confirming that an email address is valid and that the status selected matches predefined options. This prevents incorrect or invalid data from being added to the database, maintaining its integrity and reliability.

## How To Use The Program

This program is deployed via Heroku and can be accessed here: [Auto Emails Application](https://auto-emails-e92e0f29caf5.herokuapp.com/)

To view the leads database and verify that leads are being added or updated, visit: [Leads Database](https://sedate-molybdenum-41d.notion.site/auto-emails-168284e4604f806eb9a7dcdc7e005e9b?pvs=4)

To access the company sales list database and ensure accuracy in the workflow, visit: [Company Database](https://sedate-molybdenum-41d.notion.site/company-database-168284e4604f80aca775d10d51bce604?pvs=4)

### How to add a lead

Explain step-by-step how to add a lead

### How to update a lead

Explain step-by-step how to update a leads information.

## User Experience

Explain that the goal is to create a very easy, clear and simple way to handle leads. Not many options, not a lot of text. 

### Adding Leads

This is a process where quickness is important. I want to add leads as quickly as possible. So there should not be a lot of text or steps to add a lead, thats important. and I want clear messages in this process to that I see right away that this lead is not already in the database, or in the company sales list. And then, a very clear way to see that an action has happened with an emoji. Leaving company and notes optional because I sometimes don't have time fixing this, I sometimes add this later when theres time. I want feedback all the time, after every input.

### Updating Leads

This is also a process where I want quickness. I want to only show the important things. So, a success message that the email I want to edit is actually in the database, that the program found the email. And show current status and notes, so I get a qucik overview of what currently is in the database. When updating a lead, date and company is not important, so this is not shown at all. Here I also use emojis to easily show that something has happened or not. Here I also want a lot of feedback, so I know things are going as expected. 

### Colorama

I use colorama for a better user experience... Cyan is for basic messages, green is for something good, red is for something "bad" (something didn't go as planned). Explan how I installed colorama etc. I don't want to waste time reading to much so I'm happy just to look at a color and see if it went as I wanted or not.

# Program Structure

The program is structured with API integration to Notion. A class and methods to handle leads and a main function to handle.... more information below.

## Notion API

Explain how this works, link to the page where I was guided.

## Lead Class

Explan the lead class and why I chose to do this. Show before and after code.

## Main function

Explain how the main function is set up, and how it works with the methods. Maybe also talk about how this could be improved?

## Other

Function to handle formatting on messages, because there is so many messages and it was repetativ to formatt every one (show before and after)

## Issues

Trouble with notes loop, wanting to loop back to the main function when I'm deep in a loop. I solved this by getting function main inside the loop. Not so clean but it works...

# Tools and Technologies

## Languages

Python only

## Libraries

json: Parses the creds.json file to extract Notion API credentials.
notion_client: Facilitates interaction with the Notion API, enabling CRUD operations in Notion databases.
re: Validates email addresses to ensure data integrity.
datetime: Tracks the date of the last interaction with leads.
colorama: Enhances the terminal interface with colored and styled text.

## Development Tools

Gitpod, Github, Heroku

## Other Tools

Notion: The core database platform integrated with the project, enabling lead management and email tracking.

Python Interpreter: Used to run and test the Python program locally.

Adobe XD for Flowchart

# Testing

## Code Validation

PEP test thing

## Workflow Testing

Test if the program does what I wanted in the start? My list of requirements and wished from the start?

## Input Testing 

- Test for inputs:
    - Things to test:
    - a letter `a`
    - multiple letters `abc`
    - a number `1`
    - multiple numbers `123`
    - an empty ENTER with nothing `ENTER`
    - only spaces
    - special characters `?` `!` `@`
    - `isalpha()` , `isnumeric()` , `isalphanum()`

## Known Bugs and Limitations

Not any that I know of!

# Future Improvements

Explain that I will definetly keep working with this project because it helped me so much already. I see the possibilitues with python and Notion for this workflow. Something that I want to do is:

## Automated Email Sending
The program could be extended to automatically send emails using predefined templates. Maybe a bunch of emails at a time. This would streamline the workflow further, eliminating the need to switch between the program and an email client.

### Integration with CRM Systems
Add integration with CRM platform Upsales so that Key Account Managers easily can see activity for leads.

## Automated Reminders
Set up automatic reminders for follow-ups. For instance, if a lead hasn’t replied within a week, the program could send a reminder notification or email.

# Deployment

## Local Deployment

## Github Deployment

# Credits

## Content

## Other

## Acknowledgements