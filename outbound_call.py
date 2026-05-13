import os
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()

# Twilio Credentials from .env
account_sid = os.getenv('TWILIO_ACCOUNT_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')
from_number = os.getenv('TWILIO_PHONE_NUMBER') # You need to add this to .env
to_number = "+916360607023"

# The SIP URI provided by LiveKit (e.g., sip:your-sip-trunk@sip.livekit.cloud)
sip_uri = os.getenv('LIVEKIT_SIP_URI') 

if not all([account_sid, auth_token, from_number, to_number]):
    print("Error: Missing credentials or phone numbers in .env")
    print(f"Required: ACCOUNT_SID, AUTH_TOKEN, TWILIO_PHONE_NUMBER")
    exit(1)

client = Client(account_sid, auth_token)

try:
    print(f"Initiating outbound call to {to_number}...")
    
    # We dial the phone number and connect it to the SIP URI
    # This effectively makes the AI agent 'call' the person
    call = client.calls.create(
        to=to_number,
        from_=from_number,
        url=f"http://twimlets.com/forward?PhoneNumber={sip_uri}" if sip_uri else None,
    )
    
    print(f"Call initiated! SID: {call.sid}")
except Exception as e:
    print(f"Failed to place call: {e}")

