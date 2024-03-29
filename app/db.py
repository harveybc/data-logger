import sqlite3

import click
from flask import current_app
from flask import g
from flask.cli import with_appcontext
import os


def get_db():
    """Connect to the application's configured database. The connection
    is unique for each request and will be reused if this is called
    again.
    """
    #with app.app_context():
    #    if "db" not in current_app.g:
    #        basedir = os.path.dirname("setup.py")
    #        g.db = sqlite3.connect(
    #            os.path.join(basedir, 'db.sqlite3'), detect_types=sqlite3.PARSE_DECLTYPES
    #        )
    #        g.db.row_factory = sqlite3.Row
    #        print("Warning: db is not in g, using db.sqlite3 as database")
    #    return g.db
    if "db" not in g:
        basedir = os.path.dirname("setup.py")
        g.db = sqlite3.connect(
            os.path.join(basedir, 'db.sqlite3'), detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
        print("Warning: db is not in g, using db.sqlite3 as database")
    return g.db

def close_db(e=None):
    """If this request connected to the database, close the
    connection.
    """
    db = g.pop("db", None)

    if db is not None:
        db.close()


def init_db():
    """Clear existing data and create new tables."""
    db = get_db()

    with current_app.open_resource("schema.sql") as f:
        db.executescript(f.read().decode("utf8"))


@click.command("init-db")
@with_appcontext
def init_db_command():
    """Clear existing data and create new tables."""
    init_db()
    click.echo("Initialized the database.")


def init_app(app):
    """Register database functions with the Flask app. This is called by
    the application factory.
    """
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
