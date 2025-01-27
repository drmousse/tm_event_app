#!/usr/bin/python3
# -*- coding: utf-8

# core imports
from sqlalchemy import String, Integer, exc

# custom imports
import tioglobals
from . import TioDB


# classes
class Games(TioDB.db.Model):
    __tablename__ = 'tio_games'
    __classname__ = 'tio_games'

    name = TioDB.db.Column(String(100), primary_key=True)
    game_id = TioDB.db.Column(String(tioglobals.LENGTH_ID), unique=True)
    description = TioDB.db.Column(String(10000))
    score_type = TioDB.db.Column(String(5), nullable=False)
    score_counting = TioDB.db.Column(String(12), nullable=False)
    duration = TioDB.db.Column(Integer, nullable=False)
    game_blob_id = TioDB.db.Column(String(tioglobals.LENGTH_ID))
    active = TioDB.db.Column(Integer)

    @classmethod
    def ByKeys(cls, name):
        try:
            return TioDB.db.session.execute(TioDB.db.select(cls).filter_by(name=name)).scalar_one()
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
        all_games = cls.query.all()
        _games = []
        for game in all_games:
            _games.append({
                'name': game.name,
                'gameID': game.game_id,
                'description': game.description,
                'scoreType': game.score_type,
                'scoreCounting': game.score_counting,
                'duration': game.duration,
                'gameBlobId': game.game_blob_id,
                'active': game.active
            })

        return _games

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
