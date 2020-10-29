from flask import Blueprint, jsonify, request

from app.models.role import Role

blueprint = Blueprint('role', __name__)


role = Role()

@blueprint.route('/role/insert', methods=['POST'])
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