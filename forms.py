from wtforms import Form, StringField, PasswordField, validators

class SignupForm(Form):
    username = StringField('Username', [validators.DataRequired()])
    email = StringField('Email', [validators.Email(), validators.DataRequired()])
    password = PasswordField('Password', [validators.DataRequired()])
