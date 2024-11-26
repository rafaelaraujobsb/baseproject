from datetime import datetime
from logging import getLogger

from pydantic import BaseModel
from sqlalchemy.exc import MissingGreenlet
from sqlalchemy.orm import DeclarativeBase, Mapped, class_mapper, mapped_column
from sqlalchemy.sql import func
from sqlalchemy.types import BigInteger

logger = getLogger(__name__)


def serialize_instance(obj):
    columns = [c.key for c in class_mapper(obj.__class__).columns]

    model_dict = {}
    for attr in columns:
        try:
            model_dict[attr] = getattr(obj, attr)

        except MissingGreenlet:
            logger.warning(f"MissingGreenlet: {obj.__class__.__name__}.{attr}")

    return model_dict


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())

    def to_base_model(self, base_model: BaseModel):
        serialized_data = serialize_instance(self)
        return base_model(**serialized_data)
