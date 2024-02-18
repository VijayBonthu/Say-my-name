git clone https://github.com/VijayBonthu/say-my-name.git
This should clone it to your laptop.
install reqired modules and packages for both front end and backend using pip install -r requirements.txt.
Then work on the files accordingly.
before pushing the changes make sure you pull the latest code using by doing the following commands.
git remote add origin https://github.com/VijayBonthu/say-my-name.git
git pull orign main
git add .
git commit -m "your commit message"
git push origin main
All the above commands should let you commit changes and update the github.
Make sure you update perodically, so that if you want to undo the pull request because your files are overwritten use the below command to undo it to previous version.
git reset --hard HEAD^1
Thank you

If you are working on this project and have existing files before
git remote add origin https://github.com/VijayBonthu/say-my-name.git
if the above respond backs that its already present then
git pull orign main 
This should update your files to the latest version in github.

create a virtual environment if you already dont have it with the command "python -m venv venv" check your local repositry if you have venv before performing the command.
activate your virtual environement with venv\Scripts\activate
if there are any modules missing then run pip install -r requirements.txt to update or install all modules

run python main.py to run the backend.