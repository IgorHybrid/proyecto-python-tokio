from flask import render_template, Blueprint, request, flash, redirect, url_for, g
from app.controllers.auth import login_required
from bson import ObjectId


blueprint = Blueprint('products', __name__, url_prefix='/products')

from app.models.product import Product
from app.forms import AddProductForm


@blueprint.route('/list')
@login_required
def list_products():
    product = Product()
    products_list = product.find(None)

    return render_template('products.html', products=products_list)


@blueprint.route('/add', methods=['GET', 'POST'])
@login_required
def add_product():
    product = Product()
    form = AddProductForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        description = form.description.data
        place = form.place.data
        price = form.price.data
        max_stock = form.max_stock.data
        colors = form.colors.data

        try:
            product_fields = {
                "name": name,
                "description": description,
                "place": place,
                "price": price,
                "shopPrice": round(price + (price * 0.2), 2),
                "currentStock": 0,
                "maxStock": set_stock(max_stock),
                "colors": colors,
                "_owner": ObjectId(g.user["_id"])
            }

            product.create(product_fields)

            return redirect(url_for('products.list_products'))
        except Exception as e:
            flash(str(e), 'danger')
    return render_template('add_product.html', form=form)


@blueprint.route('/<int:id>/delete', methods=['POST'])
@login_required
def delete_product(id):
    return True



def set_stock(size):
    stock = 100
    if size == "small":
        stock = 320
    elif size == "large":
        stock = 50
    return stock