import functions
import const
import pandas as pd
import datetime as dt
from dateutil.relativedelta import relativedelta

# Initialize date variables
today = dt.date.today()
today_formatted = today.strftime(const.DATE_PATTERN)

period_end = today.replace(day=1) - relativedelta(days=1)
period_end_formatted = period_end.strftime(const.DATE_PATTERN)
period_start = period_end.replace(day=1)
period_start_formatted = period_start.strftime(const.DATE_PATTERN)

# Initialize log file that will store information during the script runtime
log = [f"Start: {dt.datetime.now()}", ""]

# Load the list of ASANA resources for developers
devs_df = pd.read_csv("dev_team.csv")

# Get data about clients and the Google Sheets GIDs from master config Google sheet
gs = const.GS_CLIENT.open_by_key(const.GS_MASTER_GID)
ws = gs.worksheet_by_title('Clients')
master_client_list = ws.get_all_records()

# Iterate over all clients' Google Sheets reports
for client in master_client_list:

    # Save the client's name to the log
    log.append(f"Client: {client['Client']}")

    # Connect to Ticket Costing Google sheet and prepare the data sheet
    gs = const.GS_CLIENT.open_by_key(client['Report GID'])
    ws = gs.worksheet_by_title('Config')
    asana_projects_list = ws.get_values('A2', 'B100', returnas='matrix')
    ws = gs.worksheet_by_title('Data')
    ws.clear(start='A2', end='I'+str(ws.rows))

    # Iterate through each project found in the Config sheet of a client's report
    rows_inserted = 0
    for project in asana_projects_list:

        # Get relevant information about tasks of the project
        df_tasks = functions.get_tasks(const.ASANA_CLIENT, str(project[0]), project[1])
        assignees_l = []

        # Find tasks' assignees
        for index, row in df_tasks.iterrows():
            assignees_l.append(functions.assignees_per_task_information_list(row['Task ID']))

        # Join tasks DataFrame with assignees
        assignees_df = pd.DataFrame(data=assignees_l, columns=['Task ID', 'Assignees'])
        df_tasks = df_tasks.merge(assignees_df, on='Task ID', how='left')

        # Write dataframe to client's google sheet
        if not df_tasks.empty:
            # The Task ID column is not needed in the Google Sheet report, therefore it is dropped
            df_tasks.drop(columns={'Task ID'}, inplace=True)

            gs = const.GS_CLIENT.open_by_key(client['Report GID'])
            ws = gs.worksheet_by_title('Data')
            ws.set_dataframe(df_tasks, start='A'+str(rows_inserted + 3), copy_head=False, extend=True, nan='')

            df_tasks_len = len(df_tasks.index)
            rows_inserted += df_tasks_len
            log.append("   [" + dt.datetime.strftime(dt.datetime.now(), '%Y-%m-%d %H:%M:%S') + "] " + project[1] +
                       " - tasks inserted: " + str(df_tasks_len))

    # Add empty line after each client
    log.append("")

    """
    Routine after all tasks have been inserted to google sheets:
      1) Data is added from the third row in order to keep the ARRAYFORMULA functions (columns J to Q) unchanged.
      Therefore 2nd row is empty and needs to be deleted.
      2) Update reporting, comparison and data refresh dates
    """
    # Routine 1)
    gs = const.GS_CLIENT.open_by_key(client['Report GID'])
    ws = gs.worksheet_by_title('Data')
    ws.delete_rows(2)

    # Routine 2)
    date_cell = gs.worksheet_by_title('Cost Overview').cell('E5')
    date_cell.set_value(period_start_formatted)
    date_cell = gs.worksheet_by_title('Cost Overview').cell('E6')
    date_cell.set_value(period_end_formatted)
    date_cell = gs.worksheet_by_title('Cost Overview').cell('J2')
    date_cell.set_value(today_formatted)

# Update confing file - insert log
gs = const.GS_CLIENT.open_by_key(const.GS_MASTER_GID)
ws = gs.worksheet_by_title('Log')
ws.clear()
ws.set_dataframe(pd.DataFrame(log), start='A1', copy_head=False, extend=True)
