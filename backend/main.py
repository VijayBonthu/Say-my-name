
from fastapi import FastAPI, Depends, HTTPException, status, Response
import uvicorn
import p_model_type
from different_languages import different_language
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
import os
from Split_word import Splitword
from sqlalchemy import exc

from fastapi.middleware.wsgi import WSGIMiddleware

from fastapi.middleware.cors import CORSMiddleware


#Database Creation
models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI()

#CORS to connect to any ip
origins = ["http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:9090"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root(request):
    return {"Hello": "World"}


#Create student Record
@app.post("/createpost", status_code=status.HTTP_201_CREATED )
def tt_speech(details:p_model_type.Post, response:Response, db: Session= Depends(get_db)):
    # print(details.first_name, details.pronoun)

    

    new_dict = details.dict()
    # print(new_dict)
    name = [details.first_name, details.last_name]
    full_name = " ".join(name)
    new_dict["full_name"] = full_name  
    file_name = full_name+str(details.student_id)  
    pronoun = details.pronoun


    different_language(text=full_name,lang=details.lang_name)
    with open(f"{full_name}.wav", "rb") as file: 
        audio_binary = file.read()
    new_dict["audio_binary"] = audio_binary
    if os.path.exists(f"{full_name}.wav"):
        os.remove(f"{full_name}.wav")
    with open(f"{file_name}.wav", "wb") as file:
        file.write(audio_binary)


    new_student_details = models.Student_data(**new_dict)

    try:
        db.add(new_student_details)
        db.commit()
        db.refresh(new_student_details)
    except exc.IntegrityError as e:
        if "duplicate key value violates unique constraint" in str(e):
            raise HTTPException(status_code=404, detail="Student ID already exists")
        db.rollback()
        

    pro_data = {
    "student_id" : new_student_details.student_id,
    "first_name" : new_student_details.first_name,
    # "last_name": new_student_details.last_name,
    "full_name": new_student_details.full_name
    }

    # first_name_pro_eng, last_name_pro_eng =Splitword().Phonetics_eng_words(first_name=pro_data["first_name"], last_name=pro_data["last_name"])
    first_name_pro, f_name_num= Splitword().pronouncing_word(first_name=pro_data["first_name"] )
    split_first_name = Splitword().seperating_name(first_name=pro_data["first_name"])
    # first_name_pro, last_name_pro, f_name_num, l_name_num = Splitword().pronouncing_word(first_name=pro_data["first_name"], last_name=pro_data["last_name"])
    # split_first_name, split_last_name = Splitword().seperating_name(first_name=pro_data["first_name"], last_name=pro_data['last_name'])




    # pro_data["first_name_p_eng"] = first_name_pro_eng
    pro_data["first_name_p"] = first_name_pro
    # pro_data["first_namenum_p"] = f_name_num
    # pro_data["last_name_p_eng"] = last_name_pro_eng
    # pro_data["last_name_p"] = last_name_pro
    # pro_data["last_namenum_p"] = l_name_num
    pro_data["split_first_name"] = split_first_name
    # pro_data["split_last_name"] = split_last_name


    name_list = pro_data["full_name"].split()

    results = db.query(models.Namepronounciation).filter(models.Namepronounciation.name.in_(name_list)).order_by(models.Namepronounciation.votes.desc()).limit(3).all()


    return {"data": pro_data,
            "results": results}


#creating selection record
@app.post("/selection", status_code=status.HTTP_201_CREATED)
def selection(details:p_model_type.Selection, db: Session= Depends(get_db)):
    print(details.student_id, details.name)
    statement_dict = []
    for i in range(len(details.name)):
        data = {"student_id":details.student_id,
                "name":details.name[i],
                "name_selection":details.name_selection[i],
                "audio_selection":"string",
                "votes":details.votes,
                "show":details.show}
        statement_dict.append(data)


    for stat_dict in statement_dict:
        new_data = models.Namepronounciation(**stat_dict)
        db.add(new_data)
        db.commit()
        # db.refresh(new_data)




if __name__ == "__main__":
    uvicorn.run("main:app", port=8081, log_level="info", reload=True)