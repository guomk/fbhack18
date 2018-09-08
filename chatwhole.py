from app import create_app, socketio
app = create_app(debug=True)
from flask_socketio import emit, join_room, leave_room, rooms, close_room
from flask_wtf import Form
from wtforms.fields import StringField, SubmitField, HiddenField
from wtforms.validators import Required

class LoginForm(Form):
    """Accepts a nickname and a room."""
    name = StringField('Name', validators=[Required()])
    room = HiddenField()
    submit = SubmitField('Enter Chatroom')
from flask import session, redirect, url_for, render_template, request




usernames = {}
number_of_users = 0
i = 0
room_dict = {}
@app.route('/', methods=['GET', 'POST'])
def index():
    """Login form to enter a room."""
    global room_dict
    global i
    form = LoginForm()
    if form.validate_on_submit():
        session['name'] = form.name.data
        print()
        print()
        print(room_dict)
        print()
        print()
        if i not in room_dict.keys():
            session['room'] = i  # Should be a random number
            room_dict[i] = [1, False]
        else:
            if room_dict[i][1]:
                i += 1
                room_dict[i] = [1, False]
                session['room'] = i  # Should be a random number
            else:
                room_dict[i] = [2, False]
                session['room'] = i  # Should be a random number
                i += 1
        print()
        print()
        print("room #", session['room'])
        print()
        print()
        # print(request.sid)
        # print(room_dict)
        return redirect(url_for('.chat'))
    elif request.method == 'GET':
        form.name.data = session.get('name', '')
        form.room.data = session.get('room', '')

    return render_template('index.html', form=form)


@app.route('/chat')
def chat():
    """Chat room. The user's name and room must be stored in
    the session."""
    name = session.get('name', '')
    room = session.get('room', '')
    if name == '' or room == '':
        return redirect(url_for('.index'))
    return render_template('chat.html', name=name, room=room, rooms=room_dict)





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
    # print(room_dict)
    emit('status', {'msg': session.get('name') + ' has entered the room.'}, room=room)


# When client emits 'add user' this listens and executes
@socketio.on('add user', namespace='/chat')
def add_user(data):
    print('Adding User')
    global usernames
    global number_of_users

    session['username'] = data
    usernames[data] = session['username']

    number_of_users += 1

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
    room_dict[room][1] = True

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












if __name__ == '__main__':
    socketio.run(app)


