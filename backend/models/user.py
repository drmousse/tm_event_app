#!/usr/bin/python3
# -*- coding: utf-8

# core imports
from sqlalchemy import String, DateTime, Integer, exc


# custom imports
import tioglobals
from . import TioDB


# classes
class User(TioDB.db.Model):
    __tablename__ = 'tio_user'
    __classname__ = 'tio_user'

    login = TioDB.db.Column(String(50), primary_key=True)
    user_id = TioDB.db.Column(String(tioglobals.LENGTH_ID), nullable=False)
    firstname = TioDB.db.Column(String(50), nullable=False)
    lastname = TioDB.db.Column(String(50), nullable=False)
    email = TioDB.db.Column(String(50))
    phone = TioDB.db.Column(String(50))
    gender = TioDB.db.Column(String(1))
    title = TioDB.db.Column(String(10))
    function = TioDB.db.Column(String(30))
    pw_last_changed = TioDB.db.Column(DateTime)
    active = TioDB.db.Column(Integer)
    first_login = TioDB.db.Column(Integer)
    profile_blob_id = TioDB.db.Column(String(tioglobals.LENGTH_ID))

    # CLASS METHODS
    @classmethod
    def ByKeys(cls, login):
        try:
            return TioDB.db.session.execute(TioDB.db.select(cls).filter_by(login=login)).scalar_one()
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
    def GetUserByID(cls, user_id):
        return cls.KeywordQuery(user_id=user_id)[0]

    @classmethod
    def Query(cls):
        all_users = cls.query.all()
        _users = []
        for user in all_users:
            _users.append({
                'userId': user.user_id,
                'firstname': user.firstname,
                'lastname': user.lastname,
                'email': user.email,
                'phone': user.phone,
                'gender': user.gender,
                'title': user.title,
                'function': user.function,
                'profileBlobId': user.profile_blob_id,
                'active': user.active,
            })

        return _users

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

    def get_full_name(self):
        return '{} {}'.format(self.firstname, self.lastname)
