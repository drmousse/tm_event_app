#!/usr/bin/python3
# -*- coding: utf-8

# core imports
from sqlalchemy import String

# custom imports
import tioglobals
from . import TioDB


# classes
class UserSettings(TioDB.db.Model):
    __tablename__ = 'tio_user_settings'
    __classname__ = 'tio_user_settings'

    setting_id = TioDB.db.Column(String(20), primary_key=True)
    user_id = TioDB.db.Column(String(tioglobals.LENGTH_ID), primary_key=False)
    value = TioDB.db.Column(String(50))

    @classmethod
    def ByKeys(cls, setting_id, user_id):
        return cls.query.filter_by(setting_id=setting_id, user_id=user_id).first()

    @classmethod
    def KeywordQuery(cls, **kwargs):
        all_user_settings = cls.query.filter_by(**kwargs).all()
        u_settings = []
        for user_setting in all_user_settings:
            u_settings.append({'setting_id': user_setting.setting_id, 'value': user_setting.value})
        return u_settings

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

    def convert_to_dict(self):
        return {col.name: getattr(self, col.name) for col in self.__table__.columns}
