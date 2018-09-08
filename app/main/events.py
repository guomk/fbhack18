from flask import session, request
from flask_socketio import emit, join_room, leave_room, rooms, close_room
from .. import socketio
from .routes import room_dict

# from flask.ext.socketio import rooms

usernames = {}
number_of_users = 0


# When the client emits 'connection', this listens and executes
@socketio.on('connect', namespace='/chat')
def user_connected():
    room = session.get('room')
    print('User connected')

@socketio.on('joined', namespace='/chat')
def joined(message):
    """Sent by clients when they enter a room.
    A status message is broadcast to all people in the room."""
    global room_dict
    room = session.get('room')
    print(request.sid)
    join_room(room)
    # print('***' + request.sid + '***')
    print(room_dict)
    emit('status', {'msg': session.get('name') + ' has entered the room.'}, room=room)


# When client emits 'add user' this listens and executes
@socketio.on('add user', namespace='/chat')
def add_user(data):
    print('Adding User')
    global usernames
    global number_of_users

    session['username'] = data
    usernames[data] = session['username']

    number_of_users += 1;

    emit('login', {'numUsers': number_of_users})
    emit('user joined', {'username': session['username'], 'numUsers': number_of_users}, broadcast=False)


@socketio.on('typing', namespace='/chat')
def typing_response():
    room = session.get('room')
    try:
        emit('typing', {'username': session['username']}, room=room)
    except:
        pass


@socketio.on('stop typing', namespace='/chat')
def stop_typing():
    room = session.get('room')
    try:
        emit('stop typing', {'username': session['username']}, room=room)
    except:
        pass


@socketio.on('disconnect', namespace='/chat')
def disconnect():
    global usernames
    global number_of_users
    room = session.get('room')

    try:
        del usernames[session['username']]
        number_of_users -= 1
        emit('user left', {'username': session['username'], 'numUsers': number_of_users}, room=room)

    except:
        pass


@socketio.on('new message', namespace='/chat')
def new_message(data):
    room = session.get('room')
    print("*** new message ***")
    emit('new message',
         {'username': session['username'],
          'message': data}, room=room)

@socketio.on('timer', namespace='/chat')
def timer(data):
    room = session.get('room')
    print("*** timer executed ***")
    emit('new message',
         {'username': session['username'],
          'message': data}, room=room, broadcast=True)


@socketio.on('left', namespace='/chat')
def left(message):
    """Sent by clients when they leave a room.
    A status message is broadcast to all people in the room."""
    global room_dict
    room = session.get('room')
    leave_room(room)
    emit('status', {'msg': session.get('name') + ' <h1>has left the room. The conversation is end<h1>'}, room=room)
    close_room(room)
