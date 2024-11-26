from sqlalchemy import delete, select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session


class BaseRepository:
    def __init__(self, session: Session):
        self.session = session

    @staticmethod
    def offset_generator(page: int, page_size: int):
        return (page - 1) * page_size

    async def commit(self):
        await self.session.commit()

    async def execute(self, query):
        result = await self.session.execute(query)
        return result

    async def flush(self):
        await self.session.flush()

    async def rollback(self):
        await self.session.rollback()


class Repository[T](BaseRepository):
    async def refresh(self, model: T):
        await self.session.refresh(model)

    async def add(self, model: T, commit: bool = False) -> T:
        self.session.add(model)

        if commit:
            await self.commit()
            await self.refresh(model)
        else:
            await self.flush()

        return model

    async def add_by_dict(self, model: T, data: dict, commit: bool = False) -> T:
        model = await self.add(model(**data), commit=commit)
        return model

    async def get_one_by_column(
        self,
        model: T,
        *,
        value: str | int,
        column: str = "id",
        with_for_update: bool = False,
    ) -> T:
        query = select(model).where(getattr(model, column) == value)

        if with_for_update:
            query = query.with_for_update()

        results = await self.execute(query)
        return results.unique().scalar_one_or_none()

    async def update_one(
        self,
        model: T,
        *,
        value: str | int,
        data: dict,
        column: str = "id",
        commit: bool = False,
    ) -> T:
        db_model = await self.get_one_by_column(model, value=value, column=column, with_for_update=True)

        if not db_model:
            raise NoResultFound

        for k, v in data.items():
            setattr(db_model, k, v)

        if commit:
            await self.commit()
            await self.refresh(db_model)
        else:
            await self.flush()

        return db_model

    async def delete_by_column(self, model: T, value: str | int, column: str = "id", commit: bool = False) -> int:
        query = delete(model).where(getattr(model, column) == value)
        rows = await self.execute(query)

        if commit:
            await self.commit()

        return rows.rowcount
