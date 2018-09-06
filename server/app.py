# -*- coding: utf-8 -*-

import uuid
from flask import Flask, request, make_response, send_from_directory
from chatterbot import ChatBot
from NDChatterBot import NDChatterBot

app = Flask(__name__, static_folder='build')

bot = NDChatterBot.NDChatterBot()

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

## REACT
@app.route("/")
@app.route("/index.html")
def home():
    return app.send_static_file('index.html')

@app.route("/manifest.json")
def manifest():
    return app.send_static_file('manifest.json')

@app.route("/asset-manifest.json")
def assetmanifest():
    return app.send_static_file('asset-manifest.json')

@app.route("/service-worker.js")
def serviceworker():
    return app.send_static_file('service-worker.js')

@app.route('/vendor/<path:path>')
def send_vendor(path):
    return send_from_directory('build/vendor', path)

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('build/static', path)
## REACT

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
    #app.run(host="0.0.0.0")
    #app.run(host="0.0.0.0", port=80)
