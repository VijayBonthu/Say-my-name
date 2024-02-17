
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

# def get_db_session2():
#     another_db = SessionLocal()
#     try:
#         yield another_db
#     finally:
#         another_db.close()

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

    new_dict = details
    new_dict = details.dict()
    name = [details.first_name, details.last_name]
    full_name = " ".join(name)
    new_dict["full_name"] = full_name
    file_name = full_name+str(details.student_id)  
    pronoun = details.pronoun
    preferred_name = details.preferred_name.lower()


    different_language(text=preferred_name,lang="en")
    with open(f"{preferred_name}.wav", "rb") as file: 
        audio_binary = file.read()
        # print(type(audio_binary))
    new_dict["audio_binary"] = audio_binary
    if os.path.exists(f"{preferred_name}.wav"):
        os.remove(f"{preferred_name}.wav")
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

    #logic to get the phonetics from the DB
    # phonetics_data = db.query(models.Phonetics).filter(models.Phonetics.names == new_student_details.preferred_name.lower()).all()
    phonetics_data = db.query(models.Phonetics).filter(models.Phonetics.names == new_student_details.preferred_name.lower()).all()
    # print(phonetics_data.phonetics)

    preferred_phonetics = [x.phonetics for x in phonetics_data]

    pro_data = {
    "student_id" : new_student_details.student_id,
    "first_name" : new_student_details.first_name.lower(),
    "last_name": new_student_details.last_name.lower(),
    "full_name": new_student_details.full_name.lower(),
    "preferred_name": new_student_details.preferred_name.lower(),
    "audio_binary": new_student_details.audio_binary,
    "pronoun": new_student_details.pronoun,
    "phonetics": preferred_phonetics
    }

    # first_name_pro_eng, last_name_pro_eng =Splitword().Phonetics_eng_words(first_name=pro_data["first_name"], last_name=pro_data["last_name"])
    # first_name_pro, f_name_num= Splitword().pronouncing_word(first_name=pro_data["first_name"] )
    # split_first_name = Splitword().seperating_name(first_name=pro_data["first_name"])
    # first_name_pro, last_name_pro, f_name_num, l_name_num = Splitword().pronouncing_word(first_name=pro_data["first_name"], last_name=pro_data["last_name"])
    # split_first_name, split_last_name = Splitword().seperating_name(first_name=pro_data["first_name"], last_name=pro_data['last_name'])




    # pro_data["first_name_p_eng"] = first_name_pro_eng
    # pro_data["first_name_p"] = first_name_pro
    # pro_data["first_namenum_p"] = f_name_num
    # pro_data["last_name_p_eng"] = last_name_pro_eng
    # pro_data["last_name_p"] = last_name_pro
    # pro_data["last_namenum_p"] = l_name_num
    # pro_data["split_first_name"] = split_first_name
    # pro_data["split_last_name"] = split_last_name


    name_list = pro_data["preferred_name"].split()


    results = db.query(models.Votes).filter(models.Votes.name.in_(name_list)).order_by(models.Votes.votes.desc()).limit(3).all()

    print(len(results))
    if len(results) == 0:
        pro_data["data_in_votes_table"] = False
    elif len(results)>0:
        pro_data["data_in_votes_table"] = True


    return {"data": pro_data,
            "results": results}


