import json
import boto3
import os
from boto3.dynamodb.conditions import Attr

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["TABLE_NAME"])


def lambda_handler(event, context):
    """
    Retrieve all units regardless of their type.
    """
    try:
        # Extract query parameters
        query_params = event.get('queryStringParameters') or {}
        location = query_params.get('location')
        status = query_params.get('status')
        
        # Perform a scan to get all items in the table
        response = table.scan()

        # Get the list of items (units)
        units = response.get("Items", [])
        
        # Apply filters if provided
        if location:
            units = [unit for unit in units if unit.get('location') == location]
        if status:
            units = [unit for unit in units if unit.get('status') == status]

        # Return the units
        return {
            "statusCode": 200,
            "body": json.dumps(units),
            "headers": {"Content-Type": "application/json"},
        }

    except Exception as e:
        print(f"Error: {e}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "Internal server error"}),
            "headers": {"Content-Type": "application/json"},
        }
