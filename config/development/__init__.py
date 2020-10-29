import os

DEBUG = True
ENVIRONMENT = "development"
HOST = 'localhost'
PORT = int(os.environ.get('PORT', 5000))

## DATABASE
MONGO_HOSTNAME = "localhost"
MONGO_PORT = 27017
MONGO_APP_DATABASE = "proyecto"