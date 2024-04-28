

from flask import current_app
from langchain_openai import AzureChatOpenAI


def get_llm():
    return AzureChatOpenAI(temperature=0,
                           azure_deployment=current_app.config["AZURE_GPT35_MODEL"],
                           azure_endpoint=current_app.config['AZURE_GPT35_MODEL_API_BASE'],
                           api_version=current_app.config['AZURE_API_VERSION'],
                           api_key=current_app.config['AZURE_GPT35_MODEL_API_TOKEN'],
                           )
