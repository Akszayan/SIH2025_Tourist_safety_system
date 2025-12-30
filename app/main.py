from fastapi import FastAPI, WebSocket
from pydantic import BaseModel
import math
from .utils import create_tourist_pass, calculate_safety_score

app = FastAPI()

# In-memory store
passes = {}
iot_data_store = []

# Global buzzer flag
force_buzzer = False


# ---------------- Tourist Pass APIs ----------------
class TouristPassRequest(BaseModel):
    name: str
    trip_days: int = 5


class SafetyData(BaseModel):
    location: str
    heart_rate: int


class PanicAlert(BaseModel):
    tourist_id: str
    message: str


# ---------------- IoT Data Model ----------------
class IoTData(BaseModel):
    accel_x: float
    accel_y: float
    accel_z: float
    gyro_x: float
    gyro_y: float
    gyro_z: float


@app.post("/create_pass")
def create_pass(request: TouristPassRequest):
    data, hash_ = create_tourist_pass(request.name, request.trip_days)
    passes[hash_] = data
    return {"pass_data": data, "hash": hash_}


@app.post("/verify_pass/{pass_hash}")
def verify_pass(pass_hash: str):
    if pass_hash in passes:
        return {"valid": True, "pass_data": passes[pass_hash]}
    return {"valid": False}


# ---------------- Panic Alert ----------------
@app.post("/panic")
def panic_alert(alert: PanicAlert):
    print(f"🚨 PANIC ALERT from {alert.tourist_id}: {alert.message}")
    return {"status": "alert received"}


# ---------------- WebSocket Safety Monitoring ----------------
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_json()
        score = calculate_safety_score(data["location"], data["heart_rate"])
        await websocket.send_json({"score": score})


# ---------------- IoT (ESP32 Accelerometer + Gyro) ----------------
@app.post("/iot_data")
def receive_data(data: IoTData):
    global force_buzzer

    # Save data for viewing
    iot_data_store.append(data.dict())
    print(f"📥 Received from ESP32: {data.dict()}")

    # ---- Position + Fall Detection ----
    # Magnitude of acceleration vector
    accel_mag = math.sqrt(data.accel_x**2 + data.accel_y**2 + data.accel_z**2)

    # Angle with respect to gravity (Z-axis)
    if accel_mag != 0:
        tilt_angle = math.degrees(math.acos(data.accel_z / accel_mag))
    else:
        tilt_angle = 0

    # Anomaly rules
    alert = (
        accel_mag < 0.5            # near free-fall
        or accel_mag > 2.5         # sudden impact
        or tilt_angle > 60         # lying down / flipped
        or abs(data.gyro_x) > 200  # fast rotation
        or abs(data.gyro_y) > 200
        or abs(data.gyro_z) > 200
    )

    response = {
        "status": "ok",
        "alert": alert,
        "accel_mag": round(accel_mag, 2),
        "tilt_angle": round(tilt_angle, 2),
    }

    # Include manual trigger if set
    if force_buzzer:
        response["force_buzzer"] = True
        force_buzzer = False

    print(f"📤 Sending to ESP32: {response}")
    return response


# ---------------- Manual Trigger Endpoint ----------------
@app.post("/trigger_buzzer")
def trigger_buzzer():
    global force_buzzer
    force_buzzer = True
    print("⚡ Force buzzer trigger set for next ESP32 poll")
    return {"status": "buzzer will trigger on next ESP32 request"}


# ---------------- View All IoT Data ----------------
@app.get("/iot_data/all")
def get_all_iot_data():
    return {"iot_data": iot_data_store}


# ---------------- Root ----------------
@app.get("/")
def root():
    return {"message": "SIH Prototype Backend (ESP32 + Tourist Safety) 🚀"}
