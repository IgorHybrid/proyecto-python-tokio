from wtforms import Form, StringField, PasswordField, validators


class LoginForm(Form):
    username = StringField('Username', [
        validators.DataRequired(),
        validators.length(min=4, max=50)
    ], render_kw={
        "placeholder": "Username"
    })
    password = PasswordField('Password',  [
        validators.DataRequired(),
    ], render_kw={
        "placeholder": "Password"
    })