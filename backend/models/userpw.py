#!/usr/bin/python3
# -*- coding: utf-8

# core imports
import bcrypt
from sqlalchemy import String, BINARY, exc

# custom imports
import tioglobals
import tools
from . import TioDB


# classes
class UserPW(TioDB.db.Model):
    __tablename__ = 'tio_user_pw'
    __classname__ = 'tio_user_pw'

    user_id = TioDB.db.Column(String(tioglobals.LENGTH_ID), primary_key=True)
    user_pw = TioDB.db.Column(BINARY(70))

    @classmethod
    def ByKeys(cls, user_id):
        try:
            return TioDB.db.session.execute(TioDB.db.select(cls).filter_by(user_id=user_id)).scalar_one()
        except exc.NoResultFound:
            return None

    @classmethod
    def KeywordQuery(cls, **kwargs):
        obj = []
        _objs = TioDB.db.session.execute(TioDB.db.select(cls).filter_by(**kwargs)).all()
        for _o in _objs:
            obj.append(_o[0])

        return obj

    @classmethod
    def Query(cls):
        raise NotImplemented

    # INSTANCE METHODS
    def update(self, key, value):
        """
        This method is used to update a value in database and commit it immediately.
        :param key: str
        :param value: str | int | float | datetime.datetime
        :return: None
        """
        setattr(self, key, value)
        TioDB.db.session.commit()

    def commit(self):
        """
        This method is used to commit changes to the database.
        Especially useful if multiple changes were made, so you only have to commit once.
        :return: None
        """
        TioDB.db.session.commit()

    def update_pw(self, password):
        self.user_pw = tools.hash_pw(password)
        self.commit()
