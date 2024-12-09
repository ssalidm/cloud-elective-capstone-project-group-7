import json
import boto3
import os

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["TABLE_NAME"])


def lambda_handler(event, context):
    """
    Update the details of a specific storage unit.
    """
    try:
        # Extract unitId from path parameters
        unit_id = event["pathParameters"]["unitId"]

        # Check if the unit exists
        existing_item = table.get_item(Key={"unitId": unit_id})
        if "Item" not in existing_item:
            return {
                "statusCode": 404,
                "body": json.dumps({"error": "Unit not found"}),
                "headers": {
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Methods": "POST",
                    "Access-Control-Allow-Headers": "Content-Type,Authorization",
                },
            }

        # Parse the request body
        body = json.loads(event["body"])
        update_expressions = []
        expression_attribute_values = {}
        expression_attribute_names = {}

        # Build the update expression dynamically
        for key, value in body.items():
            # Handle reserved keywords
            if key in ["status", "type", "location"]:  # Reserved keywords
                expression_attribute_names[f"#{key}"] = key
                update_expressions.append(f"#{key} = :{key}")
            else:
                update_expressions.append(f"{key} = :{key}")
            expression_attribute_values[f":{key}"] = value

        if not update_expressions:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "No valid fields to update"}),
                "headers": {
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Methods": "POST",
                    "Access-Control-Allow-Headers": "Content-Type,Authorization",
                },
            }

        update_expression = "SET " + ", ".join(update_expressions)

        # Perform the update
        response = table.update_item(
            Key={"unitId": unit_id},
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_attribute_values,
            ExpressionAttributeNames=expression_attribute_names or None,
            ReturnValues="UPDATED_NEW",
        )

        return {
            "statusCode": 200,
            "body": json.dumps(
                {
                    "message": "Unit updated successfully",
                    "updatedFields": response.get("Attributes", {}),
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
