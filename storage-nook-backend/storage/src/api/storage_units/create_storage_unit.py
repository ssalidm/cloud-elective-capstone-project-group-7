import json
import boto3
import os
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource("dynamodb")
units_table = dynamodb.Table(os.environ["TABLE_NAME"])
types_table = dynamodb.Table(os.environ["STORAGE_TYPES_TABLE"])


def validate_storage_type(type_id):
    """
    Check if the given typeId exists in the StorageTypesTable.
    """
    response = types_table.get_item(Key={"typeId": type_id})
    return "Item" in response  # Returns True if typeId exists


def sanitize_location(location):
    """
    Convert the location string into a URL-friendly format.
    """
    return location.lower().replace(" ", "-")


def generate_unit_id(type_id, location, counter):
    """
    Generate a composite unitId.
    """
    sanitized_location = sanitize_location(location)
    return f"{type_id[:3]}-{sanitized_location}-{counter:03d}"


def get_existing_counters(type_id):
    """
    Retrieve all existing counters for a given typeId.
    """
    response = units_table.scan(
        FilterExpression="typeId = :type_id",
        ExpressionAttributeValues={":type_id": type_id},
    )

    # Create a dictionary of max counters by location
    existing_counters = {}
    for unit in response.get("Items", []):
        location = sanitize_location(unit["location"])
        try:
            counter = int(unit["unitId"].split("-")[-1])
            existing_counters[location] = max(
                existing_counters.get(location, 0), counter
            )
        except ValueError:
            continue

    return existing_counters


def lambda_handler(event, context):
    """
    Create units for a specific storage type.
    """
    try:
        claims = event["requestContext"]["authorizer"]["claims"]
        groups = claims.get("cognito:groups", [])
        if "admin" not in groups:
            return {
                "statusCode": 403,
                "body": json.dumps({"error": "Forbidden"}),
                "headers": {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
                    "Access-Control-Allow-Headers": "Content-Type,Authorization",
                },
            }

        # Extract typeId from the path
        type_id = event["pathParameters"]["typeId"]

        # Validate if the typeId exists
        if not validate_storage_type(type_id):
            return {
                "statusCode": 400,
                "body": json.dumps({"error": f"Storage type {type_id} does not exist"}),
                "headers": {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
                    "Access-Control-Allow-Headers": "Content-Type,Authorization,X-Amz-Date,X-Api-Key,X-Amz-Security-Token",
                },
            }

        # Parse the request body
        body = json.loads(event["body"])
        units = body.get("units", [])

        if not units:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "No units provided"}),
                "headers": {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
                    "Access-Control-Allow-Headers": "Content-Type,Authorization,X-Amz-Date,X-Api-Key,X-Amz-Security-Token",
                },
            }

        # Precompute unit IDs
        existing_counters = get_existing_counters(type_id)
        for unit in units:
            location = unit["location"]
            sanitized_location = sanitize_location(location)

            # Get the next counter for this location
            next_counter = existing_counters.get(sanitized_location, 0) + 1
            unit["unitId"] = generate_unit_id(type_id, location, next_counter)
            unit["typeId"] = type_id

            # Update the counter for this location
            existing_counters[sanitized_location] = next_counter

        # Save units to DynamoDB
        with units_table.batch_writer() as batch:
            for unit in units:
                batch.put_item(Item=unit)

        return {
            "statusCode": 201,
            "body": json.dumps({"message": "Units created successfully"}),
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type,Authorization,X-Amz-Date,X-Api-Key,X-Amz-Security-Token",
            },
        }

    except Exception as e:
        print(f"Error: {e}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "Internal server error"}),
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type,Authorization,X-Amz-Date,X-Api-Key,X-Amz-Security-Token",
            },
        }
