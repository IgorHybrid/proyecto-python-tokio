from app.models.factory.validator import Validator
from app.models.factory.database import Database


class Product(object):
    def __init__(self):
        self.validator = Validator()
        self.db = Database()

        self.collection_name = 'product'
        self.fields = {
            "name": "string",
            "description": "string",
            "place": "string",
            "price": "float",
            "shopPrice": "float",
            "currentStock": "int",
            "maxStock": "int",
            "colors": ["string"],
            "_owner": "objectid"
        }

        self.create_required_fields = ["name", "description", "place", "price", "_owner", "currentStock", "maxStock"]

        # Fields optional for CREATE
        self.create_optional_fields = ["colors", "shopPrice"]

        # Fields required for UPDATE
        self.update_required_fields = []

        # Fields optional for UPDATE
        self.update_optional_fields = []

    def create(self, product):
        # Validator will throw error if invalid
        self.validator.validate(product, self.fields, self.create_required_fields, self.create_optional_fields)
        res = self.db.insert(product, self.collection_name)
        return res

    def find(self, product, projection=None):  # find all
        return self.db.find(product, self.collection_name, projection)

    def find_by_id(self, id):
        return self.db.find_by_id(id, self.collection_name)

    def update(self, id, product):
        self.validator.validate(product, self.fields, self.update_required_fields, self.update_optional_fields)
        return self.db.update(id, product, self.collection_name)

    def delete(self, id):
        return self.db.delete(id, self.collection_name)