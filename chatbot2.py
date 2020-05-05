
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
import ssl


config = json.load(open('config.json'))

requiredAmount = 3225

apiHost = "http://api.robotstreamer.com:8080"


print("starting")


def getWithRetry(url, secure=True):

    for retryNumber in range(2000):
        try:
            print("GET", url)
            if secure:
                object = urllib.request.urlopen(url)

            else:
                ctx = ssl.create_default_context()
                ctx.check_hostname = False
                ctx.verify_mode = ssl.CERT_NONE
                object = urllib.request.urlopen(url, context=ctx)



            break
        except:
            print("could not open url", url)
            traceback.print_exc()
            time.sleep(2)

    data = object.read()
    encoding = object.info().get_content_charset('utf-8')
    return data.decode(encoding)



def getChatHost():

        return {'host':'207-148-11-143.robotstreamer.com', 'port':8765}
    
        url = apiHost+'/v1/get_endpoint/rschat/100'

        response = getWithRetry(url, False)
        print("response:", response)
        return json.loads(response)

chatEndpoint = getChatHost() #{'host': '144.202.55.57', 'port': 8765}


parser = argparse.ArgumentParser(description='robotstreamer chat bot')
parser.add_argument('robot_id')
parser.add_argument('user_id')
parser.add_argument('interval', type=int)
parser.add_argument('message')


commandArgs = parser.parse_args()
userID = commandArgs.user_id

print("user id:", userID)
print("robot id:", commandArgs.robot_id)

    

async def initiateConnection(websocket):
		await websocket.send(json.dumps({
			'type': 'connect',
			'message': 'joined',
			'token': config['jwt_user_token'],	#only required on connect
			'robot_id': commandArgs.robot_id,	#only required on connect
			'owner_id': commandArgs.user_id 	#only required on connect
		}))




async def connectAndSendOneMessage():

    url = 'wss://%s:%s' % (chatEndpoint['host'], chatEndpoint['port'])
    print("chat url:", url)

    async with websockets.connect(url) as websocket:

        print('starting connection')
        
        print("connected to service at", url)
        print("chat websocket object:", websocket)

        print("starting websocket.send")

        await initiateConnection(websocket)
        
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


