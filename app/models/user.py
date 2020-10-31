from app.models.factory.validator import Validator
from app.models.factory.database import Database

from werkzeug.security import check_password_hash, generate_password_hash

class User(object):
    def __init__(self):

        self.validator = Validator()
        self.db = Database()

        self.collection_name = 'user'
        self.fields = {
            "username": "string",
            "password": "string",
            "email": "string",
            "_role": "objectid"
        }

        self.create_required_fields = ["username", "password", "email", "_role"]

        # Fields optional for CREATE
        self.create_optional_fields = []

        # Fields required for UPDATE
        self.update_required_fields = []

        # Fields optional for UPDATE
        self.update_optional_fields = []


    def create(self, user):
        # Validator will throw error if invalid
        user["password"] = generate_password_hash(user["password"])
        self.validator.validate(user, self.fields, self.create_required_fields, self.create_optional_fields)
        res = self.db.insert(user, self.collection_name)
        return res


    def find(self, user, projection=None):  # find all
        return self.db.find(user, self.collection_name, projection)


    def find_by_id(self, id):
        return self.db.find_by_id(id, self.collection_name)


    def update(self, id, user):
        self.validator.validate(user, self.fields, self.update_required_fields, self.update_optional_fields)
        return self.db.update(id, user, self.collection_name)


    def delete(self, id):
        return self.db.delete(id, self.collection_name)