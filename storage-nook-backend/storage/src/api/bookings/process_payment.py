import json
import boto3
import os

dynamodb = boto3.resource("dynamodb")
bookings_table = dynamodb.Table(os.environ["BOOKINGS_TABLE"])
profiles_table = dynamodb.Table(os.environ["PROFILES_TABLE"])

def lambda_handler(event, context):
    try:
        # Get user details from the token
        claims = event["requestContext"]["authorizer"]["claims"]
        user_id = claims["sub"]
        
        body = json.loads(event["body"])
        booking_id = event["pathParameters"]["bookingId"]
        payment_method_type = body.get("paymentMethodType")

        if not (user_id and payment_method_type):
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Missing userId or paymentMethodType"}),
            }

        # Fetch user profile
        profile = profiles_table.get_item(Key={"userId": user_id}).get("Item")
        if not profile:
            return {
                "statusCode": 404,
                "body": json.dumps({"error": "User not found"}),
            }

        # Find payment method
        payment_methods = profile.get("paymentMethods", [])
        payment_method = next((pm for pm in payment_methods if pm["type"] == payment_method_type), None)
        if not payment_method:
            return {
                "statusCode": 404,
                "body": json.dumps({"error": "Payment method not found"}),
            }

        # Fetch booking
        booking = bookings_table.get_item(Key={"bookingId": booking_id}).get("Item")
        if not booking:
            return {
                "statusCode": 404,
                "body": json.dumps({"error": "Booking not found"}),
            }

        # Simulate payment
        if booking["paymentStatus"] == "Paid":
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Booking is already paid"}),
            }

        booking["status"] = "Paid"

        # Update booking status
        bookings_table.update_item(
            Key={"bookingId": booking_id},
            UpdateExpression="SET paymentStatus = :status",
            # ExpressionAttributeNames={"#status": "status"},
            ExpressionAttributeValues={":status": "Paid"},
        )

        return {
            "statusCode": 200,
            "body": json.dumps({"message": "Payment successful", "paymentMethod": payment_method}),
        }

    except Exception as e:
        print(f"Error: {e}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "Internal server error"}),
        }
