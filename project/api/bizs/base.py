from flask import current_app
from sqlalchemy import func
from sqlalchemy.exc import DatabaseError, SQLAlchemyError

from ..models import db
from ..exceptions.customs import DatabaseError as DBError


class BaseBiz:

    def __init__(self):
        self.model = None
        self.session = db.session
        self.allow_query_all = False

    @property
    def fields(self):
        return []

    def find(self, **kwargs):
        return self.session.query(self.model).filter_by(**kwargs).first()

    def delete(self, **kwargs):
        return self.session.query(self.model).filter_by(**kwargs).delete()

    def query(self, **kwargs):
        query = self.session.query(self.model)
        return self.base_query(query, **kwargs)

    def base_query(self, query, **kwargs):
        total_count = self.query_count(query)
        query = self._build_query_filter(query, kwargs.get('filter', {}), strict=kwargs.get('strict'))
        query = self._build_query_order(query, kwargs.get('order', {}))
        filter_count = self.query_count(query)
        data = self._query_with_pagination(query, kwargs.get('page', 0), kwargs.get('size', 15))
        json_data = self._build_json_data(data, filter_count, total_count, **kwargs)

        return json_data

    @staticmethod
    def query_count(query):
        count_query = query.statement.with_only_columns([func.count()]).order_by(None)
        count = query.session.execute(count_query).scalar()

        return count

    def _query_with_pagination(self, query, page=1, size=10):
        if page == -1 and self.allow_query_all:
            return query.all()

        start = (page - 1) * size
        length = size
        if start < 0 or length < 0:
            start = 0
            length = 15
        data = query.slice(start, start + length).all()
        return data

    def _build_json_data(self, data, filter_count, total_count, fields=None, **kwargs):

        return {
            "records": [self.trans2dict(obj, fields=fields, **kwargs) for obj in data],
            "total_count": total_count,
            "filter_count": filter_count
        }

    @staticmethod
    def _build_query_filter(query, condition, strict=False):
        return query

    @staticmethod
    def trans2dict(obj, fields=None, **kwargs):
        return obj.as_dict(fields=fields)

    def _build_query_order(self, query, order):
        order_field, order_dir = order.get('field', 'update_time'), order.get('direction', 'desc')
        if order_field not in self.fields:
            order_field = 'update_time'
        obj_attr = getattr(self.model, order_field)
        return query.order_by(
            getattr(obj_attr, order_dir)()).order_by(self.model.id.desc())

    def safe_commit(self):
        try:
            self.session.commit()
        except (DatabaseError, SQLAlchemyError) as db_error:
            current_app.logger.error(db_error)
            self.session.rollback()
            raise DBError(str(db_error))

