# app/models/sensor.py
from sqlalchemy import Column, BigInteger, DateTime, Integer, ForeignKey, DECIMAL, SmallInteger
from sqlalchemy.sql import func
from app.db import Base

class SensorData(Base):
    __tablename__ = "sensor_data"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    sensor_id = Column(Integer, nullable=True)  # 1-6 or null

class HumidityReading(Base):
    __tablename__ = "humidity_readings"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    sensor_data_id = Column(ForeignKey("sensor_data.id", ondelete="CASCADE"), nullable=False)
    value_index = Column(SmallInteger, nullable=False)
    value = Column(DECIMAL(5,2), nullable=False)

class TemperatureReading(Base):
    __tablename__ = "temperature_readings"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    sensor_data_id = Column(ForeignKey("sensor_data.id", ondelete="CASCADE"), nullable=False)
    value_index = Column(SmallInteger, nullable=False)
    value = Column(DECIMAL(5,2), nullable=False)

class ImpedanceReading(Base):
    __tablename__ = "impedance_readings"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    sensor_data_id = Column(ForeignKey("sensor_data.id", ondelete="CASCADE"), nullable=False)
    index = Column(SmallInteger, nullable=False)
    freq = Column(DECIMAL(7,2), nullable=False)
    reZ = Column(DECIMAL(7,2), nullable=False)
    imZ = Column(DECIMAL(7,2), nullable=False)
    magZ = Column(DECIMAL(7,2), nullable=False)
    phase = Column(DECIMAL(7,2), nullable=False)
