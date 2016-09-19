import requests
import sys
import logging
import threading
import os

from flask import Flask, request, render_template
from flask_ask import Ask
from werkzeug.contrib.cache import SimpleCache
from flask_sqlalchemy import SQLAlchemy
from werkzeug.serving import WSGIRequestHandler

from util.heroku_logger import p
from util.extensions import session_required

app = Flask(__name__)
ask = Ask(app, "/")
app.config.from_object(os.environ['APP_SETTINGS'])
db = SQLAlchemy(app)
cache = SimpleCache()

from views.unreal import *
from views.intent_generation import *

def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

@app.route('/shutdown', methods=['POST'])
def shutdown():
    shutdown_server()
    return 'Server shutting down...'

if __name__ == '__main__':
    app.run(debug=True, threaded=True)
