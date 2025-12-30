# read_realtime_sos.py
import firebase_admin
from firebase_admin import credentials, db

# 1) Path to the service account JSON your friend gave you:
SERVICE_ACCOUNT = "serviceAccountKey.json"

# 2) Realtime DB URL you copied:
DATABASE_URL = "https://your-project-id-default-rtdb.firebaseio.com/"

cred = credentials.Certificate(SERVICE_ACCOUNT)
firebase_admin.initialize_app(cred, {
    "databaseURL": DATABASE_URL
})

# 3) Reference the SOS node (use the exact path from the console)
ref = db.reference("SOS")   # or db.reference("alerts/users")
data = ref.get()            # returns a dict (or None if empty)

print("Raw SOS data:", data)
# Example: iterate
if data:
    for key, sos in data.items():
        print(key, sos)   # sos likely a dict: { "lat":..., "lng":..., "time":... }
