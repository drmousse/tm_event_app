#!/usr/bin/python3
# -*- coding: utf-8

# core imports
from sqlalchemy import String, DateTime, Integer, BINARY, Date, exc

# custom imports
import tioglobals
from . import TioDB


# classes
class Event(TioDB.db.Model):
    __tablename__ = 'tio_event'
    __classname__ = 'tio_event'

    event_id = TioDB.db.Column(String(tioglobals.LENGTH_ID), primary_key=True)
    event_lead_id = TioDB.db.Column(String(tioglobals.LENGTH_ID))
    creator_id = TioDB.db.Column(String(tioglobals.LENGTH_ID))
    event_code = TioDB.db.Column(BINARY(70))
    customer = TioDB.db.Column(String(200), nullable=False)
    event_date = TioDB.db.Column(Date, nullable=False)
    event_format = TioDB.db.Column(String(200), nullable=False)
    multi_mode = TioDB.db.Column(String(6))
    description = TioDB.db.Column(String(500))
    created_at = TioDB.db.Column(DateTime)
    start_fcast = TioDB.db.Column(DateTime)
    end_fcast = TioDB.db.Column(DateTime)
    start_actual = TioDB.db.Column(DateTime)
    end_actual = TioDB.db.Column(DateTime)
    status = TioDB.db.Column(Integer)
    status_type = TioDB.db.Column(String(tioglobals.LENGTH_STATUS_TYPE))
    event_blob_id = TioDB.db.Column(String(tioglobals.LENGTH_ID))
    greeting_duration = TioDB.db.Column(Integer)
    challenges_duration = TioDB.db.Column(Integer)
    transfer_duration = TioDB.db.Column(Integer)
    ceremony_duration = TioDB.db.Column(Integer)
    station_duplicates = TioDB.db.Column(Integer)
    num_teams = TioDB.db.Column(Integer)
    group_distribution = TioDB.db.Column(String(300))

    # CLASS METHODS
    @classmethod
    def ByKeys(cls, event_id):
        try:
            return TioDB.db.session.execute(TioDB.db.select(cls).filter_by(event_id=event_id)).scalar_one()
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
        return TioDB.db.session.execute(TioDB.db.select(cls)).all()

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
