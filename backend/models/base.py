#!/usr/bin/python3
# -*- coding: utf-8
#
# copyright (c) 2024 Mustafa Caglar

# core imports
import os
from sqlalchemy import event
from dotenv import load_dotenv
from sqlalchemy.orm import DeclarativeBase
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS


# globals
load_dotenv()

TIO_DB_USER = os.getenv('TIO_DB_USER')
TIO_DB_PW = os.getenv('TIO_DB_PW')
TIO_DB_SCHEMA = os.getenv('TIO_DB_SCHEMA')
MYSQL_ON = int(os.getenv('MYSQL_ON'))
TIO_API_APP_KEY = os.getenv('TIO_API_APP_KEY')


# classes
class Base(DeclarativeBase):
    pass


class TioDB:
    __classname__ = 'TioDB'
    db = SQLAlchemy(model_class=Base)
    app = Flask(__name__)
    cors = CORS(app, supports_credentials=True, origins=['*'])
    app.config['TIO_API_APP_KEY'] = TIO_API_APP_KEY
    app.config['UPLOAD_FOLDER'] = 'event_app/frontend/public/media'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    migrate = Migrate(app, db)
    if MYSQL_ON:
        app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{TIO_DB_USER}:{TIO_DB_PW}@localhost/{TIO_DB_SCHEMA}'
    else:
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///../tio_event.db"
    db.init_app(app)

    # Enable WAL mode for SQLite
    @classmethod
    def set_sqlite_wal_mode(cls):
        # Enable WAL mode for SQLite
        @event.listens_for(cls.db.engine, "connect")
        def set_sqlite_pragma(dbapi_connection, connection_record):
            cursor = dbapi_connection.cursor()
            cursor.execute("PRAGMA journal_mode=WAL")
            cursor.close()

    @classmethod
    def run(cls):
        from waitress import serve
        # Ensure the context is pushed before setting PRAGMA
        with cls.app.app_context():
            cls.set_sqlite_wal_mode()
        serve(cls.app, host='localhost', port=1337)

    @classmethod
    def add_object(cls, obj):
        cls.db.session.add(obj)
        cls.db.session.commit()

    @classmethod
    def add_objects(cls, objs):
        # todo: error handling
        if isinstance(objs, str):
            cls.add_object(objs)
        else:
            cls.db.session.add_all(objs)
            cls.db.session.commit()

    @classmethod
    def commit(cls):
        cls.db.session.commit()
