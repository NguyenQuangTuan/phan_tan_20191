import json
import operator

from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
from marshmallow import ValidationError
from phan_tan.common.errors import (
    UPermissionDenied, UNotFound, UUnprocessableEntity
)
from phan_tan.common.helpers import empty_obj


db = empty_obj()


def init_app(app_name=__name__):
    from database_new import db_engine, db_flask_session
    load_dotenv()

    # Config App
    app = Flask(app_name, instance_relative_config=True)
    app.url_map.strict_slashes = False
    CORS(app)

    # Config DB
    engine = db_engine()
    db_flask_session.configure(bind=engine)
    db.session_factory = db_flask_session

    __config_blueprints(app)
    _config_error_handlers(app)
    _config_cli(app)

    return app


def __config_blueprints(app):
    def _config_api(app):
        from phan_tan.apps.apis import app_api
        app.register_blueprint(app_api, url_prefix='/api/group8')

    handle_exception = app.handle_exception
    handle_user_exception = app.handle_user_exception

    _config_api(app)

    app.handle_exception = handle_exception
    app.handle_user_exception = handle_user_exception


def _config_error_handlers(app):
    """
    Inspired by
    http://flask.pocoo.org/docs/latest/errorhandling/
    https://httpstatuses.com/
    """
    @app.errorhandler(ValidationError)
    def validation_error_handler(error):
        # TODO: Should change the error message format in future
        return json.dumps(
            {
                'error': 'Bad request',
                'messages': error.messages
            }
        ), 400

    @app.errorhandler(500)
    def server_error_page(error):
        return json.dumps({'error': 'Internal server error'}), 500

    @app.errorhandler(UPermissionDenied)
    def permission_denied(error):
        return json.dumps({'error': 'Permission denied'}), 401

    @app.errorhandler(UNotFound)
    def not_found(error):
        error_message = str(error) or 'Resource not found'
        return json.dumps({'error': error_message}), 404

    @app.errorhandler(UUnprocessableEntity)
    def unprocessable_entity(error):
        error_message = str(error) or 'Unprocessable Entity'
        return json.dumps({'error': error_message}), 422


def _config_cli(app):
    @app.cli.command()
    def initdb():
        print('init db - sample cli')

    @app.cli.command()
    def routes():
        """Display registered routes"""
        rules = []
        for rule in app.url_map.iter_rules():
            methods = ','.join(sorted(rule.methods))
            rules.append((rule.endpoint, methods, str(rule)))

        sort_by_rule = operator.itemgetter(2)
        for endpoint, methods, rule in sorted(rules, key=sort_by_rule):
            route = '{:50s} {:25s} {}'.format(endpoint, methods, rule)
            print(route)
