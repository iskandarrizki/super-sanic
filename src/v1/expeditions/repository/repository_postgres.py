from sqlalchemy import select, func

from src.v1.expeditions.repository.repository import ExpeditionsRepository
from src.v1.model.expeditions import expeditions


class ExpeditionsRepositoryPSQL(ExpeditionsRepository):
    def __init__(self, db, tracer):
        self._db = db
        self._tracer = tracer
        super(ExpeditionsRepositoryPSQL, self).__init__()

    async def get_all(self, request_objects):
        query = select([expeditions]).limit(10).offset(0)

        with self._tracer.start_span('start_get_all_expedition') as span:
            span.log_kv({'event': 'test message'})
            span.set_tag('query', query)
            span.set_tag('param', request_objects)

        try:
            data = await self.db().fetch_all(query)
        except Exception as e:
            data = e

        return data

    async def get_total(self, request_objects):
        query = select([func.count()]).select_from(expeditions)
        with self._tracer.start_span('start_get_total_expedition') as span:
            span.log_kv({'event': 'test message'})
            span.set_tag('query', query)
            span.set_tag('param', request_objects)

        try:
            data = await self.db().execute(query)
        except Exception as e:
            print(e, "error ")
            data = e

        return data

    async def get_by_id(self, id):
        query = expeditions.select().where('id' == id)
        try:
            data = await self.db().fetch_one(query)
        except Exception as e:
            data = e

        return data