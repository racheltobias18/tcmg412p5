#!/usr/bin/python3
from flask import Flask, Response, jsonify

DEBUG = True
app = Flask(__name__)
slack_app = None
slack_app_id = None

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
    response = False
    decoded_message = message.replace("%20", " ")
    return jsonify(input=message, output=response)

if __name__ == "__main__":
    SLACK_KEY = None
    for l in open("slack.key"):
        SLACK_KEY = l
    app.run(host="0.0.0.0")
