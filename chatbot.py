
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

userID = "26"
requiredAmount = 3225

chatEndpoint = {'host': '184.72.15.121', 'port': 8765}
parser = argparse.ArgumentParser(description='robotstreamer chat bot')
parser.add_argument('robot_id')
commandArgs = parser.parse_args()

#sendFailed = False
mainWebsocket = None


async def sendWithCheck(message):

    global mainWebsocket

    print("send with check:", message)
    
    if mainWebsocket is not None:
            print("about to make the raw send")
            await mainWebsocket.send(message)
            print("finished making the raw send")
    else:
            print("send failed because main web socket is not initialized yet")



 



def jsonResponsePOST(url, jsonObject):

    print("json object to POST", jsonObject)

    params = json.dumps(jsonObject).encode('utf8')
    req = urllib.request.Request(url, data=params,
                             headers={'content-type': 'application/json'})
    response = urllib.request.urlopen(req)

    jsonResponse = json.loads(response.read())
    
    print("response:", jsonResponse)
   
    return jsonResponse
    

async def handleStatusMessagesWithRetry():

    while True:
        try:
            await handleStatusMessages()
        except Exception as e:
            print("cound not handle the message, will retry")
        time.sleep(1)

    
        
async def handleStatusMessages():

    global mainWebsocket
    #global sendFailed
    
    print("running handle status messages")

    url = 'ws://%s:%s' % (chatEndpoint['host'], chatEndpoint['port'])
    print("chat url:", url)

    async with websockets.connect(url) as websocket:

        mainWebsocket = websocket
    
        print("connected to service at", url)
        print("chat websocket object:", websocket)

        print("starting websocket.send")
        #await websocket.send(json.dumps({"type":"connect",
        #                                 "robot_id":1,
        #                                 "local_address":"1"}))

        secondCount = 0
        
        while True:
            time.sleep(1)
            secondCount += 1
            if secondCount > 60 * 10:
                print("automatically reconnecting")
                return
            #if sendFailed:
            #    print("send failed, returning")
            #    sendFailed = False
            #    return
            
        #    message = await websocket.recv()
        #    print("received message:", message)
            



async def handleUpdateMessagesWithRetry():

    while True:
        await handleUpdateMessages()
        time.sleep(1)
        
        
async def handleUpdateMessages():                

    global mainWebsocket
    count = 0
    print("start update")
    while True:
            time.sleep(2)
            print("sending")
            j = jsonResponsePOST("http://robotstreamer.com:6001/v1/get_goal_funbits", {"user_id":userID})
            goalAmount = j['goal_funbits']

            if goalAmount > requiredAmount:
                goalMetText = " Goal met. NICE."
                delay = 59 * 110
            else:
                goalMetText = ""
                delay = 59 * 28

            print("delay:", delay)
                
            m = "RS Project Life " + str(int(goalAmount)) + " of " + str(requiredAmount) + " funbits for today. If we meet this daily, robotstreamer stays alive. " + goalMetText
            if count % 2 == 0:
                m = m + " "
            print("message to send:", m)
            await sendWithCheck(json.dumps({"message": m,
                                            "token": config['jwt_user_token']}))
            count += 1
            time.sleep(delay)

            
async def handleAdMessageWithRetry(m, delay):

    while True:
        await handleAdMessage(m, delay)
        time.sleep(1)
            
            
async def handleAdMessage(m, delay):                

    global mainWebsocket
    count = 0
    print("start update")
    while True:
            time.sleep(delay / 50.0)
                
            if count % 2 == 0:
                m = m + " "
            print("message to send:", m)
            await sendWithCheck(json.dumps({"message": m,
                                                 "token": config['jwt_user_token'], "robot_id": commandArgs.robot_id}))
            count += 1
            time.sleep(delay)
            

            
            
            
def start(fn, params):
        try:
                asyncio.new_event_loop().run_until_complete(fn(*params))
        except:
                print("error")
                traceback.print_exc()


def main():                

    print(commandArgs)
    print("starting threads")
    
    _thread.start_new_thread(start, (handleStatusMessagesWithRetry, ()))
    #_thread.start_new_thread(start, (handleUpdateMessagesWithRetry, ()))
    _thread.start_new_thread(start, (handleAdMessageWithRetry, ("RickCast Sat 4PM Pacific Time", 60 * 100)))
    _thread.start_new_thread(start, (handleAdMessageWithRetry, ("Join us on Discord https://discord.gg/n6B7ymy", 60 * 110)))
    _thread.start_new_thread(start, (handleAdMessageWithRetry, ("Want to help the site out? Buying funbits is a great way to donate. Thanks to those that have already!", 60 * 120)))
    _thread.start_new_thread(start, (handleAdMessageWithRetry, ("RobotStreamer all hands Meeting: Sunday 4PM PST. Using Google Hangouts. Check Discord for Details.", 60 * 130)))

    # wait forever
    while True:
        time.sleep(5)

                
if __name__ == '__main__':
    main()


