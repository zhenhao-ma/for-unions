import os

from flask import Flask
from flask import (
    redirect, url_for, request, abort
)
from wechatpy.exceptions import (
    InvalidSignatureException,
    InvalidAppIdException,
)
from wechatpy.utils import check_signature

from . import db, rag
from .view import auth, content, chat


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
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

    # home
    @app.route('/')
    def index():
        return redirect(url_for('content.edit'))

    # set token or get from environments
    WECHAT_TOKEN = app.config['WECHAT_TOKEN']
    WECHAT_AES_KEY = app.config['WECHAT_AES_KEY']
    WECHAT_APPID = app.config['WECHAT_APPID']

    # wechat api
    @app.route("/wechat", methods=["GET", "POST"])
    def wechat():
        signature = request.args.get("signature", "")
        timestamp = request.args.get("timestamp", "")
        nonce = request.args.get("nonce", "")
        encrypt_type = request.args.get("encrypt_type", "raw")
        msg_signature = request.args.get("msg_signature", "")
        try:
            check_signature(WECHAT_TOKEN, signature, timestamp, nonce)
        except InvalidSignatureException:
            abort(403)
        if request.method == "GET":
            echo_str = request.args.get("echostr", "")
            return echo_str

        # POST request
        if encrypt_type == "raw":
            # plaintext mode
            return app.config['rag'].response_wechat_xml(request.data)
        else:
            # encryption mode
            from wechatpy.crypto import WeChatCrypto

            crypto = WeChatCrypto(WECHAT_TOKEN, WECHAT_AES_KEY, WECHAT_APPID)
            try:
                msg = crypto.decrypt_message(request.data, msg_signature, timestamp, nonce)
            except (InvalidSignatureException, InvalidAppIdException):
                abort(403)
            else:
                return crypto.encrypt_message(app.config['rag'].response_wechat_xml(msg), nonce, timestamp)

    return app


if __name__ == "__main__":
    # Only for debugging while developing
    create_app().run(host='0.0.0.0', port=80)
