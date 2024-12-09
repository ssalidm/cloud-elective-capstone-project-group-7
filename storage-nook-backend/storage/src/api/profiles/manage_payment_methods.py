import json
import boto3
import os
from uuid import uuid4

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["TABLE_NAME"])


def lambda_handler(event, context):
    try:
        # Get user details from the token
        claims = event["requestContext"]["authorizer"]["claims"]
        user_id = claims["sub"]

        body = json.loads(event["body"])
        # user_id = event["pathParameters"]["userId"]
        payment_method = body.get("paymentMethod")

        if (
            not payment_method
            or "type" not in payment_method
            or "details" not in payment_method
        ):
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Invalid payment method data"}),
                "headers": {
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Methods": "POST",
                    "Access-Control-Allow-Headers": "Content-Type,Authorization",
                },
            }

        payment_method["methodId"] = str(uuid4())

        response = table.update_item(
            Key={"userId": user_id},
            UpdateExpression="SET paymentMethods = list_append(if_not_exists(paymentMethods, :empty_list), :new_method)",
            ExpressionAttributeValues={
                ":new_method": [payment_method],
                ":empty_list": [],
            },
            ReturnValues="UPDATED_NEW",
        )

        return {
            "statusCode": 201,
            "body": json.dumps(
                {
                    "message": "Payment method added successfully",
                    "paymentMethods": response["Attributes"].get("paymentMethods", []),
                }
            ),
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "POST",
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
                "Access-Control-Allow-Methods": "POST",
                "Access-Control-Allow-Headers": "Content-Type,Authorization",
            },
        }
