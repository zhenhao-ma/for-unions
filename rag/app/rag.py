import os
from typing import List
from typing import Optional

import tiktoken
from fake_useragent import UserAgent
from flask import current_app
from keble_helpers import inline_string
from langchain.document_transformers import Html2TextTransformer
from langchain_community.document_loaders import UnstructuredURLLoader
from langchain_community.document_loaders.recursive_url_loader import RecursiveUrlLoader
from langchain_core.documents import Document
from werag import WeRag

max_chunk_size = 2000
chunk_overlap = 500


def split_large_text(large_text, max_tokens):
    enc = tiktoken.get_encoding("cl100k_base")
    tokenized_text = enc.encode(large_text)

    chunks = []
    current_chunk = []
    current_length = 0

    for token in tokenized_text:
        current_chunk.append(token)
        current_length += 1

        if current_length >= max_tokens:
            chunks.append(enc.decode(current_chunk).rstrip(' .,;'))
            current_chunk = []
            current_length = 0

    if current_chunk:
        chunks.append(enc.decode(current_chunk).rstrip(' .,;'))

    return chunks


def split_documents(documents: List[Document]) -> List[Document]:
    final_docs = []
    for doc in documents:
        sp_texts = split_large_text(doc.page_content, max_tokens=max_chunk_size)
        print("sp_texts: ", len(sp_texts))
        final_docs += [Document(page_content=d) for d in sp_texts]
    return final_docs


def save_urls(werag, *, urls: List[str], user: str,

              content_type: Optional[str] = None, **kwargs):
    docs_transformed = []
    max_depth: int = 2

    def print_docs(documents: List[Document]):
        for doc in documents:
            current_app.logger.info(f"- Page content: {inline_string(doc.page_content)}")

    # Converts HTML to plain text
    html2text = Html2TextTransformer()

    for url in urls:
        header_template = {}
        header_template["User-Agent"] = UserAgent().random

        loader = RecursiveUrlLoader(url, max_depth=max_depth, headers=header_template, **kwargs)
        new_docs = loader.load()
        current_app.logger.warning(f"RecursiveUrlLoader found {len(new_docs)} docs on url: {url}")

        if len(new_docs) == 0 or new_docs is None:
            current_app.logger.warning(f"Use another loader on url: {url}")
            loader = UnstructuredURLLoader(urls=[url])
            new_docs = loader.load()
            if len(new_docs) == 0:
                current_app.logger.critical(f"Still found 0 docs on url: {url}")
            else:
                current_app.logger.warning(f"Successfully found {len(new_docs)} docs on url: {url}")
        transformed_new_docs = html2text.transform_documents(new_docs)
        print_docs(transformed_new_docs)
        docs_transformed += transformed_new_docs
    split_docs = split_documents(docs_transformed)
    current_app.logger.warning(
        f"Totally found {len(docs_transformed)} (and split into {len(split_docs)}) docs on urls: " + ' ; '.join(urls))

    werag.save_documents(user=user, documents=split_docs, content_type=content_type)

__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

def get_werag(app):
    folder = os.path.join(app.instance_path, "werag")

    return WeRag(
        persist_directory=folder,
        collection_name="werag",
        chunk_size=6000, # to ensure the strings of user_content does not split. so this can be larger than the variable max_chunk_size
        chunk_overlap=chunk_overlap
    )
