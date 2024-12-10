import json
from moto import mock_dynamodb
import boto3
from datetime import datetime, timedelta
from uuid import uuid4
from lambda_function import lambda_handler, get_pricing_for_unit, calculate_price


@mock_dynamodb
def test_successful_booking_creation():
    # Set up mock DynamoDB
    dynamodb = boto3.resource("dynamodb", region_name="us-east-1")
    
    # Create tables
    bookings_table = dynamodb.create_table(
        TableName="BookingsTable",
        KeySchema=[{"AttributeName": "bookingId", "KeyType": "HASH"}],
        AttributeDefinitions=[{"AttributeName": "bookingId", "AttributeType": "S"}],
        ProvisionedThroughput={"ReadCapacityUnits": 5, "WriteCapacityUnits": 5},
    )
    units_table = dynamodb.create_table(
        TableName="UnitsTable",
        KeySchema=[{"AttributeName": "unitId", "KeyType": "HASH"}],
        AttributeDefinitions=[{"AttributeName": "unitId", "AttributeType": "S"}],
        ProvisionedThroughput={"ReadCapacityUnits": 5, "WriteCapacityUnits": 5},
    )
    bookings_table.meta.client.get_waiter("table_exists").wait(TableName="BookingsTable")
    units_table.meta.client.get_waiter("table_exists").wait(TableName="UnitsTable")
    
    # Add mock unit
    unit_id = str(uuid4())
    units_table.put_item(
        Item={
            "unitId": unit_id,
            "status": "Available",
            "pricing": {"perDay": "100", "perWeek": "600", "perMonth": "2000"},
        }
    )

    # Define test event
    event = {
        "body": json.dumps(
            {
                "customerId": "customer-123",
                "unitId": unit_id,
                "startDate": datetime.now().strftime("%Y-%m-%d"),
                "endDate": (datetime.now() + timedelta(days=10)).strftime("%Y-%m-%d"),
            }
        )
    }

    # Call the Lambda function
    response = lambda_handler(event, None)

    # Assert response
    assert response["statusCode"] == 201
    response_body = json.loads(response["body"])
    assert response_body["message"] == "Booking created successfully"
    assert "bookingId" in response_body


@mock_dynamodb
def test_missing_required_fields():
    # Define test event with missing fields
    event = {
        "body": json.dumps({"unitId": "unit-123", "startDate": "2024-01-01"})
    }

    # Call the Lambda function
    response = lambda_handler(event, None)

    # Assert response
    assert response["statusCode"] == 400
    assert "Missing required fields" in json.loads(response["body"])["error"]


@mock_dynamodb
def test_invalid_booking_duration():
    # Define test event with invalid duration
    event = {
        "body": json.dumps(
            {
                "customerId": "customer-123",
                "unitId": "unit-123",
                "startDate": "2024-01-01",
                "endDate": "2024-01-01",
            }
        )
    }

    # Call the Lambda function
    response = lambda_handler(event, None)

    # Assert response
    assert response["statusCode"] == 400
    assert "Invalid booking duration" in json.loads(response["body"])["error"]


@mock_dynamodb
def test_unit_not_available():
    # Set up mock DynamoDB
    dynamodb = boto3.resource("dynamodb", region_name="us-east-1")
    
    # Create UnitsTable
    units_table = dynamodb.create_table(
        TableName="UnitsTable",
        KeySchema=[{"AttributeName": "unitId", "KeyType": "HASH"}],
        AttributeDefinitions=[{"AttributeName": "unitId", "AttributeType": "S"}],
        ProvisionedThroughput={"ReadCapacityUnits": 5, "WriteCapacityUnits": 5},
    )
    units_table.meta.client.get_waiter("table_exists").wait(TableName="UnitsTable")
    
    # Add a unit that is not available
    units_table.put_item(
        Item={
            "unitId": "unit-123",
            "status": "Reserved",
            "pricing": {"perDay": "100", "perWeek": "600", "perMonth": "2000"},
        }
    )

    # Define test event
    event = {
        "body": json.dumps(
            {
                "customerId": "customer-123",
                "unitId": "unit-123",
                "startDate": "2024-01-01",
                "endDate": "2024-01-10",
            }
        )
    }

    # Call the Lambda function
    response = lambda_handler(event, None)

    # Assert response
    assert response["statusCode"] == 400
    assert "Unit unit-123 is not available" in json.loads(response["body"])["error"]


@mock_dynamodb
def test_internal_server_error(mocker):
    # Mock get_pricing_for_unit to raise an exception
    mocker.patch("lambda_function.get_pricing_for_unit", side_effect=Exception("Test error"))

    # Define test event
    event = {
        "body": json.dumps(
            {
                "customerId": "customer-123",
                "unitId": "unit-123",
                "startDate": "2024-01-01",
                "endDate": "2024-01-10",
            }
        )
    }

    # Call the Lambda function
    response = lambda_handler(event, None)

    # Assert response
    assert response["statusCode"] == 500
    assert "Internal server error" in json.loads(response["body"])["error"]
