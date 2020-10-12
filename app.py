#!/usr/bin/python3
from flask import Flask, Response, jsonify
import os
import re
from slack import WebClient

DEBUG = True
app = Flask(__name__)
slack_app = None

# Flask Methods
@app.route("/md5/<string:data_to_hash>")
def calc_md5(data_to_hash):
   hash = ""
   return jsonify(input=data_to_hash, output=hash)

@app.route("/factorial/<int:number>")
def calc_factorial(number):
    factorial = 0
    return jsonify(input=number, output=factorial)

@app.route("/fibonacci/<int:number>")
def calc_fibonacci(number):
    fibonacci = 0
    return jsonify(input=number, output=fibonacci)

@app.route("/is-prime/<int:number>")
def calc_is_prime(number):
    is_prime = False
    return jsonify(input=number, output=is_prime)

@app.route("/slack-alert/<string:message>")
def post_slack_alert(message):
    response = slack_app.chat_postMessage(channel='#group-4', text=message)
    return jsonify(input=message, output=response["ok"])

if __name__ == "__main__":
    print("Attempting to read Slack App Key from slack.key file...")
    SLACK_KEY = None
    for l in open("slack.key"):
        SLACK_KEY = l
    if SLACK_KEY == None or len(SLACK_KEY) <= 0:
        print("ERROR: Could not read Slack App Key from slack.key file!")
        if DEBUG == False:
            exit(1)
    else:
        print("Connecting to Slack App with Key ", SLACK_KEY)
        slack_app = WebClient(SLACK_KEY)
    print("Launching Flask App.")
    app.run(host="0.0.0.0")
