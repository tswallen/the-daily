import websocket
import json
import threading
import time
import pandas as pd

# Because of discord's live and secure nature, i used websocket
def send_json_request(ws, request):
    ws.send(json.dumps(request))

def receive_json_response(ws):
    response = ws.recv()
    if response:
        return json.loads(response)

# This starts the "heartbeat" or the initial connection to the discord server
def heartbeat(interval, ws):
    print('Heartbeat begin')
    while True:
        time.sleep(interval)
        heartbeatJSON = {
            "op": 1,
            "d": 'null'
        }
        send_json_request(ws, heartbeatJSON)
        print("Heartbeat Sent")

ws= websocket.WebSocket()
ws.connect('wss://gateway.discord.gg/?v=6&encoding=json')
event = receive_json_response(ws)

heartbeat_interval = event['d']['heartbeat_interval']/1000
threading._start_new_thread(heartbeat, (heartbeat_interval, ws))

# Token is your security token and is unique per user. I can explain if you need but this is WIP
token = 'MjczMTUwNjI3ODgwNjMyMzIx.Gfd8JB.dRw-pXWkNJ13Al1UKlIiA0cPAwbriamLoPU7H8'
payload = {
    'op' : 2,
    'd':{
        'token' : token,
        'properties':{
            '$os': "windows",
           'brower': "edge",
           "$device": "pc"
        }
    }
}
send_json_request(ws,payload)

while True:
    event = receive_json_response(ws)
    try:
        print(f"{event['d']['author']['username']}: {event['d']['content']}:\n:{event['d']['attachments']}")
        op_code = event('op')
        if op_code == 11:
            print('heartbeat recveived')
    except:
        pass
