
Instructions for using chatbot:

(1) Make sure you are logged in to RobotStreamer

(2) In Chrome, press F12 to do to Developer Tools, then go to the console, and enter this:
localStorage.getItem('robotstreamer_token');

(3) The ouput with be a token in quotes, copy it.

(5) git clone https://github.com/robotstreamer/chatbot.git

(4) In the chatbot folder, create a config.json file.
Contends of the file should be this:

{"jwt_user_token":"YOURTOKENGOESHERE"}

Make sure you replace YOURTEKNGOESHERE with the token you got in step 3.

(5) Now you can start chatbot:

python chatbot2.py ROBOTID USERID TIMEINTERVALINSECONDS MESSAGE

For example:

python3 chatbot2.py 100 32848 300 ".this is a message"

