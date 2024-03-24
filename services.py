

"""
The files contain all the support functions required for the api routes also this file contains the database session
"""

from typing import TYPE_CHECKING, List, Dict, Any
from sqlalchemy import between, or_, text, func
from datetime import datetime
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import HTTPException, APIRouter, status, Depends
from datetime import datetime, timedelta

import database as _database
import models as _models
import schemas as _schemas
import utils as _utils
import oauth as _oauth
import config as _config
from jose import JWTError, jwt
import config as _config

if TYPE_CHECKING:
    from sqlalchemy.orm import Session


"""
function to make tables 
"""
def _add_tables():
    return _database.Base.metadata.create_all(bind=_database.engine)


"""
    Function used for getting the database
    
    Returns:
     databse
"""
def get_db():
    db = _database.SessionLocal()
    try:
        yield db
    finally:
        db.close()
        


"""
    Support function used for creating user
    
    Return
     string: successful creatiuon of the user
"""
async def create_user(
    user: _schemas.User, db: "Session"
): 

    hashed_pass = _utils.get_password_hash(user.password)
    user.password = hashed_pass
    
    new_user = _models.User(
        username=user.username,
        email=user.email,
        full_name=user.full_name,
        hashed_password=user.password,
        disabled=user.disabled
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return {"message": f"Sucessfully created user {new_user.full_name}"}



"""
    Support function for login user
    
    Return
      string
"""    
async def login_user(
    userdetails: OAuth2PasswordRequestForm,
    db: "Session"
):
    user = db.query(_models.User).filter(_models.User.username == userdetails.username).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f"The User Does not exist")
    if not _utils.verify_password(userdetails.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f"The User Does not exist")
        
    access_token_expires = timedelta(minutes=_config.ACCESS_TOKEN_EXPIRE_MINUTES)
       
    access_token = _oauth.create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    
    return {"access_token": access_token, "token_type": "bearer"}


"""
Support function used for getting current user
  
  Argeument
   token: Token Schema
  
  Raise
    credential exception
    
  Return
   User deails : User Schema

"""

async def get_current_user(token: str = Depends(_oauth.oauth2_scheme), db: "Session" = Depends(get_db)):
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                         detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"}) 
    try:
        payload = jwt.decode(token, _config.SECRET_KEY, algorithms=[_config.ALGORITHM])
    
        username: str = payload.get("sub")
        if username is None:
            raise credential_exception

        token_data = _schemas.DataToken(username=username)
    except JWTError:
        raise credential_exception

    user = db.query(_models.User).filter(_models.User.username == token_data.username).first()

    if user is None:
        raise credential_exception

    return user



async def get_current_active_user(current_user: _schemas.UserCurrent = Depends(get_current_user)):
    
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")

    return current_user

async def get_user(
    current_user: _schemas.UserCurrent = Depends(get_current_active_user),
    db: "Session" = Depends(get_db)
):
    return current_user
    
    
"""
Function to create observation to create an entry in Observation table

Argument:
  observation: WaterQuality Schema 
  
 Return:
  String
"""

async def create_observation(
    observation: _schemas.WaterQuality, db: "Session"
) :
    observation = _models.WaterQualityObservationDB(
        latitude=observation.location.latitude,
        longitude=observation.location.longitude,
        date_time=observation.date_time,
        description=observation.description,
        pH=observation.parameters.pH,
        conductivity=observation.parameters.conductivity,
        DO=observation.parameters.DO,
        contaminants=observation.parameters.contaminants
    )
    db.add(observation)
    db.commit()
    db.refresh(observation)
    return {"message": "Observation created Successfully"}



"""
Function to get all observation from the table

Return:
  records: List    
"""
async def get_all_observation(db: "Session") :
    records = db.query(_models.WaterQualityObservationDB).all()
    return records  

"""
  The Function is used to get an observation by id.    

    Argument:
      observation_id: int
      
    Returns:
        WaterQuality: Pydantic model
"""

async def get_observation_by_id(observation_id: int, db: "Session"):
    record = db.query(_models.WaterQualityObservationDB).filter(_models.WaterQualityObservationDB.id == observation_id).first()
    return record


