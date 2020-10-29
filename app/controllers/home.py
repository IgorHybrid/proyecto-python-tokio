from flask import render_template, Blueprint

blueprint = Blueprint('home', __name__)


@blueprint.route('/')
def home():
    return render_template('home.html')