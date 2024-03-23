import schemas  as _schemas
from math import radians, sin, cos, sqrt, atan2
from datetime import datetime
from passlib.context import CryptContext

### Function to give entries in format of pydantic model WaterQuality
def data_format_waterqualtiy(records):
    if type(records) != list:
        location = _schemas.Location(latitude=records.latitude, longitude=records.longitude)
        parametes = _schemas.Parameters(pH=records.pH, conductivity=records.conductivity, DO=records.DO, contaminants=records.contaminants)
        observation = _schemas.WaterQuality(id=records.id,location=location, date_time=records.date_time, description=records.description, parameters=parametes)
        return observation
    else:
        data = []
        for record in records:
            location = _schemas.Location(latitude=record.latitude, longitude=record.longitude)
            parametes = _schemas.Parameters(pH=record.pH, conductivity=record.conductivity, DO=record.DO, contaminants=record.contaminants)
            observation = _schemas.WaterQuality(id=record.id,location=location, date_time=record.date_time, description=record.description, parameters=parametes)
            data.append(observation)

    return data 
        
        
### Function used to calculate distance between locations

def calculate_distance(lat1, lon1, lat2, lon2):
    # Converting latitude and longitude from degrees to radians
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    distance = 6371 * c  # Radius of Earth in kilometers
    return distance

# Function to parse the date
def parse_date(date_str: str) -> datetime:
    return datetime.strptime(date_str, "%d-%m-%Y").strftime("%Y-%m-%dT%H:%M:%SZ")


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(non_hashed_pass, hashed_pass):
    return pwd_context.verify(non_hashed_pass, hashed_pass)
