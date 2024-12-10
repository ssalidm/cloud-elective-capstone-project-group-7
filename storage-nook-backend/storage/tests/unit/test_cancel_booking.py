import json
from moto import mock_dynamodb
import boto3
from datetime import datetime, timedelta
from lambda_function import lambda_handler


def test_successful_cancellation():
    with mock_dynamodb():
        # Set up mock DynamoDB
        dynamodb = boto3.resource("dynamodb", region_name="us-east-1")
        
        # Create BookingsTable
        bookings_table = dynamodb.create_table(
            TableName="BookingsTable",
            KeySchema=[{"AttributeName": "bookingId", "KeyType": "HASH"}],
            AttributeDefinitions=[{"AttributeName": "bookingId", "AttributeType": "S"}],
            ProvisionedThroughput={"ReadCapacityUnits": 5, "WriteCapacityUnits": 5},
        )
        bookings_table.meta.client.get_waiter("table_exists").wait(TableName="BookingsTable")

        # Add mock booking
        bookings_table.put_item(
            Item={
                "bookingId": "test-booking",
                "endDate": (datetime.now() + timedelta(days=10)).strftime("%Y-%m-%d"),
                "noticePeriod": 7,
                "unitId": "unit-1",
                "typeId": "type-1",
            }
        )

        # Create UnitsTable
        units_table = dynamodb.create_table(
            TableName="UnitsTable",
            KeySchema=[
                {"AttributeName": "unitId", "KeyType": "HASH"},
                {"AttributeName": "typeId", "KeyType": "RANGE"},
            ],
            AttributeDefinitions=[
                {"AttributeName": "unitId", "AttributeType": "S"},
                {"AttributeName": "typeId", "AttributeType": "S"},
            ],
            ProvisionedThroughput={"ReadCapacityUnits": 5, "WriteCapacityUnits": 5},
        )
        units_table.meta.client.get_waiter("table_exists").wait(TableName="UnitsTable")

        # Add mock unit
        units_table.put_item(Item={"unitId": "unit-1", "typeId": "type-1", "status": "Available"})

        # Define test event
        event = {
            "pathParameters": {"bookingId": "test-booking"},
            "body": json.dumps({"cancellationDate": datetime.now().strftime("%Y-%m-%d")}),
        }

        # Call the function
        response = lambda_handler(event, None)

        # Assert response
        assert response["statusCode"] == 200
        assert json.loads(response["body"])["message"] == "Cancellation successful"
