# SIH_Prototype\app\models.py

from pydantic import BaseModel


# -------- Tourist Models --------
class TouristPassRequest(BaseModel):
    name: str
    trip_days: int


class SafetyData(BaseModel):
    location: str
    heart_rate: int


class PanicAlert(BaseModel):
    tourist_id: str
    message: str


# -------- IoT (ESP32) Models --------
class IoTData(BaseModel):
    accel_x: float
    accel_y: float
    accel_z: float
