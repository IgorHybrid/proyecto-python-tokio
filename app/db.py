from pymongo import MongoClient

import click

from flask import current_app, g
from flask.cli import with_appcontext


def get_db():
    if 'db' not in g:
        g.mongo_client = MongoClient(current_app.config["MONGO_HOSTNAME"], current_app.config["MONGO_PORT"])
        g.db = g.mongo_client[current_app.config["MONGO_APP_DATABASE"]]
    return g.db


def init_db():
    db = get_db()

    role_col = db['role']

    role_col.drop()

    from app.models.role import Role
    from app.models.user import User

    role = Role()
    user = User()

    admin = role.create({"name": "admin"})
    cliente = role.create({"name": "cliente"})
    proveedor = role.create({"name": "proveedor"})

    user.create({"username": "admin", "password": "admin", "email":"admin@gmail.com", "_role":admin.inserted_id})
    user.create({"username": "cliente", "password": "cliente", "email": "cliente@gmail.com", "_role": cliente.inserted_id})
    user.create({"username": "proveedor", "password": "proveedor", "email": "proveedor@gmail.com", "_role": proveedor.inserted_id})
def init_app(app):
    app.cli.add_command(init_db_command)


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')
