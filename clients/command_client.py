import requests
import time

from datetime import datetime
from threading import Thread, Event

URL = "http://localhost:5000"

name = input("Name: ")
password = input("Password: ")

r = requests.post(URL + "/login", json={'name': name, 'password': password})
token = str()

if r.ok:
    r :dict= r.json()
    token = r['token']
    print(token)
else:
    r.json()['message']
headers = {"Content-Type": "application/json", 'Token': token}

class Reciever(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.kill = Event()
    def run(self):
        self.__time = time.time() - 24 * 60 * 60
        while not self.kill.is_set():
            r = requests.get(URL + "/messages", headers=headers, params=(('after', self.__time),))
            if r.ok:
                messages = r.json()['messages']
                for message in messages:
                    t = message['time']
                    date = datetime.utcfromtimestamp(t).strftime("%H:%M")
                    print(f"{date} {message['name']}: {message['text']}")
                    if t > self.__time:
                        self.__time = t
            elif r.status_code == 401:
                print("You need to relogin")
                self.kill.set()
                break
            time.sleep(2)

rec = Reciever()
rec.daemon = True
rec.start()
time.sleep(5)
try:
    while rec.is_alive():
        message = input("Message: ")
        if not 0 < len(message) < 255: 
            continue
        r = requests.post(URL + "/send", headers=headers, json={'text': message})
        time.sleep(2)
        if not r.ok:
            break
    print("Reciever closed.")
except KeyboardInterrupt:
    pass
print("Closing application...")
rec.kill.set()
                    