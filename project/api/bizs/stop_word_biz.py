from project.api.bizs.base import BaseBiz
from project.api.models import StopWord


class StopWordBiz(BaseBiz):

    def __init__(self):
        super().__init__()
        self.model = StopWord
        self.allow_query_all = True

    def get(self):
        words = self.session.query(StopWord).all()
        data = [obj.word for obj in words]
        return data

    def add(self, server_info):
        stop_word = StopWord(word=server_info['word'])
        self.session.add(stop_word)
        self.safe_commit()
        return {"停用词": stop_word.word}

    def delete(self, server_info):
        stop_word = self.find(id=server_info['id'])
        self.session.delete(stop_word)
        return self.safe_commit()
