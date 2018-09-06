# -*- coding: utf-8 -*-

import uuid
from flask import Flask, request, make_response
from chatterbot import ChatBot
from NDChatterBot import NDChatterBot

app = Flask(__name__)

bot = NDChatterBot.NDChatterBot()

@app.route("/")
def home():
    return "Invalid endpoint"

@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')

    resp = None
    if (request.cookies.get('uid')):
        uid = request.cookies.get('uid')
        resp = make_response(str(bot.get_response(userText, uid)))
    else:
        resp = make_response(str(bot.get_response(userText)))
        uid = str(bot.default_conversation_id)
        resp.set_cookie('uid', uid)

    return resp

if __name__ == "__main__":
    app.run()
    #app.run(host="0.0.0.0", port=80)
