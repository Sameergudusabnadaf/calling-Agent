import os
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()

# Twilio Credentials from .env
account_sid = os.getenv('TWILIO_ACCOUNT_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')
from_number = os.getenv('TWILIO_PHONE_NUMBER') # You need to add this to .env
to_number = "+916360607023"

if not all([account_sid, auth_token, from_number, to_number]):
    print("Error: Missing credentials or phone numbers in .env")
    print(f"Required: ACCOUNT_SID, AUTH_TOKEN, TWILIO_PHONE_NUMBER")
    exit(1)

client = Client(account_sid, auth_token)

try:
    print(f"Initiating outbound call to {to_number}...")
    
    twiml_content = """<Response>
        <Say voice="Polly.Aditi" language="en-IN">Tomorrow, admission starts at G T T C Magadi. Please visit the college.</Say>
        <Pause length="1"/>
        <Say voice="Polly.Aditi" language="hi-IN">कल जी टी टी सी मागड़ी में एडमिशन शुरू हो रहा है। कृपया कॉलेज आएं।</Say>
        <Pause length="1"/>
        <Say voice="Polly.Aditi" language="en-IN">Naale G T T C magadi-yalli pravesha prarambha-vagalide. Dayavittu college-ge bheti needi.</Say>
    </Response>"""
    
    call = client.calls.create(
        to=to_number,
        from_=from_number,
        twiml=twiml_content
    )
    
    print(f"Call initiated! SID: {call.sid}")
except Exception as e:
    print(f"Failed to place call: {e}")
