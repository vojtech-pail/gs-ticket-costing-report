# Analysis of ASANA tickets in Google Sheets
This is a modified version of an analytical project, whose purpose was to provide a certain level of detail about ASANA tasks, that wasn't possible using the ASANA's built-in analytical features.
  
*The access tokens, gids of individual elements and content of the Google Sheet report was anonymized and is fully fictional.*

## The business need
The whole project evolved from the need to have a tool that could be used as a basis for invoicing our customers for support and developments tickets. These tickets were managed in ASANA and mixed with other tasks that were considered out-of-scope for the invoicing tool. Separation of the in-scope and out-of-scope tickets was not possible directly in ASANA and therefore it required custom tool.

## Overview of the solution
I have decided to use:
* ASANA's API to access the data of the tickets (using `asana` python library)
* Python to transform the data
* Google Sheets document for the tickets' analysis
* Google's API to insert the data to the Google Sheet document (using `pygsheets` python library)
* `cron` job to run the python script automatically and periodically

## Solution in detail
