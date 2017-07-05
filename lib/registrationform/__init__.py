from wtforms import Form, BooleanField, StringField, PasswordField, validators


class RegistrationForm(Form):
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email Address', [validators.Length(min=6, max=40)])
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must  match')
    ])
    firstname = StringField('First Name', [validators.DataRequired(), validators.Email])
    confirm = PasswordField('Repeat Password')