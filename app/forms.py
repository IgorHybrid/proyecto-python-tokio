from wtforms import Form, StringField, SelectField, PasswordField, validators

from app.models.role import Role


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


class RegisterForm(Form):
    role = Role()
    found_roles = role.find({"name": {"$ne": 'admin'}})

    roles = [tuple((role["_id"], role["name"])) for role in found_roles]

    username = StringField('Username', [
        validators.DataRequired(),
        validators.length(min=4, max=50)
    ])
    email = StringField('Email', [
        validators.DataRequired(),
        validators.Email()
    ])
    roles_input = SelectField('Roles', [
        validators.DataRequired()
    ], choices=roles)

    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message="Passwords do not match")
    ])
    confirm = PasswordField('Confirm')
