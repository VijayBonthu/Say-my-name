from database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text

class Student_data(Base):
    __tablename__ = "student_data"

    id = Column(Integer, primary_key=True, nullable=False)
    student_id = Column(Integer, unique=True, nullable=False)
    first_name = Column(String, nullable=False)
    pronoun = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    status_active = Column(Boolean, server_default='TRUE', nullable=False)
    lang_name = Column(String, nullable=False)
    course = Column(String, nullable=False)
    intake = Column(String, nullable=False)
    year = Column(Integer, nullable=False)
    audio_binary = Column(String)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default= text('now()'))

class Namepronounciation(Base):
    __tablename__ = "pronounciation"

    id = Column(Integer, primary_key=True, nullable=False)
    student_id = Column(Integer, ForeignKey(Student_data.student_id), nullable=False)
    name = Column(String, nullable=False)
    name_selection = Column(String, nullable=False)
    audio_selection = Column(String, nullable=True)
    votes = Column(Integer, nullable=False, server_default= text('0'))
    show = Column(Boolean, server_default='False') 
     


