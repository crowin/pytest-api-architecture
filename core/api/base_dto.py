from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class ExtendedBaseModel(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True
    )

class BaseResponse[T](ExtendedBaseModel):
    data: T

class BaseListResponse[T](ExtendedBaseModel):
    data: list[T]