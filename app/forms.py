from wtforms import Form, StringField, SelectField, DecimalField, SelectMultipleField, PasswordField, validators

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


class CustomDecimalField(DecimalField):
    def process_formdata(self, valuelist):
        if valuelist:
            try:
                self.data = float(valuelist[0].replace(',', '.'))
            except ValueError:
                self.data = None
                raise ValueError(self.gettext('Not a valid float value'))


class AddProductForm(Form):


    name = StringField('Name', [
        validators.DataRequired(),
        validators.length(min=4, max=50)
    ])

    description = StringField('Description', [
        validators.DataRequired(),
        validators.length(min=4, max=200)
    ])

    place = StringField('Place', [
        validators.DataRequired(),
        validators.length(min=4, max=50)
    ])

    price = CustomDecimalField('Price', [
        validators.DataRequired(),
        validators.NumberRange(min=1.00)
    ])

    max_stock = SelectField('Max Stock', [
        validators.DataRequired()
    ], choices = [
        ("small", "Pequeño"),
        ("medium", "Mediano"),
        ("large", "Grande")
    ])

    colors = SelectMultipleField('Colors', [
        validators.optional()
    ], choices=[
        ("verde", "Verde"),
        ("rojo", "Rojo"),
        ("morado", "Morado"),
        ("amarillo", "Amarillo")
    ])
