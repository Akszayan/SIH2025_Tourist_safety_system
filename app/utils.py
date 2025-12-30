
# SIH_Prototype\app\models.py

import hashlib
import json
from datetime import datetime, timedelta

def create_tourist_pass(name, trip_days=5):
    expiry = datetime.utcnow() + timedelta(days=trip_days)
    pass_data = {
        "tourist_name": name,
        "trip_start": datetime.utcnow().isoformat(),
        "trip_end": expiry.isoformat(),
        "pass_id": hashlib.sha256(f"{name}{datetime.utcnow()}".encode()).hexdigest()
    }
    pass_hash = hashlib.sha256(json.dumps(pass_data).encode()).hexdigest()
    return pass_data, pass_hash

def calculate_safety_score(location, heart_rate):
    risk_zones = ["area51", "darkstreet"]
    score = 100
    if location in risk_zones:
        score -= 50
    if heart_rate > 120:
        score -= 20
    return max(score, 0)
