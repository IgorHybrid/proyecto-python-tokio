from flask_script import Manager
from app import create_app

app = create_app('config.development')
manager = Manager(app)

if __name__ == '__main__':
    app.secret_key = 'super secret key'
    manager.run()