import json
import boto3
import os

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["TABLE_NAME"])


def extract_type_id_from_unit_id(unit_id):
    """
    Extract the typeId from the unitId.
    """
    return unit_id.split("-")[0]


def lambda_handler(event, context):
    """
    Update the details of a specific storage unit.
    """
    try:
        # Extract unitId from path parameters
        unit_id = event["pathParameters"]["unitId"]

        # Extract typeId dynamically from unitId
        type_id = extract_type_id_from_unit_id(unit_id)

        # Parse the request body
        body = json.loads(event["body"])
        update_expressions = []
        expression_attribute_values = {}
        expression_attribute_names = {}

        # Build the update expression dynamically
        for key, value in body.items():
            # Handle reserved keywords
            if key in [
                "status",
                "type",
                "location",
            ]:  # Add other reserved keywords here
                expression_attribute_names[f"#{key}"] = key
                update_expressions.append(f"#{key} = :{key}")
            else:
                update_expressions.append(f"{key} = :{key}")
            expression_attribute_values[f":{key}"] = value

        if not update_expressions:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "No valid fields to update"}),
                "headers": {"Content-Type": "application/json"},
            }

        update_expression = "SET " + ", ".join(update_expressions)

        # Perform the update
        table.update_item(
            Key={"unitId": unit_id, "typeId": type_id},
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_attribute_values,
            ExpressionAttributeNames=expression_attribute_names or None,
        )

        return {
            "statusCode": 200,
            "body": json.dumps({"message": "Unit updated successfully"}),
            "headers": {"Content-Type": "application/json"},
        }

    except Exception as e:
        print(f"Error: {e}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "Internal server error"}),
            "headers": {"Content-Type": "application/json"},
        }
