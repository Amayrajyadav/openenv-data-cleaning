from pydantic import BaseModel
from typing import List, Dict

class Observation(BaseModel):
    dataset: List[Dict]

class Action(BaseModel):
    cleaned_data: List[Dict]

class Reward(BaseModel):
    score: float