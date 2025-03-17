# backend/schemas.py
from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class ResultBase(BaseModel):
    race_id: int
    driver_id: int
    team_id: int
    position: int
    points: float

class Result(ResultBase):
    id: int
    class Config:
        orm_mode = True

class RaceBase(BaseModel):
    name: str
    date: datetime
    circuit: str

class Race(RaceBase):
    id: int
    results: Optional[List[Result]] = []
    class Config:
        orm_mode = True

class DriverBase(BaseModel):
    name: str
    nationality: str

class Driver(DriverBase):
    id: int
    class Config:
        orm_mode = True

class TeamBase(BaseModel):
    name: str

class Team(TeamBase):
    id: int
    class Config:
        orm_mode = True