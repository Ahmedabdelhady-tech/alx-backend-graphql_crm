#!/usr/bin/env python3
import sys
import logging
from datetime import datetime, timedelta

from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

# إعداد اللوج
LOG_FILE = "/tmp/order_reminders_log.txt"
logging.basicConfig(filename=LOG_FILE, level=logging.INFO)


def main():
    # إعداد GraphQL transport
    transport = RequestsHTTPTransport(
        url="http://localhost:8000/graphql",
        verify=True,
        retries=3,
    )

    client = Client(transport=transport, fetch_schema_from_transport=True)

    last_week = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")

    # GraphQL query
    query = gql(
        """
        query GetRecentOrders($lastWeek: Date!) {
            orders(orderDate_Gte: $lastWeek, status: "PENDING") {
                id
                customer {
                    email
                }
            }
        }
        """
    )

    params = {"lastWeek": last_week}

    try:
        result = client.execute(query, variable_values=params)
        orders = result.get("orders", [])

        for order in orders:
            msg = f"{datetime.now()} - Reminder for Order ID: {order['id']}, Customer Email: {order['customer']['email']}"
            logging.info(msg)

        print("Order reminders processed!")

    except Exception as e:
        logging.error(f"{datetime.now()} - Error: {str(e)}")
        print("Failed to process reminders", file=sys.stderr)


if __name__ == "__main__":
    main()
