import functools

from flask import Blueprint, jsonify, request, render_template, g, url_for, redirect, session, flash
from bson import ObjectId

from app.models.role import Role
from app.models.user import User
from app.forms import LoginForm, RegisterForm


blueprint = Blueprint('auth', __name__, url_prefix='/auth')


role = Role()
user = User()


@blueprint.route('/register/role', methods=['POST'])
def insert():

    name = request.json.get("name", None)

    error = None

    if not name:
        error = 'Name is required'

    if error is None:
        result = role.find({"name": name},{"name":1})

        if not result:
            id = role.create({"name": name})
            return jsonify(
                msg="Role created!",
                id=id
            )
        else:
            error = "Role already exists"

    msg = {
        "msg": error
    }
    return msg, 409


@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if g.user is None:
        if request.method == 'POST' and form.validate():
            username = form.username.data
            password = form.password.data
            try:
                user_found = user.check_credentials({"username": username, "password": password})

                session.clear()
                session['user_id'] = str(user_found['_id'])

                return redirect(url_for('home.home'))
            except Exception as e:
                flash(str(e), 'danger')
        return render_template('login.html', form=form)
    else:
        return redirect(url_for('home.home'))


@blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if g.user is None:
        if request.method == 'POST' and form.validate():
            username = form.username.data
            password = form.password.data
            email = form.email.data
            role = form.roles_input.data

            found_user = user.find({"username": username})

            if not found_user:
                try:
                    user_fields = {
                        "username": username,
                        "password": password,
                        "email": email,
                        "_role": ObjectId(role)
                    }
                    id = user.create(user_fields)

                    session.clear()
                    session['user_id'] = str(id.inserted_id)

                    return redirect(url_for('home.home'))
                except Exception as e:
                    flash(str(e), 'danger')

            else:
                flash('User already exists', 'danger')
        return render_template('register.html', form=form)
    else:
        return redirect(url_for('home.home'))


@blueprint.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home.home'))


@blueprint.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = user.find_by_id(user_id)


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)
    return wrapped_view