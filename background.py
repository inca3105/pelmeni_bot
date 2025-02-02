import os
from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "Бот активен!"

def run():
    app.run(
        host='0.0.0.0',
        port=int(os.environ.get('PORT', 8080))
    )

def keep_alive():
    server = Thread(target=run)
    server.start()