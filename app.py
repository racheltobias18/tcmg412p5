#!/usr/bin/python3
from flask import Flask, Response, jsonify
from slack import WebClient
import hashlib
import redis

FLASK_APP = Flask(__name__)
REDIS = None
SLACK_APP = None

# Flask Methods
@FLASK_APP.route("/keyval/<string:key_str>/<string:val>", methods=["POST"])
def post_value(key_str, val):
    cmd = "POST " + key_str + "/" + val
    if REDIS.exists(key_str):
        return jsonify(key=key_str, value=val, command=cmd, result=False, error="Unable to add pair: key already exists."), 409
    return_code = REDIS.set(key_str, val)
    if return_code is False:
        return jsonify(key=key_str, value=val, command=cmd, result=False, error="Unable to add pair: I/O Error!"), 400
    return jsonify(key=key_str, value=val, command=cmd, result=True, error=""), 200

@FLASK_APP.route("/keyval/<string:key_str>", methods=["GET"])
def get_value(key_str):
    method = "GET" + key_str
    if REDIS.exists(key_str):
        return jsonify(key=key_str, value=val, command=method, result=False, error="Unable to retrieve pair: Key does not exist."). 409
    code = REDIS.get(key_str)
    if code is False:
        return jsonify(key=key_str, value=val, command=method, result=False, error="Unable to retrieve pair: Invalid request."), 400
    return jsonify(key=key_str, value=val, command=method, result=True, error=""), 200

@FLASK_APP.route("/keyval/<string:key_str>/<string:val>", methods=["PUT"])
def put_value(key_str, val):
    return jsonify(key=key_str, value=val, command="", result=True, error=""), 200

@FLASK_APP.route("/keyval/<string:key_str>", methods=["DELETE"])
def delete_value(key_str):
    return jsonify(key=key_str, value=val, command="", result=True, error=""), 200

@FLASK_APP.route("/md5/<string:data_to_hash>")
def calc_md5(data_to_hash):
    #encode string for hash
    hash = data_to_hash.encode("utf-8")
    #convert to hash
    hash = hashlib.md5( hash )
    #return code in new format
    hash = hash.hexdigest()
    return jsonify(input=data_to_hash, output=hash)

@FLASK_APP.route("/factorial/<int:number>")
def calc_factorial(number):
    factorial = 1
    if number < 0:
        return jsonify(input=number, output="Error: factorial does not exist for negative numbers")
    elif number == 0:
        return jsonify(input=number, output=1)
    else:
        for i in range(1,number+1):
            factorial = factorial*i
    return jsonify(input=number, output=factorial)

@FLASK_APP.route("/fibonacci/<int:number>")
def calc_fibonacci(number):
    fibonacci = [0]
    c1 = 0
    c2 = 1
    fib = 0
    check = 0

    if number < 0:
        return jsonify(input=number, output="Error: Please use a number greater or equal to 0")
    elif number == 0:
        fibonacci = [0]
    else:
        while check == 0:
            fib = c1 + c2
            c2 = c1
            c1 = fib
            if fib <= number:
                fibonacci.append(fib)
            else:
                check = 1
    return jsonify(input=number, output=fibonacci)

@FLASK_APP.route("/is-prime/<int:number>")
def calc_is_prime(number):
    is_integer = isinstance(number, int)
    if is_integer == True:
        if number > 1:
            for i in range(2, number):
                if (number % i) == 0:
                    return jsonify(input=number, output=False)
        elif number == 1:
            return jsonify(input=number, output=False)
        elif number == 0:
            return jsonify(input=number, output=True)
        else:
            return jsonify(input=number, output="Input is a negative integer and is invalid. Please enter a positive integer.")
    else:
        return jsonify(input=number, output="Input is a float and is invalid. Please enter an integer.")    
    return jsonify(input=number, output=True)

@FLASK_APP.route("/slack-alert/<string:message>")
def post_slack_alert(message):
    response = SLACK_APP.chat_postMessage(channel='#group-4', text=message)
    return jsonify(input=message, output=response["ok"])

if __name__ == "__main__":
    print("Attempting to read Slack App Key from slack.key file...")
    SLACK_KEY = None
    for l in open("slack.key"):
        SLACK_KEY = l.replace(" ", "")
    if SLACK_KEY == None or len(SLACK_KEY) < 55:
        print("ERROR: Could not read Slack App Key from slack.key file!")
    else:
        print("Connecting to Slack App with Key ", SLACK_KEY)
        SLACK_APP = WebClient(SLACK_KEY)
    print("Connecting to REDIS Server @ 127.0.0.1:6379")
    REDIS = redis.Redis()
    print("Launching Flask App.")
    FLASK_APP.run(host="0.0.0.0")
