import datetime
import requests
from crm.models import Product


LOG_FILE = "/tmp/crm_heartbeat_log.txt"
GRAPHQL_ENDPOINT = "http://localhost:8000/graphql"


def log_crm_heartbeat():
    now = datetime.datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
    message = f"{now} CRM is alive"

    # Append log
    with open(LOG_FILE, "a") as f:
        f.write(message + "\n")

    try:
        query = {"query": "{ hello }"}
        response = requests.post(GRAPHQL_ENDPOINT, json=query)
        if response.status_code == 200:
            print(f"{now} - GraphQL OK: {response.json()}")
        else:
            print(f"{now} - GraphQL failed: {response.status_code}")
    except Exception as e:
        print(f"{now} - GraphQL error: {e}")

import os
import django
import logging
from datetime import datetime
from graphene.test import Client
import schema

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE", "project.settings"
) 
django.setup()

logger = logging.getLogger(__name__)


def update_low_stock():
    client = Client(schema)

    mutation = """
    mutation {
        updateLowStockProducts {
            updatedProducts {
                id
                name
                stock
            }
            message
        }
    }
    """

    result = client.execute(mutation)

    log_file = "/tmp/low_stock_updates_log.txt"
    with open(log_file, "a") as f:
        f.write(f"{datetime.now().strftime('%d/%m/%Y-%H:%M:%S')} - {result}\n")
