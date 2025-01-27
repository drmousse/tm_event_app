#!/usr/bin/python3
# -*- coding: utf-8

# core imports
from sqlalchemy import String, DateTime, Integer, exc

# custom imports
import tioglobals
from . import TioDB


# classes
class Message(TioDB.db.Model):
    __tablename__ = 'tio_message'
    __classname__ = 'tio_message'

    message_id = TioDB.db.Column(String(tioglobals.LENGTH_ID), primary_key=True)
    parent_message_id = TioDB.db.Column(String(tioglobals.LENGTH_ID))
    message_number = TioDB.db.Column(Integer)
    object_id = TioDB.db.Column(String(tioglobals.LENGTH_ID))
    user_id = TioDB.db.Column(String(tioglobals.LENGTH_ID))
    user_name = TioDB.db.Column(String(100))
    message_type = TioDB.db.Column(String(15))
    content = TioDB.db.Column(String(10000))
    created_on = TioDB.db.Column(DateTime)
    edited_on = TioDB.db.Column(DateTime)

    @classmethod
    def ByKeys(cls, message_id):
        try:
            return TioDB.db.session.execute(TioDB.db.select(cls).filter_by(message_id=message_id)).scalar_one()
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
        messages = cls.query.all()
        return messages

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

    def convert_to_dict(self):
        return {col.name: getattr(self, col.name) for col in self.__table__.columns}
