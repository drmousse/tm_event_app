#!/usr/bin/python3
# -*- coding: utf-8

# core imports
from sqlalchemy import String, Integer, exc

# custom imports
import tioglobals
from . import TioDB


# classes
class EventRoundGroupDistribution(TioDB.db.Model):
    __tablename__ = 'tio_event_round_group_distribution'
    __classname__ = 'tio_event_round_group_distribution'

    event_id = TioDB.db.Column(String(tioglobals.LENGTH_ID), primary_key=True)
    game_id = TioDB.db.Column(String(tioglobals.LENGTH_ID), primary_key=True)
    group_name = TioDB.db.Column(String(1), primary_key=True)
    round_number = TioDB.db.Column(Integer, primary_key=True)
    position = TioDB.db.Column(Integer, primary_key=True)

    @classmethod
    def ByKeys(cls, event_id, group_name, round_number, position):
        try:
            return TioDB.db.session.execute(TioDB.db.select(cls).filter_by(event_id=event_id,
                                                                           group_name=group_name,
                                                                           round_number=round_number,
                                                                           position=position)).scalar_one()
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
        return cls.query.all()

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
