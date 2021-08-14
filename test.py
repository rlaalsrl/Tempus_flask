import os
from flask import Flask, render_template, session
from flask_socketio import SocketIO, emit

# app = Flask(__name__)
# app.secret_key = "secret"
# socketio = SocketIO(app)

# user_no = 1

# @app.before_request
# def before_request():
#     global user_no
#     if 'session' in session and 'user-id' in session:
#         pass
#     else:
#         session['session'] = os.urandom(24)
#         session['username'] = 'user'+str(user_no)
#         user_no += 1

# @app.route('/')
# def index():
#     return render_template('chat.html')

# @socketio.on('connect', namespace='/mynamespace')
# def connect():
#     emit("response", {'data': 'Connected', 'username': session['username']})

# @socketio.on('disconnect', namespace='/mynamespace')
# def disconnect():
#     session.clear()
#     print(Disconnected)

# @socketio.on("request", namespace='/mynamespace')
# def request(message):
#     emit("response", {'data': message['data'], 'username': session['username']}, broadcast=True)

# if __name__ == '__main__':
#     socketio.run(app)

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/sessions')
def sessions():
    return render_template('session.html')

def messageReceived(methods=['GET', 'POST']):
    print('message was received!!!')

@socketio.on('my event')
def handle_my_custom_event(json, methods=['GET', 'POST']):
    print('received my event: ' + str(json))
    socketio.emit('my response', json, callback=messageReceived)




if __name__ == '__main__':
    socketio.run(app, debug=True)

