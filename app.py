#!/usr/bin/python3
from flask import Flask

DEBUG = True
app = Flask(__name__)
slack_app = None
slack_app_id = None

# Flask Methods
@app.route("/md5")
def calc_md5(data_to_hash):
    return ""

@app.route("/factorial")
def calc_factorial(number):
    return 0

@app.route("/fibonacci")
def calc_fibonacci(number):
    return 0

@app.route("/is-prime")
def calc_is_prime(number):
    return False

@app.route("/slack-alert")
def post_slack_alert(message):
    return False

if __name__ == "__main__":
    SLACK_KEY = None
    for l in open("slack.key"):
        SLACK_KEY = l
    app.run(host="0.0.0.0")
