
"""
    The file is having all the Pydantic models that I have used for making api's
 """

from typing import List, Dict, Optional
from pydantic import BaseModel, validator
from datetime import datetime



"""
The function is used to validate the datetime format at which the date is stored
 
 Argument:
   date
  Returns:
   date
"""
def validate_date_format(date_str: str) -> str:
    try:
        datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ")
    except ValueError:
        raise ValueError("Date does not match the format 'YYYY-MM-DDTHH:MM:SSZ'")
    return date_str


# Pydantic model for giving current user information
class UserCurrent(BaseModel):
    username: str
    email: Optional[str]
    full_name: Optional[str]
    disabled: Optional[bool]
    
# Pydantic model for storing the user information inherits from UserCurrent
class User(UserCurrent):
    password: str

# Pydantic model for Token
class Token(BaseModel):
    access_token: str
    token_type: str

# pydantic model for JWT  
class DataToken(BaseModel):
    username: Optional[str]
     
# pydantic model for Location storing latitude and longitude
class Location(BaseModel):
    latitude: float
    longitude: float


# pydantic model defined for storing the parameters of observation
class Parameters(BaseModel):
    pH: float
    conductivity: float
    DO: float
    contaminants: List[str]

# Pydantic model defined for getting the Observation's 
class BaseWaterQuality(BaseModel):
    location: Location
    date_time: str
    description: str
    parameters: Parameters
    
    @validator("date_time")
    def validate_date_time(cls, v):
        return validate_date_format(v)
   
   
# Pydantic model defined for storing the Observations in the table
class WaterQuality(BaseWaterQuality):
    id: int
    
# Pydantic model defined for getting the date range 
class DateRange(BaseModel):
    start_date: str
    end_date: str
    
    
