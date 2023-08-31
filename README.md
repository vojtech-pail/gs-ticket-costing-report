# Analysis of ASANA tickets in Google Sheets
This is a demo* version of an analytical project, whose purpose was to provide a certain level of detail about ASANA tasks, that wasn't possible using the ASANA's built-in analytical features.
  
**The access tokens and GIDs were replaced with fake data and the content of the Google Sheet report was artificially generated.*

## The business need
The whole project evolved from the need to have a tool that could be used as a basis for invoicing our customers for support and developments tickets. These tickets were managed in ASANA and mixed with other tasks that were considered out-of-scope for the invoicing. Separation of the in-scope and out-of-scope tickets was not possible directly in ASANA and therefore it required custom approach. A task was considered in-scope if it was assigned to a member of development team in any point in time in the task's history.

## Overview of the solution
I have decided to use:
* ASANA's API to access the data of the tickets (using `asana` python library)
* Python to transform the data
* Google Sheets document for the tickets' analysis
* Google's API to insert the data to the Google Sheet document (using `pygsheets` python library)
* `cron` job to run the python script automatically and periodically

The whole solution was designed in a way that would allow making changes to the scope (adding new ASANA projects that should be part of the reports or removing old ones) without touching the python scripts. The same logic was followed in the area of financial aspects - the pricing model was developped directly in the Google Sheets report.

## Solution in detail
The following sections describe the solution in more detail.

### 1) Setting up access tokens for authentication with APIs
#### Google Cloud Platform
* Set up a project in Google Cloud Platform console and allow Google Sheets API
* Create service account that will edit the Google Sheet document
  * The document had to be shared with this account and (with editor rights)

#### ASANA
* Create Personal Access Token

*I have included the fake ASANA's PAT directly in the `const.py` file for the demonstration purposes only. The recommended solution is to have this secret stored in an environment variable.*

### 2) Extracting the list of developers
Extracting all the users of ASANA workspace using `users.get_users()` function and selecting only developers. The result was saved to the `dev_team.csv` file (only demo data here).

### 3) Setting up a configuration Google Sheet document
A configuration Google Sheet document was used to store information about different clients and reference to the final Google Sheet reports in the form of each report's GID (the GID of each report was added after the report structure was created).
![The columns of the config google sheet](/assets/config_clients_page.png "Config Google Sheet's columns")



