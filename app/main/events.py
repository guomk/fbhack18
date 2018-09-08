from flask import session, request
from flask_socketio import emit, join_room, leave_room, rooms, close_room
from .. import socketio
from .routes import room_dict
# from flask.ext.socketio import rooms


@socketio.on('joined', namespace='/chat')
def joined(message):
    """Sent by clients when they enter a room.
    A status message is broadcast to all people in the room."""
    global room_dict
    room = session.get('room')
    join_room(room)
    # print('***' + request.sid + '***')
    print(room_dict)
    emit('status', {'msg': session.get('name') + ' has entered the room.'}, room=room)


@socketio.on('text', namespace='/chat')
def text(message):
    """Sent by a client when the user entered a new message.
    The message is sent to all people in the room."""
    global room_dict
    room = session.get('room')
    emit('message', {'msg': session.get('name') + ':' + message['msg']}, room=room)


@socketio.on('left', namespace='/chat')
def left(message):
    """Sent by clients when they leave a room.
    A status message is broadcast to all people in the room."""
    global room_dict
    room = session.get('room')
    leave_room(room)
    emit('status', {'msg': session.get('name') + ' <h1>has left the room. The conversation is end<h1>'}, room=room)
    close_room(room)