#creating selection record
@app.post("/selection", status_code=status.HTTP_201_CREATED)
def selection(details:p_model_type.Selection, db: Session= Depends(get_db)):
    # print(details.student_id, details.name)


    if details.data_in_votes_table is True:
        getting_votes = db.query(models.Votes).filter(models.Votes.phonetic.in_(details.phonetics_selection)).all()

        current_vote = [{"id": x.votes_id,"name": x.name, "phonetic": x.phonetic, "votes":x.votes, "exist_in_phonetics_db": x.exist_in_phonetics_db} for x in getting_votes]

        print(current_vote[0]["id"])
        statement_dict = []
        voting_data_dict = []
        for i in range(len(details.name)):
            data = {"student_id":details.student_id,
                    "name":details.name[i],
                    "phonetics_selection":details.phonetics_selection[i],
                    "audio_selection":details.audio_selection[i],
                    "show":details.show}
            statement_dict.append(data)  
        for stat_dict in statement_dict:
            new_data = models.Namepronounciation(**stat_dict)
            db.add(new_data)
            db.commit()
        for i in range(len(current_vote)):
            voting_data = {"votes_id": current_vote[i]["id"],
                        "name":details.name[i],
                        "phonetic": details.phonetics_selection[i],
                        "votes": current_vote[i]["votes"] +1}
            voting_data_dict.append(voting_data)

        print(voting_data_dict)
        for vote_dict in voting_data_dict:
            print(vote_dict)
            post_query = db.query(models.Votes).filter(models.Votes.votes_id == vote_dict["votes_id"])
            print(post_query)
            post = post_query.first()
            print(post)
            if post == None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {vote_dict['votes_id']} doesn't exist")
            try:
                post_query.update(vote_dict, synchronize_session=False)
                db.commit()
            except Exception as e:
                print(e) 
                db.rollback()
            

    if details.data_in_votes_table is False:
        # getting_votes = db.query(models.Votes).filter(models.Votes.phonetic.in_(details.phonetics_selection)).all()

        # current_vote = [{"id": x.votes_id,"name": x.name, "phonetic": x.phonetic, "votes":x.votes, "exist_in_phonetics_db": x.exist_in_phonetics_db} for x in getting_votes]

        # print(current_vote[0]["id"])
        statement_dict = []
        voting_data_dict = []
        for i in range(len(details.name)):
            data = {"student_id":details.student_id,
                    "name":details.name[i],
                    "phonetics_selection":details.phonetics_selection[i],
                    "audio_selection":details.audio_selection,
                    "show":details.show}
            statement_dict.append(data) 

            voting_data = {
                        "name":details.name[i],
                        "phonetic": details.phonetics_selection[i],
                        "votes":1}
            voting_data_dict.append(voting_data)
             
        for stat_dict in statement_dict:
            new_data = models.Namepronounciation(**stat_dict)
            db.add(new_data)
            db.commit()

        for i in range(len(details.name)):
            voting_data = {
                        "name":details.name[i],
                        "phonetic": details.phonetics_selection[i],
                        "votes":1}
            voting_data_dict.append(voting_data)
        for vote_dict in voting_data_dict:
            new_data = models.Votes(**vote_dict)
            try:
                db.add(new_data)
                db.commit()
            except Exception as e:
                print(f"couldn't add the record because {e}")
                db.rollback()


    # else:
    #     for i in range(len(details.name)):
    #         data = {"student_id":details.student_id,
    #                 "name":details.name[i],
    #                 "phonetics_selection":details.phonetics_selection[i],
    #                 "audio_selection":details.audio_selection[i],
    #                 "show":details.show}
    #         statement_dict.append(data)
    #         voting_data = {"name":details.name[i],
    #             "phonetics": details.phonetics_selection[i],
    #             "votes": 1}
    #         voting_data_dict.append(voting_data)

    # for stat_dict in statement_dict:
    #     new_data = models.Namepronounciation(**stat_dict)
    #     new_votes_data = models.Votes(**voting_data)
    #     db.add(new_data)
    #     db.add(new_votes_data)
    #     db.commit()
    #     # db.refresh(new_data)

@app.get("/getRecords/{details}")
async def get_students(details, db: Session= Depends(get_db)):
    print(details)

    # query = db.query(models.Student_data)

    # if details.studentID:
    #     query = query.filter(models.Student_data.student_id == details.studentID)
    # # if firstname:
    # #     query = query.filter(StudentDetails.firstname == firstname)
    # # if lastname:
    # #     query = query.filter(StudentDetails.lastname == lastname)
    # # if preferred_name:
    # #     query = query.filter(StudentDetails.preferred_name == preferred_name)
    # # if year:
    # #     query = query.filter(StudentDetails.year == year)
    # # if course:
    # #     query = query.filter(StudentDetails.course == course)
    # # if intake:
    # #     query = query.filter(StudentDetails.intake == intake)

    # total_count = query.count()

    # students = query.offset(details.offset).limit(details.limit).all()

    # return {"total_count": total_count, "students": students}
    return {"details": details}

if __name__ == "__main__":
    uvicorn.run("main:app", port=8081, log_level="info", reload=True)