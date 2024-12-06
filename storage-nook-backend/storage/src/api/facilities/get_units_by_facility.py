import json
import boto3
import os
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource("dynamodb")

TABLE_NAME = os.environ["TABLE_NAME"]


def lamdba_handler(event, context):
    """
    Retrieve units for a specific facility, optionally filtered by location.
    """
    try:
        facility_id = event["pathParameters"]["facilityId"]
        location = (
            event["queryStringParameters"].get("location")
            if event.get("queryStringParameters")
            else None
        )

        table = dynamodb.Table(TABLE_NAME)

        if location:
            response = table.query(
                IndexName="LocationIndex",
                KeyConditionExpression=Key("location").eq(location),
            )
        else:
            response = table.query(
                KeyConditionExpression=Key("facilityId").eq(facility_id)
            )

        units = response.get("Items", [])
        return {
            "statusCode": 200,
            "body": json.dumps(units),
            "headers": {
                "Content-Type": "application/json",
            },
        }
    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "Internal Server Error"}),
            "headers": {
                "Content-Type": "application/json",
            },
        }
