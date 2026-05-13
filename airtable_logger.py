import os
import datetime
from pyairtable import Table
from dotenv import load_dotenv

load_dotenv()

class AirtableLogger:
    def __init__(self):
        token = os.getenv("AIRTABLE_TOKEN")
        base_id = os.getenv("AIRTABLE_BASE_ID")
        table_name = os.getenv("AIRTABLE_TABLE_NAME", "CallLogs")

        if all([token, base_id, table_name]):
            self.table = Table(token, base_id, table_name)
        else:
            print("Airtable configuration missing. Logging disabled.")
            self.table = None

    def log_call(self, caller_number, duration, transcript):
        if not self.table:
            return

        try:
            self.table.create({
                "Caller Number": str(caller_number),
                "Duration": f"{duration}s",
                "Transcript": transcript,
                "Timestamp": datetime.datetime.now().isoformat()
            })
            print(f"Call logged to Airtable for {caller_number}")
        except Exception as e:
            print(f"Failed to log call to Airtable: {e}")

if __name__ == "__main__":
    # Test script
    logger = AirtableLogger()
    logger.log_call("+1234567890", 120, "Test transcript for Flora assistant.")
