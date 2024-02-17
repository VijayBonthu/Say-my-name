from pydantic import BaseModel
from typing import Literal, Optional


class Post(BaseModel):
    first_name: str
    pronoun: str
    last_name:str
    preferred_name: str
    student_id : int
    course: str
    intake: Literal["Fall", "January", "May"]
    year: int


class Selection(BaseModel): 
    student_id : int
    name:list
    phonetics_selection: list
    audio_selection: str
    show: bool
    data_in_votes_table: bool

# class Selection(BaseModel): 
#     vote_id : int
#     name:list
#     phonetics_selected: list
#     audio_selected: str
    
class Admin_page(BaseModel):
    studentID: Optional[int] = None
    # firstname: str = None,
    # lastname: str = None,
    # preferred_name: str = None,
    # year: int = None,
    # course: str = None,
    # intake: str = None,
    # offset: int = 0,
    # limit: int = 10,
    # class Config:
    #     orm_mode = True
