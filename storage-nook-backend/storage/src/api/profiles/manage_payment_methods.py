import json
import boto3
import os

dynamodb = boto3.resource("dynamodb")
profiles_table = dynamodb.Table(os.environ["TABLE_NAME"])


def lambda_handler(event, context):
    """
    Manage payment methods for a user.
    """
    try:
        body = json.loads(event["body"])
        user_id = body.get("userId")
        payment_method = body.get("paymentMethod")

        if not (user_id and payment_method):
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Missing required fields"}),
            }

        # Retrieve existing methods
        response = profiles_table.get_item(Key={"userId": user_id})
        profile = response.get("Item", {})
        payment_methods = profile.get("paymentMethods", [])

        # Add new method
        payment_methods.append(payment_method)
        profiles_table.update_item(
            Key={"userId": user_id},
            UpdateExpression="SET paymentMethods = :methods",
            ExpressionAttributeValues={":methods": payment_methods},
        )

        return {
            "statusCode": 200,
            "body": json.dumps({"message": "Payment method added"}),
        }

    except Exception as e:
        print(f"Error: {e}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "Internal server error"}),
        }
