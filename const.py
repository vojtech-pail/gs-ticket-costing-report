import asana
import pygsheets
import pandas as pd

# General
DATE_PATTERN = "%d/%m/%Y"

# Indigo
DEVS_DF = pd.read_csv("dev_team.csv")  # fake IDs and names

# ASANA
PAT = '1/8493774615220093:938de73ca8aae7992018ce82d19eb9c8'  # fake ID
ASANA_CLIENT = asana.Client.access_token(PAT)
ASANA_CLIENT.headers = {'asana-enable': 'new_goal_memberships'}

TASK_EFFORT_GID = '190298362204723'  # fake ID
TASK_URGENCY_GID = '190177483927221'  # fake ID
TASK_ACCEPTANCE_GID = '189903729994965'  # fake ID
TASK_TICKET_TYPE_GID = '190277399277144'  # fake ID

# Google Sheets client
GS_CLIENT = pygsheets.authorize(
    service_file='path-to-json-file')  # not included here

# # Config Google sheet settings
GS_MASTER_GID = "gid-of-master-config-google-sheet"