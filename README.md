# Analysis of ASANA tickets in Google Sheets
This is a demo* version of an analytical project, whose purpose was to provide a certain level of detail about ASANA tasks, that wasn't possible using the ASANA's built-in analytical features.
  
**The access tokens and GIDs were replaced with fake data and the content of the Google Sheets report was artificially generated.*

## The business need
The whole project evolved from the need to have a tool that could be used as a basis for invoicing our customers for support and developments tickets. These tickets were managed in ASANA and mixed with other tasks that were considered out-of-scope for the invoicing. Separation of the in-scope and out-of-scope tickets was not possible directly in ASANA and therefore it required custom approach. A task was considered in-scope if it was assigned to a member of development team in any point in time in the task's history.

## Overview of the solution
I have decided to use:
* ASANA's API to access the data of the tickets (using `asana` python library)
* Python to transform the data
* Google Sheets document for the tickets' analysis
* Google's API to insert the data to the Google Sheets document (using `pygsheets` python library)
* `cron` job to run the python script automatically and periodically

The whole solution was designed in a way that would allow making changes to the scope (adding new ASANA projects that should be part of the reports or removing old ones) without touching the python scripts. The same logic was followed in the area of financial aspects - the pricing model was developped directly in the Google Sheets report.

## Solution in detail
The following sections describe the solution in more detail.

### 1) Setting up access tokens for authentication with APIs
#### Google Cloud Platform
* Set up a project in Google Cloud Platform console and allow Google Sheets API
* Create service account that will edit the Google Sheets document
  * The document had to be shared with this account and (with editor rights)

#### ASANA
* Create Personal Access Token

*In this demo I have included a fake ASANA's PAT directly in the `const.py` file for the demonstration purposes only. The recommended solution is to have this secret stored in an environment variable.*

### 2) Extracting the list of developers
Extracting all the users of ASANA workspace using `users.get_users()` function and selecting only developers. The result was saved to the `dev_team.csv` file (only demo data here).

### 3) Setting up a configuration Google Sheets document
A configuration Google Sheets document was used to store references to the final Google Sheets reports for individual clients in the form of each report's GID (the GID of each report was added after the report was created).

![The columns of the config Google Sheets document](/assets/config_clients_page.png "Config Google Sheets' columns")

### 4) Creating ETL script
There are three python files:
* `const.py` - definition of constants and clients
* `functions.py` - definition of functions used in the main file
* `main.py` - the data extraction and processing logic

Code inside the `main.py` file has the following procedural logic:
1. Variables initialization - dates and log
2. Importing data about clients from the config file
3. Iterating over the list of clients acquired in previous step
    1. Connecting to the client's Google Sheets report
    2. Fetching data about ASANA projects associated with the client from the config sheet of the report
    3. Removing all the data from the data sheet*
    4. Iterating over the list of ASANA projects for the given client - **the core extraction and transformation logic**
        1. Getting all the tasks from the project
        2. Getting all the historical assignees for each task
        3. Flagging tasks with assignees from the `dev_team.csv` file
        4. Write the data to the client's Google Sheets
    5. Report formatting and cleanup routines
4. Inserting log into the config Gooogle Sheets document

**It was necessary to fetch data for all tasks everytime, becasue we could not reliably tell which tasks were not modified after being closed. Therefore incremental updates were not possible.*

## The report structure
There are two groups of sheets in every report - first group consists of those used for analysis ("frontend" sheets) and second group is used as a support to the first group ("backend" sheets - hidden in the production versions). All sheets are visible in this demo report.
### "Frontend" sheets


### "Backend" sheets
* *Config* - ASANA project IDs to be included in the report (columns `A:B`) and other setting and validation fields for the "frontend" sheets
* *Data* - Raw data imported using the python script and calculated columns (columns `J:Q`) using various formulas
* *Data Filtered* - Raw data filtered using the filtering criterias on the *Cost Overview* sheet (cells `E5`, `E6` and `E7`) for restricting the period and projects included in the analysis
* *Graph Data* - Raw data filtered using the filtering criteria on the *Cost Overview* sheet (cell `P10`) for restricting the projects displayed
* *Graph Data Summarized* - Pivot tables made from the *Graph Data* sheet data
