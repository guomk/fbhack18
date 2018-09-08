from flask import session, redirect, url_for, render_template, request
from . import main
from .forms import LoginForm

i = 0
room_dict = {}
@main.route('/', methods=['GET', 'POST'])
def index():
    """Login form to enter a room."""
    global room_dict
    global i
    form = LoginForm()
    if form.validate_on_submit():
        session['name'] = form.name.data
        session['room'] = i             # Should be a random number
        if str(i) not in room_dict.keys():
            room_dict[str(i)] = 1
        else:
            room_dict[str(i)] += 1
            if room_dict[str(i)] == 2:
                i += 1
        print(request.sid)
        print(room_dict)
        return redirect(url_for('.chat'))
    elif request.method == 'GET':
        form.name.data = session.get('name', '')
        form.room.data = session.get('room', '')
    return render_template('index.html', form=form)


@main.route('/chat')
def chat():
    """Chat room. The user's name and room must be stored in
    the session."""
    name = session.get('name', '')
    room = session.get('room', '')
    if name == '' or room == '':
        return redirect(url_for('.index'))
    return render_template('chat.html', name=name, room=room)
