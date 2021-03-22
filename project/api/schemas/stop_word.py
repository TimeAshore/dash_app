from webargs import fields
from project.api.models import StopWord, db
from project.api.exceptions.customs import InvalidAPIRequest, RecordNotFound, RecordAlreadyExists


def word_id_in_db(word_id):
    if not db.session.query(StopWord).get(word_id):
        raise RecordNotFound('无此停用词')


def word_in_db(word):
    if db.session.query(StopWord).filter_by(word=word).first():
        raise RecordAlreadyExists('已有此关键词')


add_stop_word_schema = {
    'word': fields.Str(required=True, validate=word_in_db)
}

delete_stop_word_schema = {
    'id': fields.Int(required=True, validate=word_id_in_db)
}

