#!/usr/bin/python3
from flask import Flask, Response, jsonify
from slack import WebClient
import hashlib

FLASK_APP = Flask(__name__)
SLACK_APP = None

# Flask Methods
@FLASK_APP.route("/md5/<string:data_to_hash>")
def calc_md5(data_to_hash):
    #encode string for hash
    hash = data_to_hash.encode("utf-8")
    #convert to hash
    hash = hashlib.md5( hash )
    #return code in new format
    hash = hash.digest()
    return jsonify(input=data_to_hash, output=hash)

@FLASK_APP.route("/factorial/<int:number>")
def calc_factorial(number):
    factorial = 0
    return jsonify(input=number, output=factorial)

@FLASK_APP.route("/fibonacci/<int:number>")
def calc_fibonacci(number):
    
    fibonacci = []
    c1 = 0
    c2 = 1
    fib = 0
    check = 0
    
    if number < 0:
        fibonacci = "Error: Please use a number greater or equal to 0"
    
    elif number == 0:
        fibonacci = 0
    
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
    is_prime = False
    is_integer = isinstance(number, int)        # checks if input is an integer
    if is_integer == True:                      # runs the following code if the input is an integer
        if number > 1:
            for i in range(2, number):
                 if (number % i) == 0:
                    break
            else:
                ir_prime = True
        elif number == 1:
                is_prime = False
        elif number == 0:
                is_prime = True
        else:
                print(number, "is a negative integer and is an invalid input. Please enter an integer greater than 1.")
    else:
        print(number, "is a float and is an invalid input. Please enter an integer.")    
    return jsonify(input=number, output=is_prime)

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
    print("Launching Flask App.")
    FLASK_APP.run(host="0.0.0.0")
