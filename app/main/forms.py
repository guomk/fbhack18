from flask_wtf import Form
from wtforms.fields import StringField, SubmitField, HiddenField
from wtforms.validators import Required


class LoginForm(Form):
    """Accepts a nickname and a room."""
    name = StringField('Name', validators=[Required()])
    room = HiddenField()
    submit = SubmitField('Enter Chatroom')
