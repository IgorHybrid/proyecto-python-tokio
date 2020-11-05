from flask import render_template, Blueprint
from app.controllers.auth import login_required


blueprint = Blueprint('home', __name__)


@blueprint.route('/')
@login_required
def home():
    return render_template('home.html')