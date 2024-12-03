import json
import boto3
import uuid

# Initialize DynamoDB client
dynamodb = boto3.resource("dynamodb")

TABLE_NAME = "FacilitiesTable"


def lambda_handler(event, context):
    """
    Adds a new facility to the DynamoDB table.
    """
    try:
        # Parse the request body
        body = json.loads(event["body"])
        facility_id = str(uuid.uuid4())  # Generate a unique facility ID

        # Validate required fields
        if not all(key in body for key in ("name", "size", "location", "address")):
            return {
                "statusCode": 400,
                "body": json.dumps(
                    {
                        "error": "Missing some or all required fields: name, size, location, address"
                    }
                ),
                "headers": {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*",
                },
            }

        # Prepare the facility data
        facility_data = {
            "facilityId": facility_id,
            "name": body["name"],
            "size": body["size"],
            "location": body["location"],
            "address": body["address"],
            "description": body.get("description", ""),
            "available": False,  # New facilities are initially marked as unavailable,
        }

        # Add the facility to the DynamoDB table
        table = dynamodb.Table(TABLE_NAME)
        table.put_item(Item=facility_data)

        # Return a success response
        return {
            "statusCode": 201,
            "body": json.dumps(
                {"message": "Facility added successfully", "facilityId": facility_id}
            ),
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
            },
        }

    except Exception as e:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": str(e)}),
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
            },
        }
