
import os
import asyncio
import websockets
import time
import argparse
import json
import _thread
import traceback
import subprocess
import urllib
import urllib.request


config = json.load(open('config.json'))

requiredAmount = 3225

chatEndpoint = {'host': '144.202.55.57', 'port': 8765}
parser = argparse.ArgumentParser(description='robotstreamer chat bot')
parser.add_argument('robot_id')
parser.add_argument('user_id')
parser.add_argument('interval', type=int)
parser.add_argument('message')


commandArgs = parser.parse_args()
userID = commandArgs.user_id

print("user id:", userID)
print("robot id:", commandArgs.robot_id)

    
        
async def connectAndSendOneMessage():

    url = 'ws://%s:%s' % (chatEndpoint['host'], chatEndpoint['port'])
    print("chat url:", url)

    async with websockets.connect(url) as websocket:

        print('starting connection')
        
        print("connected to service at", url)
        print("chat websocket object:", websocket)

        print("starting websocket.send")


        await websocket.send(json.dumps({"message": commandArgs.message,
                                         "token": config['jwt_user_token'],
                                         "robot_id": commandArgs.robot_id}))
        
        print("finished, connection will now close")
        
        

            


            
            
def main():

    while True:
        print("starting send")
        try:
            asyncio.new_event_loop().run_until_complete(connectAndSendOneMessage())
        except Exception as e:
            print("error", e)
            traceback.print_exc()

        print("sleeping " + str(commandArgs.interval) + " seconds")
        time.sleep(commandArgs.interval)
            

    

                
if __name__ == '__main__':
    main()


