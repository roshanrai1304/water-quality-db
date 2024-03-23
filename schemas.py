from typing import List, Dict, Optional
from pydantic import BaseModel, validator
from datetime import datetime


def validate_date_format(date_str: str) -> str:
    try:
        datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ")
    except ValueError:
        raise ValueError("Date does not match the format 'YYYY-MM-DDTHH:MM:SSZ'")
    return date_str



class UserCurrent(BaseModel):
    username: str
    email: Optional[str]
    full_name: Optional[str]
    disabled: Optional[bool]
    

class User(UserCurrent):
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    
class DataToken(BaseModel):
    username: Optional[str]
       
# class UserInDB(User):
#     hashed_password: str
    

class Location(BaseModel):
    latitude: float
    longitude: float

class Parameters(BaseModel):
    pH: float
    conductivity: float
    DO: float
    contaminants: List[str]

class BaseWaterQuality(BaseModel):
    location: Location
    date_time: str
    description: str
    parameters: Parameters
    
    @validator("date_time")
    def validate_date_time(cls, v):
        return validate_date_format(v)
   
    
class WaterQuality(BaseWaterQuality):
    id: int
    
class DateRange(BaseModel):
    start_date: str
    end_date: str
    
    
