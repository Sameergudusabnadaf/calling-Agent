import os
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()

# Twilio Credentials from .env
account_sid = os.getenv('TWILIO_ACCOUNT_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')
from_number = os.getenv('TWILIO_PHONE_NUMBER')

# List of numbers to call
to_numbers = ["+918088324492"]

if not all([account_sid, auth_token, from_number]):
    print("Error: Missing credentials in .env")
    exit(1)

client = Client(account_sid, auth_token)

# TwiML to just say "hello"
twiml_content = """<Response>
    <Say voice="alice" language="en-US">Hello!</Say>
</Response>"""

for number in to_numbers:
    try:
        print(f"Initiating outbound call to {number}...")
        
        call = client.calls.create(
            to=number,
            from_=from_number,
            twiml=twiml_content
        )
        
        print(f"Call initiated to {number}! SID: {call.sid}")
    except Exception as e:
        print(f"Failed to place call to {number}: {e}")
