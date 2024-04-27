import functools
import logging

from flask import (
    g
)
from flask import (
    redirect, url_for
)

logger = logging.getLogger(__name__)


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view

# from flask import current_app
# from langchain_openai import AzureChatOpenAI
#
#
# def get_llm():
#     return AzureChatOpenAI(temperature=0,
#                            azure_deployment=current_app.config["AZURE_GPT35_MODEL"],
#                            azure_endpoint=current_app.config['AZURE_GPT35_MODEL_API_BASE'],
#                            api_version=current_app.config['AZURE_API_VERSION'],
#                            api_key=current_app.config['AZURE_GPT35_MODEL_API_TOKEN'],
#                            )
