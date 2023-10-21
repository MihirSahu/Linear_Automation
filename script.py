import requests
from string import Template
from dotenv import load_dotenv
import os

load_dotenv()

linear_url = os.getenv('LINEAR_URL')
authorization = os.getenv('AUTHORIZATION')
team_id = os.getenv('TEAM_ID')
state_id = os.getenv('STATE_ID')

headers = { 'Authorization': authorization, 'Content-Type': 'application/json' }

# get_issue_by_id = '{"query": "{ issue(id: \\"LIF-33\\") { id title description } }"}'
# get_team_id = '{"query": "{ teams { nodes { id name } } }"}'
# get_state_id = '{"query": "{ workflowStates { nodes { id name } } }"}'
create_issue = Template('{"query": "mutation { issueCreate(input: { title: \\"${title}\\" description: \\"${description}\\" teamId: \\"${team_id}\\" stateId: \\"${state_id}\\"}) { success issue { id title } } }"}').substitute(title="Test title", description="Test description", team_id=team_id, state_id=state_id)

response = requests.post(url=linear_url, headers=headers, data=create_issue)
print(response.content.decode('utf-8'))