from flask import Flask
from threading import Thread

app = Flask("")


@app.route("/")
def home():
    return "hello,i am alive!"


def run():
    app.run(host="0.0.0", port=5050)


def keep_alive():
    t = Thread(target=run)
    t.start()
