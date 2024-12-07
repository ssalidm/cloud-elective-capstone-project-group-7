import json
import logging
import random

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Mock function to simulate Credit Card payment
def process_credit_card_payment(card_number, expiry_date, cvv, amount):
    # Simulate a random success or failure based on dummy data
    logger.info(f"Processing credit card payment for {card_number[-4:]} with amount ${amount}...")
    success = random.choice([True, False])  # Randomly decide success or failure
    if success:
        transaction_id = f"CC{random.randint(1000, 9999)}"
        return {"status": "success", "transaction_id": transaction_id}
    else:
        return {"status": "failure", "message": "Card declined or invalid"}

# Mock function to simulate EFT payment
def process_eft_payment(bank_account, amount):
    # Simulate a random success or failure based on dummy data
    logger.info(f"Processing EFT payment from account {bank_account} with amount ${amount}...")
    success = random.choice([True, False])  # Randomly decide success or failure
    if success:
        transaction_id = f"EFT{random.randint(1000, 9999)}"
        return {"status": "success", "transaction_id": transaction_id}
    else:
        return {"status": "failure", "message": "Insufficient funds or invalid account"}

# Main Lambda handler function
def lambda_handler(event, context):
    try:
        # Extract payment details from event
        payment_method = event.get("payment_method")
        amount = event.get("amount")
        
        if not amount or amount <= 0:
            return {"statusCode": 400, "body": json.dumps({"message": "Invalid payment amount"})}

        # Process credit card payment
        if payment_method == "credit_card":
            card_number = event.get("card_number")
            expiry_date = event.get("expiry_date")
            cvv = event.get("cvv")
            
            # Validate Credit Card details (basic example)
            if not card_number or not expiry_date or not cvv:
                return {"statusCode": 400, "body": json.dumps({"message": "Missing credit card details"})}
            
            # Call the function to process credit card payment
            result = process_credit_card_payment(card_number, expiry_date, cvv, amount)
        
        # Process EFT payment
        elif payment_method == "eft":
            bank_account = event.get("bank_account")
            
            # Validate EFT details (basic example)
            if not bank_account:
                return {"statusCode": 400, "body": json.dumps({"message": "Missing bank account details"})}
            
            # Call the function to process EFT payment
            result = process_eft_payment(bank_account, amount)
        
        else:
            return {"statusCode": 400, "body": json.dumps({"message": "Unsupported payment method"})}

        # Return payment response based on result
        if result["status"] == "success":
            return {
                "statusCode": 200,
                "body": json.dumps({"message": "Payment successful", "transaction_id": result["transaction_id"]})
            }
        else:
            return {"statusCode": 500, "body": json.dumps({"message": result["message"]})}
    
    except Exception as e:
        logger.error(f"Error processing payment: {str(e)}")
        return {"statusCode": 500, "body": json.dumps({"message": "Internal server error"})}
