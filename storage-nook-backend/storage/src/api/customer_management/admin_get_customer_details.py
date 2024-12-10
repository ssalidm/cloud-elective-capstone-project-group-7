import json
import boto3
import os
from decimal import Decimal

# Initialize DynamoDB
dynamodb = boto3.resource("dynamodb")
profiles_table = dynamodb.Table(os.environ["PROFILES_TABLE"])
bookings_table = dynamodb.Table(os.environ["BOOKINGS_TABLE"])


def decimal_to_native(obj):
    """
    Recursively converts DynamoDB Decimals to native Python types.
    """
    if isinstance(obj, list):
        return [decimal_to_native(i) for i in obj]
    elif isinstance(obj, dict):
        return {key: decimal_to_native(value) for key, value in obj.items()}
    elif isinstance(obj, Decimal):
        if obj % 1 == 0:  # Check if it's a whole number
            return int(obj)
        return float(obj)
    else:
        return obj


def get_customer_profile(customer_id):
    """
    Retrieve customer profile from UserProfilesTable.
    """
    response = profiles_table.get_item(Key={"userId": customer_id})
    return response.get("Item")


def get_customer_bookings(customer_id):
    """
    Retrieve customer's booking history from BookingsTable.
    """
    response = bookings_table.query(
        IndexName="CustomerIndex",
        KeyConditionExpression="customerId = :customer_id",
        ExpressionAttributeValues={":customer_id": customer_id},
    )
    return response.get("Items", [])


def lambda_handler(event, context):
    """
    Admin endpoint to fetch customer details.
    """
    try:
        # Extract customerId from path parameters
        customer_id = event["pathParameters"]["customerId"]

        # Fetch customer profile
        profile = get_customer_profile(customer_id)
        if not profile:
            return {
                "statusCode": 404,
                "body": json.dumps({"error": "Customer not found"}),
                "headers": {
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Methods": "GET",
                    "Access-Control-Allow-Headers": "Content-Type,Authorization",
                },
            }

        # Fetch customer bookings
        bookings = get_customer_bookings(customer_id)

        # Combine results
        result = {
            "profile": decimal_to_native(profile),
            "bookings": decimal_to_native(bookings),
        }

        return {
            "statusCode": 200,
            "body": json.dumps(result),
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
