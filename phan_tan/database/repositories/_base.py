from typing import Type
from sqlalchemy.orm import Session
from phan_tan.common.errors import UNotFound, UUnprocessableEntity
from phan_tan.database.models.base import Base
from sqlalchemy import exc


class CRUD:
    session: Type[Session] = None
    model: Type[Base] = None

    def find_by_id(self, model_id):
        q = self.session.query(self.model).filter(self.model.id == model_id)
        return q.first()

    def find(self, **conditions):
        query = self.session.query(self.model)
        for key, value in conditions.items():
            if isinstance(value, list):
                query = query.filter(getattr(self.model, key).in_(value))
                continue
            query = query.filter(getattr(self.model, key) == value)

        return query.all()

    def find_paging(self, limit=None, offset=None, **conditions):
        query = self.session.query(self.model)
        for key, value in conditions.items():
            if isinstance(value, list):
                query = query.filter(getattr(self.model, key).in_(value))
                continue
            query = query.filter(getattr(self.model, key) == value)

        if limit is not None and offset is not None:
            return query.count(), query.limit(limit).offset(offset).all()
        else:
            records = query.all()
            return len(records), records

    def first(self, **conditions):
        query = self.session.query(self.model)
        for key, value in conditions.items():
            if isinstance(value, list):
                query = query.filter(getattr(self.model, key).in_(value))
                continue
            query = query.filter(getattr(self.model, key) == value)

        return query.first()

    def first_or_fail(self, **condition):
        record = self.first(**condition)

        if record:
            return record
        raise UNotFound(f'{self.model.__name__} not found')

    def check_exist(self, **condition):
        record = self.first(**condition)

        if not record:
            return None
        raise UUnprocessableEntity(f'{self.model.__name__} is exist')

    def create(self, flush=True, mapping=None, **data):
        try:
            obj = self.model()
            for key in data:
                p = key
                if mapping and key in mapping:
                    p = mapping.get(key)

                if hasattr(obj, key):
                    setattr(obj, key, data[p])

            self.session.add(obj)
            if flush:
                self.session.flush()
            return obj
        except Exception as e:
            raise e

    def update(self, obj, flush=True, only=None, **data):
        if obj:
            for k in data:
                if hasattr(obj, k) and (only is None or k in only):
                    setattr(obj, k, data.get(k))
        if flush:
            self.session.flush()
        return obj

    def update_by_conditions(self, conditions={}, flush=True, **data):
        if not conditions:
            return None

        query = self.session.query(self.model)
        for key, value in conditions.items():
            if isinstance(value, list):
                query = query.filter(getattr(self.model, key).in_(value))
                continue
            query = query.filter(getattr(self.model, key) == value)
        obj = query.first()

        if obj:
            for k in data:
                if hasattr(obj, k):
                    setattr(obj, k, data.get(k))
        if flush:
            self.session.flush()
        return obj

    def delete(self, obj, flush=True):
        try:
            self.session.delete(obj)
            if flush:
                self.session.flush()
            return True
        except exc.IntegrityError as e:
            raise e
