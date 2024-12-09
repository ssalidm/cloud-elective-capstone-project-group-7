import json
import boto3
import os

# Initialize DynamoDB resource
dynamodb = boto3.resource("dynamodb")
bookings_table = dynamodb.Table(os.environ["TABLE_NAME"])


def lambda_handler(event, context):
    """
    Retrieve bookings for the authenticated user.
    """
    try:
        # Extract the userId (customerId) from the request context
        claims = event["requestContext"]["authorizer"]["claims"]
        customer_id = claims.get("sub")  # Cognito assigns user ID to 'sub'

        if not customer_id:
            return {
                "statusCode": 403,
                "body": json.dumps({"error": "User is not authorized"}),
                "headers": {
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Methods": "GET",
                    "Access-Control-Allow-Headers": "Content-Type,Authorization",
                },
            }

        # Query the bookings table using the customerId
        response = bookings_table.query(
            IndexName="CustomerIndex",
            KeyConditionExpression=boto3.dynamodb.conditions.Key("customerId").eq(
                customer_id
            ),
        )

        # Return the list of bookings
        bookings = response.get("Items", [])
        return {
            "statusCode": 200,
            "body": json.dumps(bookings),
            "headers": {"Content-Type": "application/json"},
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
