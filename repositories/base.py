from sqlalchemy import select, insert, delete, update
from pydantic import BaseModel


class BaseRepository:
    model = None

    def __init__(self, session):
        self.session = session


    async def get_all(self, *args, **kwargs):
        query = select(self.model)
        results = await self.session.execute(query)

        return results.scalars().all()

    async def get_one_or_none(self, **filter_params):
        query = select(self.model).filter_by(**filter_params)
        result = await self.session.execute(query)

        return result.scalars().one_or_none()


    async def add(self, data: BaseModel):
        stmt = insert(self.model).values(**data.model_dump()).returning(self.model)
        result = await self.session.execute(stmt)
        return result.scalars().one()


    async def edit(self, data: BaseModel, **filter_params) -> None:
        update_stmt = (
            update(self.model)
            .filter_by(**filter_params)
            .values(**data.model_dump())
        )

        await self.session.execute(update_stmt)


    async def delete(self, **filter_params) -> None:
        delete_stmt = delete(self.model).filter_by(**filter_params)

        await self.session.execute(delete_stmt)