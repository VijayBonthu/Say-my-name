from flask import Flask,request,render_template,redirect,session
import requests
import os
import binascii
import shutil
 
# Generate a key
secret_key = binascii.hexlify(os.urandom(24)) 
# print(secret_key)
 
app = Flask(__name__)
app.secret_key = secret_key
@app.route('/')
def input_form():
    return render_template('input_form 1.html') 
 
@app.route('/process', methods=['POST'])
def process_form():
    result = {
         'pronoun': request.form['prefix'],
         'first_name' : request.form['name'],
         'last_name' : ' ',
         'student_id' : request.form['Student_id'],
         'course': 'Artificial Intelligence and Data Science',
         'intake': 'Fall',
         'lang_name': 'en',
         'year': '2023'
        }
    # print (result)
    # return ("I am here")
    # result = {"pronoun": "string","first_name": "string","last_name": "string","student_id": 33221,
    #           "lang_name": "en",
    #           "course": "string",
    #           "intake": "Fall",
    #           "year": 0
    #           }
    # response = requests.post("http://127.0.0.1:8081/createpost",json=result) #connect to backend with Json data and url we are .
    # print(response)

    # print(result)
    try:
        response = requests.post("http://127.0.0.1:8081/createpost",json=result) #connect to backend with Json data and url we are 
        # return render_template('error_display 1.html', error_details=response) 
        print(response.json())
        # return render_template('result 1.html', data=response.json())
    # print(r)
    # return "Hello World"
    #     print(r)
    except requests.exceptions.RequestException as e:
        # print(f"An error occurred: {e}")
        return render_template('error_display 1.html', error_details=str(e))
        # return redirect("input_form.html")
    
    return render_template('result 1.html', data=response.json())
#    data = {
#    'pronoun': request.form['prefix'],
#    'first_name' : request.form['name'],
#    'last_name' : ' ',
#    'student_id' : request.form['Student_id'],
#    'course': 'Artificial Intelligence and Data Science',
#    'intake': 'Fall',
#    'lang_name': 'en',
#    'year': '2023'
#    }
#    print(data)
#    try:
#         response = requests.post("http://127.0.0.1:9090/createpost",json=data) #connect to backend with Json data and url we are  
#         print("**********************")
#         print(response.json()) # All the phonetics from the backend 
#         print(response.status_code)# Give the status code. 
#         if response.status_code == 201:
#             result = response.json()
#             print('The result is ')
#             session['first_name'] = result['data']['first_name'] 
#             session['studentid'] = result['data']['student_id']
#             return render_template('result 1.html', data=result)
#         else:
#             print("Error: Could not get data from FastAPI backend.")
#             return redirect("input_form.html")
#    except requests.exceptions.RequestException as e:
#         print(f"An error occurred: {e}")
#         return render_template('error_display 1.html', error_details=response)


        # You can now use the 'finalpage_data' as needed in your application logic

  


@app.route('/submit',methods=['GET','POST'])
def submit_form():

     # reder template to final result page, # Save our phobnetic to db. main code in 
   #if 'firstnameph_radio' in request.args and request.args.get('firstnameph_radio') == 'on':
   #     selected_option = request.args.get('custom_phonetic')
   #else:
    student_id = request.form.get('student_id')
    first_name = request.form.get('first_name')
    # first_name = session.get(student_id)
    selected_option = request.form.get('firstnameph')
    # student_id = session.get(student_id)
    print(student_id, first_name)
    finalpage_data = {
  "student_id": student_id,
  "name": [
    first_name
  ],
  "name_selection": [
    selected_option
  ],
  "audio_selection": "string",
  "votes": 0,
  "show": "true"
}
    print(finalpage_data)

    # finalpage_response = requests.post("http://127.0.0.1:8081/selection", json=finalpage_data)
#    print(finalpage_response)
#    print("Inside the add item form")
#    selected_option = request.args.get('firstnameph')
#    print(selected_option)
#    first_name = session.get('first_name', 'Unknown')
#    print(first_name)
#    student_id = session.get('studentid', 'Unknown')
#    print(student_id)
#    finalpage_data = {
#         'first_name': first_name,  
#         'last_name': '',          
#         'student_id': student_id,
#         'course': 'Artificial Intelligence and Data Science',  # Replace with actual course name
#         'intake': 'Fall',      # Replace with actual intake
#         'year': '2023',               # Replace with actual year
#         'studentid_submit': student_id,
#         'firstname_submit': first_name,
#         'nameselection_submit': selected_option,
#         'votes': 1,
#         'show': True
#     }
    
    source_folder = "..\\backend" #"C:\\Users\\vyshak\\Desktop\\Git_Backup\\SayMyName"
    destination_folder = "..\\F\\static\\audio" #"C:\\Users\\vyshak\\Desktop\\Git_Backup\\SayMyName\\HTML_V09\\static\\audio"
   # Construct absolute paths for the source and destination
    source_audio_path = os.path.join(source_folder, f"{first_name}  {student_id}.wav")
    destination_audio_path = os.path.join(destination_folder, f"{first_name}  {student_id}.wav")
 
    print("Source Path:", source_audio_path)
    print("Destination Path:", destination_audio_path)
    
   
    try:
        if os.path.exists(source_audio_path):
            shutil.move(source_audio_path, destination_audio_path)
            print(f"File successfully copied from:\n{source_audio_path}\nto:\n{destination_audio_path}")
        else:
            print(f"Source file does not exist: {source_audio_path}")
    except Exception as e:

        print(f"Error moving audio file: {e}")
    try:
        finalpage_response = requests.post("http://127.0.0.1:8081/selection", json=finalpage_data)
        # error_details = finalpage_response.json().get('detail', [])
        # print(error_details)
        if finalpage_response.status_code == 422:
            print("You have data set need to be corrected")
            # return render_template('error_display 1.html', error_details=error_details)
        else:
            result_submit = finalpage_response.json()
            print("Data is saved successfully")
            print (result_submit)
            return render_template('final_result 1.html', data = selected_option, firstname = first_name , student_id = student_id)
            
            # return render_template('final_result 1.html', data = result_submit['data']['first_name_p'], firstname = result_submit['data']['first_name'] , student_id = result_submit['data']['student_id'])
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return {"error": "An error occurred while processing the request"}, 500
   
if __name__ == '__main__':
    app.run(host="127.0.0.1", port=9090, debug=True)