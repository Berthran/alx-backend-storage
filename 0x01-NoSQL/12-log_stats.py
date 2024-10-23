#!/usr/bin/env python3
'''
connects to Nginx server
'''
from pymongo import MongoClient


def main():
    '''
    connects to mongoDB
    '''
    # Connect to MongoDB
    # Update the URI if necessary
    client = MongoClient('mongodb://localhost:27017/')
    db = client.logs  # Access the logs database
    collection = db.nginx  # Access the nginx collection

    # Count total number of logs
    total_logs = collection.count_documents({})

    # Count for each method
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    method_counts = {method: collection.count_documents(
        {"method": method}) for method in methods}

    # Count GET requests to /status
    get_status_count = collection.count_documents(
        {"method": "GET", "path": "/status"})

    # Display results
    print(f"{total_logs} logs")
    print("Methods:")
    for method in methods:
        print(f"\tmethod {method}: {method_counts[method]}")

    # Print the count of GET requests to /status
    print(f"\tmethod GET: {get_status_count}")


if __name__ == "__main__":
    main()
