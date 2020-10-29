from app.models.factory.validator import Validator
from app.models.factory.database import Database


class Role(object):
    def __init__(self):

        self.validator = Validator()
        self.db = Database()

        self.collection_name = 'role'
        self.fields = {
            "name": "string"
        }

        self.create_required_fields = ["name"]

        # Fields optional for CREATE
        self.create_optional_fields = []

        # Fields required for UPDATE
        self.update_required_fields = ["name"]

        # Fields optional for UPDATE
        self.update_optional_fields = []


    def create(self, role):
        # Validator will throw error if invalid
        self.validator.validate(role, self.fields, self.create_required_fields, self.create_optional_fields)
        res = self.db.insert(role, self.collection_name)
        return res


    def find(self, role, projection=None):  # find all
        return self.db.find(role, self.collection_name, projection)


    def find_by_id(self, id):
        return self.db.find_by_id(id, self.collection_name)


    def update(self, id, role):
        self.validator.validate(role, self.fields, self.update_required_fields, self.update_optional_fields)
        return self.db.update(id, role, self.collection_name)


    def delete(self, id):
        return self.db.delete(id, self.collection_name)