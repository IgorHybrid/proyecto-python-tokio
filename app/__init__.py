import logging

from flask import Flask, request as req


def create_app(config_filename=None):
    app = Flask(__name__, instance_relative_config=True)

    if config_filename is None:
        config_filename = 'config.development'

    app.config.from_object(config_filename)

    from . import db
    db.init_app(app)

    app = init_bp(app)

    app.logger.setLevel(logging.NOTSET)

    @app.after_request
    def log_response(resp):
        app.logger.info("{} {} {}\n{}".format(
            req.method, req.url, req.data, resp)
        )
        return resp

    return app


def init_bp(app_flask):
    with app_flask.app_context():
        from app.controllers import home
        from app.controllers import auth
        from app.controllers import products

        app_flask.register_blueprint(home.blueprint)
        app_flask.register_blueprint(auth.blueprint)
        app_flask.register_blueprint(products.blueprint)

        return app_flask