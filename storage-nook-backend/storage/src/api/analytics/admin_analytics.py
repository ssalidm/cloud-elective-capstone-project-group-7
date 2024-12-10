import json
import boto3
import os
from boto3.dynamodb.conditions import Attr
from decimal import Decimal

dynamodb = boto3.resource("dynamodb")
bookings_table = dynamodb.Table(os.environ["BOOKINGS_TABLE"])
units_table = dynamodb.Table(os.environ["UNITS_TABLE"])


def decimal_to_native(obj):
    """
    Convert DynamoDB Decimal objects to Python native types.
    """
    if isinstance(obj, list):
        return [decimal_to_native(i) for i in obj]
    elif isinstance(obj, dict):
        return {key: decimal_to_native(value) for key, value in obj.items()}
    elif isinstance(obj, Decimal):
        if obj % 1 == 0:
            return int(obj)
        return float(obj)
    else:
        return obj


def safe_float(value):
    """
    Safely convert a value to float.
    """
    try:
        return float(value)
    except (ValueError, TypeError):
        return 0.0


def lambda_handler(event, context):
    """
    Get financial and occupancy analytics for admin.
    """
    try:
        # Handle preflight (OPTIONS) requests
        if event["httpMethod"] == "OPTIONS":
            return {
                "statusCode": 200,
                "headers": {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
                    "Access-Control-Allow-Headers": "Content-Type,Authorization",
                },
                "body": json.dumps({"message": "CORS preflight response"}),
            }

        # Verify admin group
        claims = event["requestContext"]["authorizer"]["claims"]
        groups = claims.get("cognito:groups", [])
        if "admin" not in groups:
            return {
                "statusCode": 403,
                "body": json.dumps({"error": "Forbidden"}),
                "headers": {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*",
                },
            }

        # Calculate total revenue
        response = bookings_table.scan(FilterExpression=Attr("paymentStatus").eq("Paid"))
        bookings = response.get("Items", [])
        bookings = decimal_to_native(bookings)
        total_revenue = sum(safe_float(booking.get("totalPrice", 0)) for booking in bookings)

        # Calculate number of bookings
        number_of_bookings = len(bookings)

        # Calculate occupancy percentage
        response = units_table.scan()
        units = response.get("Items", [])
        units = decimal_to_native(units)
        total_units = len(units)
        occupied_units = len(
            [
                unit
                for unit in units
                if unit.get("status") in ["Reserved", "Unavailable"]
            ]
        )
        occupancy_percentage = (
            (occupied_units / total_units) * 100 if total_units > 0 else 0
        )

        # Prepare analytics response
        analytics = {
            "totalRevenue": round(total_revenue, 2),
            "numberOfBookings": number_of_bookings,
            "occupancyPercentage": round(occupancy_percentage, 2),
        }

        return {
            "statusCode": 200,
            "body": json.dumps(analytics),
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type,Authorization",
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
                "Access-Control-Allow-Headers": "Content-Type,Authorization",
            },
        }
