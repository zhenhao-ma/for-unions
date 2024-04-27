import os

from werag import WeRag


def get_werag(app):

    __import__('pysqlite3')
    import sys
    sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

    folder = os.path.join(app.instance_path, "werag")
    return WeRag(
        persist_directory=folder,
        collection_name="werag",
        chunk_size=4000,
        chunk_overlap=2000
    )
