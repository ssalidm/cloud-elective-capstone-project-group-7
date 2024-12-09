import json
import boto3
import os
from boto3.dynamodb.conditions import Attr

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["TABLE_NAME"])


def lambda_handler(event, context):
    """
    Retrieve units filtered by location, status, storage type, and size.
    """
    try:
        # Extract query parameters
        query_params = event.get("queryStringParameters") or {}
        location = query_params.get("location")
        status = query_params.get("status")
        storage_type = query_params.get("type")
        size = query_params.get("size")

        # Perform a scan to get all items in the table
        response = table.scan()
        units = response.get("Items", [])

        # Apply filters dynamically based on provided parameters
        if location:
            units = [unit for unit in units if unit.get("location") == location]
        if status:
            units = [unit for unit in units if unit.get("status") == status]
        if storage_type:
            units = [unit for unit in units if unit.get("typeId") == storage_type]
        if size:
            units = [unit for unit in units if unit.get("size") == size]

        # Return filtered units
        return {
            "statusCode": 200,
            "body": json.dumps(units),
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET",
                "Access-Control-Allow-Headers": "Content-Type,Authorization",
            },
        }

    except Exception as e:
        print(f"Error: {e}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "Internal server error"}),
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET",
                "Access-Control-Allow-Headers": "Content-Type,Authorization",
            },
        }
