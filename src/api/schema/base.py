from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_snake


class BaseSchema(BaseModel):
    model_config = ConfigDict(alias_generator=to_snake, allow_population_by_field_name=True)