"""
  The Function is used to delete an observation by id.    

    Argument:
      observation_id: int
      
"""
async def delete_observation_by_id(observation: _models.WaterQualityObservationDB, db: "Session"):
    db.delete(observation)
    db.commit()
    
"""
  The api Function is used to update an observation by id.    

    Argument:
      observation_id: int
      
    Returns:
        string
"""
    
async def update_contact_by_id(
    record: _models.WaterQualityObservationDB, observation_data: _schemas.BaseWaterQuality, db: "Session"
):
    id = record.id
    record.longitude = observation_data.location.longitude
    record.latitude = observation_data.location.latitude
    record.date_time = observation_data.date_time
    record.description = observation_data.description
    record.pH = observation_data.parameters.pH
    record.conductivity = observation_data.parameters.conductivity
    record.DO = observation_data.parameters.DO
    record.contaminants = observation_data.parameters.contaminants
    
    db.commit()
    db.refresh(record)
    
    return {"message": f"Observation for {id} updated Successfully"}

"""
The function is used to find the entries from the observation table which are closed to the 
given latitude and longitude or location

 Body:
   Location: Pydantic Model with consisting of latitude and longitude
   
 Returns:
  BaseWaterQuality: Pydantic Model

""" 
async def locate_observation(
    location_data: _schemas.Location, db: "Session"
):
    observations = await get_all_observation(db)
    if observations:
        closest_observation = None
        min_distance = float('inf')
        for obs in observations:
            distance = _utils.calculate_distance(location_data.latitude, location_data.longitude, obs.latitude, obs.longitude)
            if distance < min_distance:
                min_distance = distance
                closest_observation = obs
        return closest_observation
    else:
        return None
   

"""
The function is used to find the entries from the observation table which are in the given date range

 Body:
   start_date, end_date
   
 Returns:
  List[BaseWaterQuality]: List of pydantic model

"""      
async def find_observations_date_range(
    start_date: str, end_date: str, db: "Session"
):  
    
    observations = db.query(_models.WaterQualityObservationDB)\
        .filter(between(_models.WaterQualityObservationDB.date_time, start_date, end_date)).all()
    
    return observations


"""
The function is used to find the entries from the observation table with the given parameters

 Body:
   Dict[type of value's needed, contaminant]
   
 Returns:
  List[BaseWaterQuality]: List of pydantic model

""" 
async def find_observation_parameter(
    params: Dict[str, Any], db: "Session"
):
    
    query_filters = []
    for key, value in params.items():
        
        # minumum pH 
        if key == "min_pH":
            query_filters.append(_models.WaterQualityObservationDB.latitude >= value)
            
        # maximum pH
        elif key == "max_pH":
            query_filters.append(_models.WaterQualityObservationDB.pH <= value)
            
        # Exact pH
        elif key == "pH":
            query_filters.append(_models.WaterQualityObservationDB.pH == value)
            
        # minimum conductivity
        elif key == "min_conductivity":
            query_filters.append(_models.WaterQualityObservationDB.conductivity >= value)
            
        # maximum conductivity
        elif key == "max_conductivity":
            query_filters.append(_models.WaterQualityObservationDB.conductivity <= value)
            
        # Exact conductivity
        elif key == "conductivity":
            query_filters.append(_models.WaterQualityObservationDB.conductivity == value)
            
        # min DO
        elif key == "min_DO":
            query_filters.append(_models.WaterQualityObservationDB.DO >= value)
            
        # max DO
        elif key == "max_DO":
            query_filters.append(_models.WaterQualityObservationDB.DO <= value)
        
        # exact DO
        elif key == "DO":
            query_filters.append(_models.WaterQualityObservationDB.DO == value)
            
        # Give's contaminants wherever the give contaminats are present
        elif key == "any_contaminants":
            contaminant_condition = or_(*[text(f"'{contaminant}' = ANY(contaminants)") for contaminant in value])
            query_filters.append(contaminant_condition)
            
        # Give's contaminant where the exact contaminants are present
        elif key == "contaminants":
            query_filters.append(_models.WaterQualityObservationDB.contaminants == value)
        else:
            return 
        observations = db.query(_models.WaterQualityObservationDB).filter(*query_filters).all()  
        return observations
    

    