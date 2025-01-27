#!/usr/bin/python3
# -*- coding: utf-8

# core imports
from sqlalchemy import String, Integer, DateTime, Float

# custom imports
import tioglobals
from . import TioDB


# classes
class GameStation(TioDB.db.Model):
    __tablename__ = "tio_game_station"
    __classname__ = 'tio_game_station'

    game_station_id = TioDB.db.Column(String(tioglobals.LENGTH_ID), primary_key=True)
    event_id = TioDB.db.Column(String(tioglobals.LENGTH_ID), primary_key=True)
    game_id = TioDB.db.Column(String(tioglobals.LENGTH_ID), primary_key=True)
    game_no = TioDB.db.Column(Integer, nullable=False)
    team_a_id = TioDB.db.Column(String(tioglobals.LENGTH_ID), primary_key=True)
    team_b_id = TioDB.db.Column(String(tioglobals.LENGTH_ID), primary_key=True)
    status = TioDB.db.Column(Integer)
    status_type = TioDB.db.Column(String(tioglobals.LENGTH_STATUS_TYPE))
    game_start = TioDB.db.Column(DateTime)
    game_end = TioDB.db.Column(DateTime)
    game_duration = TioDB.db.Column(Float)
    station_lead_id = TioDB.db.Column(String(tioglobals.LENGTH_ID), nullable=False)
    num_rounds = TioDB.db.Column(Integer)
    group_name = TioDB.db.Column(String(1))

    @classmethod
    def ByKeys(cls, counter_name):
        raise NotImplemented

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

    @classmethod
    def GetStationLeadIDs(cls, event_id):
        game_stations = cls.KeywordQuery(event_id=event_id)
        return {gs.station_lead_id for gs in game_stations}

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
