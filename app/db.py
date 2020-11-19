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
    user_col = db['user']
    product_col = db['product']

    role_col.drop()
    user_col.drop()
    product_col.drop()

    from app.models.role import Role
    from app.models.user import User
    from app.models.product import Product

    role = Role()
    user = User()
    product = Product()

    admin_role = role.create({"name": "admin"})
    cliente_role = role.create({"name": "cliente"})
    proveedor_role = role.create({"name": "proveedor"})

    user.create({"username": "admin", "password": "admin", "email":"admin@gmail.com", "_role":admin_role.inserted_id})
    user.create({"username": "cliente", "password": "cliente", "email": "cliente@gmail.com", "_role": cliente_role.inserted_id})
    proveedor = user.create({"username": "proveedor", "password": "proveedor", "email": "proveedor@gmail.com", "_role": proveedor_role.inserted_id})

    product.create({
        "name": "Intel Core i5-1130G7",
        "description": "Procesador Intel Core",
        "place": "Galdakao(Bizkaia)",
        "price": 100.00,
        "shopPrice": 129.99,
        "maxStock": 320,
        "currentStock": 200,
        "_owner": proveedor.inserted_id
    })

    product.create({
        "name": "NZXT Aer RGB 2 120mm",
        "description": "Ventilador con LED",
        "place": "Galdakao(Bizkaia)",
        "price": 20.00,
        "shopPrice": 29.99,
        "maxStock": 320,
        "currentStock": 300,
        "colors": ["verde", "rojo", "morado"],
        "_owner": proveedor.inserted_id
    })

def init_app(app):
    app.cli.add_command(init_db_command)


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')
