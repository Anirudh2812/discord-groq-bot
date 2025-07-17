from flask import Flask
from threading import Thread
import time
import requests

app = Flask('')

@app.route('/')
def home():
    return "I'm alive!"

def ping_self():
    while True:
        try:
            print("⏱️ Pinging self...")
            requests.get("https://discord-groq-bot-ljgu.onrender.com")
        except Exception as e:
            print(f"⚠️ Ping failed: {e}")
        time.sleep(300)

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    Thread(target=run).start()
    Thread(target=ping_self).start()
