from server.models.game_state import GameState
from server.models.session import Session
from server.communication.threaded_request import ThreadedRequest, RequestType
from server.communication.unreal_socket import UnrealSocket
from server.util.heroku_logger import p
from server.app import db, app, cache
from server.util.extensions import session_required

@app.route('/register', methods=['POST'])
def register_client():
    host = request.json['host']
    port = request.json['port']
    new_session = Session(host, port)
    db.session.add(new_session)
    db.session.commit()
    return 'ok'
    
@session_required
@app.route('/alexa', methods=['POST'])
def execute_command(key):
    p('test')
    session = Session.query.filter_by(key=key).first()
    if session:
        socket = UnrealSocket(session.host, session.port)
        socket.send(request.json['command'])
        p('ok')
        return 'OK'
    else:
        p('shit')
        return 'Nope'

@app.route('/queryResponse', methods=['POST'])
def execute_query():
    cache.set('query_list', request.json['query_list'])
    return 'ok' 

def getQueryList():
    if cache.get('query_list') is not None:
        return cache.get('query_list')
    else:
        p('query list is none')
        return ['nothing yet']

def getSpeech():
    if cache.get('speech') is not None:
        return cache.get('speech')
    else:
        p('speech is none')
        return ['nothing yet']

def buildQueryList(query_list):
    query_str = ', '.join(['a ' + x for x in query_list][:-1]) + ', and a ' + query_list[-1]
    return render_template('locate', queryStr = query_str)
