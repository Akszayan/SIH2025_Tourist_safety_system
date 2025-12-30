import sseclient
import json
import requests

# Firebase Realtime DB URL for SOS node
DATABASE_URL = "https://emergencyalerts-86bcf-default-rtdb.firebaseio.com/Emergency_SOS.json"
FASTAPI_URL = "http://10.188.183.234:8000/trigger_sos"  # replace with your FastAPI host

def listen_sos():
    print("👂 Listening for SOS alerts in realtime...\n")
    client = sseclient.SSEClient(DATABASE_URL)

    for event in client:
        if event.event == 'put':
            try:
                data = json.loads(event.data)
                sos_data = data.get("data", None)
                if sos_data == "1" or sos_data == 1:
                    print("🚨 SOS Button Pressed → alerting FastAPI")
                    try:
                        requests.post(FASTAPI_URL)
                    except Exception as e:
                        print("❌ Failed to notify FastAPI:", e)
            except Exception as e:
                print("❌ Error parsing event:", e)

if __name__ == "__main__":
    listen_sos()
