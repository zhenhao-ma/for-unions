import os

from flask import Flask
from flask import (
    redirect, url_for
)

from . import db, rag, llm
from .view import auth, content, chat, wechat


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    app.logger.warning(f"Path of app instance is: {app.instance_path}")

    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=False)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # create rag instance
    app.config['rag'] = rag.get_werag(app)

    # add db command to app
    db.init_app(app)

    # create default user
    db.init_db_with_default_user(app)

    # register blueprint
    app.register_blueprint(auth.bp)
    app.register_blueprint(content.bp)
    app.register_blueprint(chat.bp)
    app.register_blueprint(wechat.bp)

    # home
    @app.route('/')
    def index():
        return redirect(url_for('content.edit'))

    return app


if __name__ == "__main__":
    # Only for debugging while developing
    create_app().run(host='0.0.0.0', port=80)
