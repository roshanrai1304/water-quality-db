

"""
This file where the FastAPI object is initialized and all the routes are defined     
"""

import fastapi as _fastapi
from typing import TYPE_CHECKING, List, Dict, Any
import sqlalchemy.orm as _orm
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm


import schemas as _schemas
import services as _services
import models as _models
import utils as _utils
import oauth as _oauth


if TYPE_CHECKING:
    from sqlalchemy.orm import Session
    
routers = _fastapi.APIRouter(
    tags=['Authentication']
)


# FastAPI object is initialized
app = _fastapi.FastAPI()





"""
    route defined for creating the user with necessary information that can acesss the api's afterwards and returns
    name of the user created and adds it to the user table
    

    Returns:
        dict: name of the user created
    """
@app.post("/", status_code=_fastapi.status.HTTP_201_CREATED)
async def create_user(user:_schemas.User, db: _orm.Session = _fastapi.Depends(_services.get_db)):

    return await _services.create_user(user=user, db=db)

# route defined for getting 
# @app.post('/login', response_model=_schemas.Token)
# async def login(
#     userdetails: OAuth2PasswordRequestForm = _fastapi.Depends(),
#     db: _orm.Session = _fastapi.Depends(_services.get_db)
#     ):
#     return await _services.login_user(userdetails=userdetails, db=db)



"""
  api is defined for getting the current user that is logged in from the user table   
   
    Body:
     User: Pydantic model User

    Returns:
        dict: User logged in
    """
@app.get("/water-quality/user")
async def read_user(current_user: _schemas.UserCurrent = _fastapi.Depends(_services.get_current_active_user)):

    return {"message": f"{current_user.full_name} is the current user"}



"""
 The api route is used enter a record in the Observation Table.
 
  Body: 
   BaseWaterQuality: pydantic model 

    Returns:
        dict: message for successfully addition of record
    """
@app.post("/water-quality/add")
async def create_observation(
    observation: _schemas.BaseWaterQuality,
    current_user: _schemas.UserCurrent = _fastapi.Depends(_services.get_current_active_user),
    db: _orm.Session = _fastapi.Depends(_services.get_db),
):
    return await _services.create_observation(observation=observation, db=db)


"""
  The api route is used to get all the records from the Observation Table.   

    Returns:
        List[WaterQuality]: List of Pydantic model's 
    """
@app.get("/water-quality/get-all")
async def get_all_observations(current_user: _schemas.UserCurrent = _fastapi.Depends(_services.get_current_active_user), db: _orm.Session = _fastapi.Depends(_services.get_db)) -> List[_schemas.WaterQuality]:
    records = await _services.get_all_observation(db=db)
    return _utils.data_format_waterqualtiy(records=records)


"""
  The api route is used to get an observation by id.    

    Argument:
      observation_id: int
      
    Returns:
        WaterQuality: Pydantic model
"""
@app.get("/water-quality/get-observation-by-id/{observation_id}", response_model=_schemas.WaterQuality)
async def get_observation_by_id(
    observation_id: int, 
    current_user: _schemas.UserCurrent = _fastapi.Depends(_services.get_current_active_user),
    db: _orm.Session = _fastapi.Depends(_services.get_db)
):
    record = await _services.get_observation_by_id(observation_id=observation_id, db=db)
    if record is None:
        raise _fastapi.HTTPException(status_code=404, detail="Observation does not exist")
    
    return _utils.data_format_waterqualtiy(records=record)

"""
  The api route is used to delete an observation by id.    

    Argument:
      observation_id: int
      
    Returns:
        string
"""
@app.delete("/water-quality/delete-observation-by-id/{observation_id}")
async def delete_observation_by_id(
    observation_id: int,
    current_user: _schemas.UserCurrent = _fastapi.Depends(_services.get_current_active_user),
    db: _orm.Session = _fastapi.Depends(_services.get_db)
):
    record = await _services.get_observation_by_id(observation_id=observation_id, db=db)
    if record is None:
        raise _fastapi.HTTPException(status_code=404, detail="Observation does not exist")
    
    await _services.delete_observation_by_id(record, db=db)
    
    return "Successfully deleted the observation"


"""
  The api route is used to upddate an observation by id.    

    Argument:
      observation_id: int
      
    Returns:
        string
"""
@app.put("/water-quality/update-observation-by-id/{observation_id}")
async def update_observation_by_id(
    observation_id:int,
    observation_data: _schemas.BaseWaterQuality,
    current_user: _schemas.UserCurrent = _fastapi.Depends(_services.get_current_active_user),
    db: _orm.Session = _fastapi.Depends(_services.get_db),
):     
    record = await _services.get_observation_by_id(observation_id=observation_id, db=db)
    if record is None:
        raise _fastapi.HTTPException(status_code=404, detail="Observation does not exist")
    
    return await _services.update_contact_by_id(
        record=record, observation_data=observation_data, db=db
    )
    
    

"""
The api route is used to find the entries from the observation table which are closed to the 
given latitude and longitude or location

 Body:
   Location: Pydantic Model with consisting of latitude and longitude
   
 Returns:
  BaseWaterQuality: Pydantic Model

"""    
@app.post("/water-quality/location-closest-observation/", response_model=_schemas.BaseWaterQuality)
async def closest_observation_location(
    location_data: _schemas.Location,
    current_user: _schemas.UserCurrent = _fastapi.Depends(_services.get_current_active_user),
    db: _orm.Session = _fastapi.Depends(_services.get_db),
):
    closest = await _services.locate_observation(location_data=location_data, db=db)
    if closest is None:
        raise _fastapi.HTTPException(status_code=404, detail="No Observations found")
    
    return _utils.data_format_waterqualtiy(records=closest)


"""
The api route is used to find the entries from the observation table which are in the given date range

 Body:
   start_date, end_date
   
 Returns:
  List[BaseWaterQuality]: List of pydantic model

""" 
@app.get("/water-qulaity/observations-date-range/")
async def find_observations_date_in_range(
    start_date: str, end_date: str, 
    current_user: _schemas.UserCurrent = _fastapi.Depends(_services.get_current_active_user),
    db: _orm.Session = _fastapi.Depends(_services.get_db)
)-> List[_schemas.BaseWaterQuality]:
    
    start_date = _utils.parse_date(start_date)
    end_date = _utils.parse_date(end_date)
  
    records = await _services.find_observations_date_range(start_date=start_date, end_date=end_date, db=db)
    if records is None:
        raise _fastapi.HTTPException(status_code=404, detail="No Observations found in the given range")
    
    return _utils.data_format_waterqualtiy(records=records)

"""
The api route is used to find the entries from the observation table with the given parameters

 Body:
   Dict[type of value's needed, contaminant]
   
 Returns:
  List[BaseWaterQuality]: List of pydantic model

""" 

@app.post("/water-quality/get-by-parameter/")
async def find_observations_by_parameters(
    params: Dict[str, Any], 
    current_user: _schemas.UserCurrent = _fastapi.Depends(_services.get_current_active_user),
    db: _orm.Session = _fastapi.Depends(_services.get_db)
) -> List[_schemas.BaseWaterQuality]:
    
    observations = await _services.find_observation_parameter(params=params, db=db)
    if not observations:
        raise _fastapi.HTTPException(status_code=404, detail="No observations found based on the specified parameters")
    
    return _utils.data_format_waterqualtiy(observations)

    
