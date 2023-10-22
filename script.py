import requests
from string import Template
from dotenv import load_dotenv
import os
import yaml
import sys

load_dotenv()
 
if len(sys.argv) == 1:
    print('Please provide the cadence of the issues to automate.')
    sys.exit()

cadence = sys.argv[1]
linear_url = os.getenv('LINEAR_URL')
authorization = os.getenv('AUTHORIZATION')
team_id = os.getenv('TEAM_ID')
todo_state_id = os.getenv('TODO_STATE_ID')
backlog_state_id = os.getenv('BACKLOG_STATE_ID')
headers = { 'Authorization': authorization, 'Content-Type': 'application/json' }

if cadence == 'weekly' or cadence == 'monthly':
    with open('issues.yaml', 'r') as file:
        yaml_data = file.read()
    issues = yaml.safe_load(yaml_data)[cadence]
    print(issues)

    for issue in issues:
        title = issue['title']

        if 'description' not in issue:
            description = ''
        else:
            description = issue['description']

        state = issue['state']
        if state == 'Todo':
            state = todo_state_id
        elif state == 'Backlog':
            state = backlog_state_id
        else:
            state = ''

        print(title)
        print(description)
        print(state)

        # get_issue_by_id = '{"query": "{ issue(id: \\"LIF-33\\") { id title description } }"}'
        # get_team_id = '{"query": "{ teams { nodes { id name } } }"}'
        # get_state_id = '{"query": "{ workflowStates { nodes { id name } } }"}'
        create_issue = Template('{"query": "mutation { issueCreate(input: { title: \\"${title}\\" description: \\"${description}\\" teamId: \\"${team_id}\\" stateId: \\"${state_id}\\"}) { success issue { id title } } }"}').substitute(title=title, description=description, team_id=team_id, state_id=state)

        response = requests.post(url=linear_url, headers=headers, data=create_issue)
        print(response.content.decode('utf-8'))
else:
    print('Please provide a valid cadence. Valid cadences are weekly and monthly.')
    sys.exit()