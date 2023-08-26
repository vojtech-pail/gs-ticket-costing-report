import asana
import const
from dateutil import parser
import pandas as pd
import re


def get_tasks(asana_client: asana.Client, asana_id: str, project_name: str) -> pd.DataFrame:
    """
    This function is used to retrieve useful information for all ASANA task in a given project
    and return it as a pandas DataFrame.

    :param asana_client: The ASANA client object that is used to handle API calls.
    :param asana_id: The ID of ASANA project.
    :param project_name: The name of the project to be added as an identifier to the resulting DataFrame.
    :return: DataFrame object of relevant information for each task in a given project.
    """

    tasks = asana_client.tasks.get_tasks_for_project(asana_id, opt_fields=['gid', 'name', 'completed_at',
                                                                           'created_at', 'custom_fields'])
    list_tasks = []
    for task in tasks:
        dict_task = {}
        effort = 0
        urgency = None
        acceptance = None
        ticket_type = None

        # Loop through task's items and save only the relevant ones
        for item in task['custom_fields']:

            # Check whether the item is Effort
            if item['gid'] == const.TASK_EFFORT_GID:
                try:
                    effort = item['display_value']
                except KeyError:
                    pass

            # Check whether the item is Urgency
            elif item['gid'] == const.TASK_URGENCY_GID:
                try:
                    urgency = item['display_value']
                except KeyError:
                    pass

            # Check whether the item is Acceptance
            elif item['gid'] == const.TASK_ACCEPTANCE_GID:
                try:
                    acceptance = item['display_value']
                except KeyError:
                    pass

            # Check whether the item is Ticket Type
            elif item['gid'] == const.TASK_TICKET_TYPE_GID:
                try:
                    ticket_type = item['display_value']
                except KeyError:
                    pass

        dict_task['Project'] = project_name
        dict_task['Task ID'] = int(task['gid'])
        dict_task['Task name'] = task['name']
        dict_task['Created'] = '' if task['created_at'] is None \
            else parser.parse(task['created_at'][:10]).date()
        dict_task['Completed'] = '' if task['completed_at'] is None \
            else parser.parse(task['completed_at'][:10]).date()
        dict_task['Effort'] = 0 if pd.isna(effort) else float(effort)
        if urgency is None:
            dict_task['Urgency'] = "Medium"
        else:
            dict_task['Urgency'] = urgency
        dict_task['Acceptance'] = acceptance
        dict_task['Ticket type'] = ticket_type

        list_tasks.append(dict_task)

    return pd.DataFrame(list_tasks)


def get_task_assignees(task_id) -> list:
    """
    Gets list of all users who have been assigned to a given task.

    :param task_id: ASANA id of a task to check for the assignees.
    :return: The list of assignees.
    """
    stories = const.ASANA_CLIENT.stories.get_stories_for_task(str(task_id), opt_fields=['text', 'resource_subtype'])
    assignees = []

    # Iterate through the stories and save the information about who were the assignees
    for s in stories:
        if s['resource_subtype'] == 'assigned':
            assigned_to = re.search(r"[\w ]+ assigned to ([\w ]+)", s['text'])
            if assigned_to is not None:
                assignees.append(assigned_to.group(1))
    return assignees


def check_assignees_developers(assignees: list) -> int:
    """
    Checks whether there are any developers among the names passed as an argument.
    :param assignees: The list of names of a tasks assignees.
    :return: Number of developers who are among the assignees.
    """
    cnt = 0
    for i in assignees:
        if i in const.DEVS_DF['name'].values:
            cnt += 1
    return cnt


def assignees_per_task_information_list(task_id) -> list:
    """
    Gets number of developers who worked on a task in a list with the ASANA task's id
    :param task_id: ASANA id of a task
    :return: ASANA id of the task and number of developers whom the task has been assigned to
    """
    assignees = get_task_assignees(task_id)
    devs_assignees_count = check_assignees_developers(assignees)

    return [task_id, devs_assignees_count]



