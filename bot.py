import slack
import requests
import os 
from pathlib import Path
from dotenv import load_dotenv
from flask import Flask,Response,request
from slackeventsapi import SlackEventAdapter
import json

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

app = Flask(__name__)
slack_event_adapter = SlackEventAdapter(os.environ.get('SIGNING_SECRET'), "/slack/events", app)

client = slack.WebClient(token=os.environ.get('SLACK_TOKEN'))
BOT_ID = client.api_call("auth.test")["user_id"]


@slack_event_adapter.on("message")
def message(payload):
    # print(payload)
    event = payload.get("event", {})
    channel_id = event.get("channel")
    user_id = event.get("user")
    text = event.get("text")

    if BOT_ID != user_id:
        client.chat_postMessage(channel=channel_id, text=text)

@app.route("/quote", methods=["POST"])
def quote():
    data = request.form
    user_id = data.get("user_id")
    channel_id = data.get("channel_id")
    #call api
    
    response = requests.get("https://zenquotes.io/api/random/")
    query = response.json()[0]["q"]
    client.chat_postMessage(channel=channel_id, text=f"Quote - {query}")
    print(query)
    return Response(), 200

if __name__ == "__main__":
    app.run(debug=True)