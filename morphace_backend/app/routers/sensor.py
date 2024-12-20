# app/routers/sensor.py
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import datetime
from app.db import get_db
from app.schemas.sensor import SensorDataCreate, SensorDataResponse
from app.models.sensor import SensorData, HumidityReading, TemperatureReading, ImpedanceReading
from app.models.user import User
from uuid import UUID

router = APIRouter(prefix="/users/{user_id}/sensor", tags=["Sensor Data"])

@router.post("/", response_model=SensorDataResponse)
def create_sensor_data(user_id: str, sensor_data: SensorDataCreate, db: Session = Depends(get_db)):
    # Validate user_id as UUID
    try:
        user_uuid = UUID(user_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid user UUID")

    user = db.query(User).filter(User.id == user_uuid).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Create main sensor_data record
    new_data = SensorData(
        user_id=user_uuid,
        timestamp=sensor_data.timestamp,
        sensor_id=sensor_data.sensor_id
    )
    db.add(new_data)
    db.flush()  # Get new_data.id

    # Insert humidity readings
    for i, val in enumerate(sensor_data.humidity):
        h = HumidityReading(sensor_data_id=new_data.id, value_index=i, value=val)
        db.add(h)

    # Insert temperature readings
    for i, val in enumerate(sensor_data.temperature):
        t = TemperatureReading(sensor_data_id=new_data.id, value_index=i, value=val)
        db.add(t)

    # Insert impedance readings
    length = len(sensor_data.impedance.freq)
    for i in range(length):
        imp = ImpedanceReading(
            sensor_data_id=new_data.id,
            index=i,
            freq=sensor_data.impedance.freq[i],
            reZ=sensor_data.impedance.reZ[i],
            imZ=sensor_data.impedance.imZ[i],
            magZ=sensor_data.impedance.magZ[i],
            phase=sensor_data.impedance.phase[i]
        )
        db.add(imp)

    db.commit()
    db.refresh(new_data)

    # Build response
    # Retrieve stored data to return in one response
    hum_vals = [h.value for h in db.query(HumidityReading).filter_by(sensor_data_id=new_data.id).order_by(HumidityReading.value_index).all()]
    temp_vals = [t.value for t in db.query(TemperatureReading).filter_by(sensor_data_id=new_data.id).order_by(TemperatureReading.value_index).all()]
    
    # For impedance, gather arrays:
    impedance_rows = db.query(ImpedanceReading).filter_by(sensor_data_id=new_data.id).order_by(ImpedanceReading.index).all()
    impedance_res = {
        "freq": [r.freq for r in impedance_rows],
        "reZ": [r.reZ for r in impedance_rows],
        "imZ": [r.imZ for r in impedance_rows],
        "magZ": [r.magZ for r in impedance_rows],
        "phase": [r.phase for r in impedance_rows]
    }

    return SensorDataResponse(
        id=new_data.id,
        timestamp=new_data.timestamp,
        sensor_id=new_data.sensor_id,
        user_id=str(new_data.user_id),
        humidity=hum_vals,
        temperature=temp_vals,
        impedance=impedance_res
    )

@router.get("/", response_model=List[SensorDataResponse])
def get_sensor_data(user_id: str, start: datetime, end: datetime, db: Session = Depends(get_db)):
    try:
        user_uuid = UUID(user_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid user UUID")

    user = db.query(User).filter(User.id == user_uuid).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    query = db.query(SensorData).filter(
        SensorData.user_id == user_uuid,
        SensorData.timestamp >= start,
        SensorData.timestamp <= end
    ).order_by(SensorData.timestamp)

    results = []
    for sd in query.all():
        hum_vals = [h.value for h in db.query(HumidityReading).filter_by(sensor_data_id=sd.id).order_by(HumidityReading.value_index).all()]
        temp_vals = [t.value for t in db.query(TemperatureReading).filter_by(sensor_data_id=sd.id).order_by(TemperatureReading.value_index).all()]
        imp_rows = db.query(ImpedanceReading).filter_by(sensor_data_id=sd.id).order_by(ImpedanceReading.index).all()
        imp_res = {
            "freq": [r.freq for r in imp_rows],
            "reZ": [r.reZ for r in imp_rows],
            "imZ": [r.imZ for r in imp_rows],
            "magZ": [r.magZ for r in imp_rows],
            "phase": [r.phase for r in imp_rows]
        }

        results.append(SensorDataResponse(
            id=sd.id,
            timestamp=sd.timestamp,
            sensor_id=sd.sensor_id,
            user_id=str(sd.user_id),
            humidity=hum_vals,
            temperature=temp_vals,
            impedance=imp_res
        ))

    return results
