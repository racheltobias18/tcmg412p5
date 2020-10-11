#!/usr/bin/python3
from flask import Flask
import os
import time
import re
from slackclient import SlackClient

DEBUG = True

app = Flask(__name__)
slack_app = None
slack_app_id = None

if __name__ == "__main__":
    SLACK_KEY = None
    for l in open("slack.key"):
        SLACK_KEY = l
    slack_app = SlackClient(SLACK_KEY)
    if slack_app.rtm_connect(with_team_state=False):
        slack_app_id = slack_app.api_call("auth.test")["user_id"]
        print("Slack Bot connected...")
    else:
        print("Slack Bot could not connect!")
        if DEBUG == False:
            exit(1)
    app.run(host="0.0.0.0")
