# set token or get from environments

from flask import (
    Blueprint, request, current_app, abort
)
from wechatpy.exceptions import (
    InvalidSignatureException,
    InvalidAppIdException,
)
from wechatpy.utils import check_signature

from app import llm
from app.db import get_db

bp = Blueprint('wechat', __name__, url_prefix='/wechat')


@bp.route("/", methods=["GET", "POST"])
def wechat():
    WECHAT_TOKEN = current_app.config['WECHAT_TOKEN']
    WECHAT_AES_KEY = current_app.config['WECHAT_AES_KEY']
    WECHAT_APPID = current_app.config['WECHAT_APPID']

    first_user = get_db().execute(
        'SELECT * FROM user WHERE id = ?', ("1",)
    ).fetchone()

    signature = request.args.get("signature", "")
    timestamp = request.args.get("timestamp", "")
    nonce = request.args.get("nonce", "")
    encrypt_type = request.args.get("encrypt_type", "raw")
    msg_signature = request.args.get("msg_signature", "")

    prompt_template = """
    ### [INST] 
    Instruction: """ + current_app.config['PROMPT_INSTRUCTION'] + f"""\n{first_user['contents']}\n""" + """
    {context}

    ### QUESTION:
    {question} 

    [/INST]
    """

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
        return current_app.config['rag'].response_wechat_xml(message=request.data, llm=llm.get_llm(),
                                                             user=str(first_user['id']),
                                                             prompt_template=prompt_template)
    else:
        # encryption mode
        from wechatpy.crypto import WeChatCrypto

        crypto = WeChatCrypto(WECHAT_TOKEN, WECHAT_AES_KEY, WECHAT_APPID)
        try:
            msg = crypto.decrypt_message(request.data, msg_signature, timestamp, nonce)
        except (InvalidSignatureException, InvalidAppIdException):
            abort(403)
        else:
            return crypto.encrypt_message(
                current_app.config['rag'].response_wechat_xml(message=msg, llm=llm.get_llm(), user=str(1),
                                                              prompt_template=prompt_template), nonce, timestamp)
