import sqlite3

import click
from flask import current_app, g
from werkzeug.security import generate_password_hash

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        # g.db.row_factory = sqlite3.Row
        g.db.row_factory = dict_factory

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db(admin_user: str, admin_password: str):
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

    try:
        db.execute(
            "INSERT INTO user (username, password, contents, urls) VALUES (?, ?, ?, ?)",
            (admin_user, generate_password_hash(admin_password), "", ""),
        )
        db.commit()
    except db.IntegrityError:
        pass
    except Exception as e:
        raise e


def init_db_with_default_user(app):
    app.app_context().push()
    db = get_db()
    default_username = "guest"
    default_password = "guest"

    try:
        first_user = db.execute(
            'SELECT * FROM user WHERE id = ?', (1,)
        ).fetchone()
        if first_user is None:
            db.execute(
                "INSERT INTO user (username, password, contents, urls) VALUES (?, ?, ?)",
                (default_username, generate_password_hash(default_password), "", ""),
            )
            db.commit()
            app.logger.info(F"Created a default account. Username: {default_username}; Password: {default_password}")
    except Exception as e:
        pass



@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    admin_user: str = click.prompt('Creating admin user, please enter your username', type=str)
    admin_password: str = click.prompt('please enter your password', type=str)
    init_db(admin_user, admin_password)
    click.echo('Initialized the database.')


def init_app(app):
    """allow app use command to init database"""
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
