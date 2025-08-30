import datetime
import requests

LOG_FILE = "/tmp/crm_heartbeat_log.txt"
GRAPHQL_ENDPOINT = "http://localhost:8000/graphql"


def log_crm_heartbeat():
    now = datetime.datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
    message = f"{now} CRM is alive"

    with open(LOG_FILE, "a") as f:
        f.write(message + "\n")

    try:
        query = {"query": "{ hello }"}
        response = requests.post(GRAPHQL_ENDPOINT, json=query)
        if response.status_code == 200:
            print(f"{now} - Heartbeat OK, GraphQL says: {response.json()}")
        else:
            print(f"{now} - GraphQL endpoint not healthy: {response.status_code}")
    except Exception as e:
        print(f"{now} - Error reaching GraphQL: {e}")
