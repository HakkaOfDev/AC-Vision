#from ast import match_case
import socket
import threading
from websocket_server import WebsocketServer
import logging
import re
import json

from components.redis.cache_updates import update_cache
import time

def register_new_client(client, server):
    print("New client added ! + " + client.address)

server = WebsocketServer(host='0.0.0.0', port=6969, loglevel=logging.INFO)
server.set_fn_new_client(register_new_client)

port = 514
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(("0.0.0.0", port))

REGEX = r"(?P<onu>ONU\([0-9],[0-9]*\)) (?P<status>(DE)?ACTIVATION) \(Reason: (?P<reason>[\w\s\(\)]*)\)"
def listener():
    print('Listener on')
    while True:
        print('hello')
        data, addr = s.recvfrom(4048)
        data = data.decode('utf-8')
        print(data)
        matches = re.search(REGEX, data)
        if matches:
            update_cache()
            print('cache updated')
            onu_info = {"onu": matches.group("onu"),
                        "status": matches.group("status"),
                        "reason": matches.group("reason")}
            print(onu_info)
            server.send_message_to_all(json.dumps(onu_info))

def run():
    threading.Thread(target=listener).start()

