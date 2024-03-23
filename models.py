from sqlalchemy import ARRAY, Column, Float, Integer, String, DateTime, Boolean
import database as _database

class WaterQualityObservationDB(_database.Base):
    __tablename__ = 'observations'

    id = Column(Integer, primary_key=True, autoincrement=True)
    latitude = Column(Float)
    longitude = Column(Float)
    date_time = Column(String)
    description = Column(String)
    pH = Column(Float)
    conductivity = Column(Float)
    DO = Column(Float)
    contaminants = Column(ARRAY(String))
    
class User(_database.Base):
    
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String)
    email = Column(String,)
    full_name = Column(String)
    hashed_password = Column(String)
    disabled = Column(Boolean)