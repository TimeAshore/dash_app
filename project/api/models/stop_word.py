from sqlalchemy import Column, String
from .base import db, BaseColumns


class StopWord(db.Model, BaseColumns):
    __tablename__ = "stop_word"

    word = Column(String(200), unique=True, nullable=False, server_default='')

    def as_dict(self, **kwargs):
        return {'id': self.id, 'word': self.word}
