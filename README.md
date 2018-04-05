
Instructions for using chatbot:

(1) Make sure you are logged in to RobotStreamer

(2) In Chrome, press F12 to do to Developer Tools, then go to the console, and enter this:
localStorage.getItem('robotstreamer_token');

(3) The ouput with be a token in quotes, copy it.

(5) git clone https://github.com/robotstreamer/chatbot

(4) In the chatbot folder, create a config.json file.
Contends of the file should be this:

{"jwt_user_token":"YOURTOKENGOESHERE"}

Make sure you replace YOURTEKNGOESHERE with the token you got in step 3.

(5) Now you can start chatbot:

python3 chatbot.py

