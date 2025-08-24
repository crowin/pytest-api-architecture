from typing import List, Annotated

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel

class BaseDto(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True,
    )

class Product(BaseDto):
    discount_percentage: Annotated[float, Field(gt=0)]
    discounted_total: Annotated[float, Field(gt=0)]
    id: Annotated[int, Field(gt=0)]
    price: Annotated[float, Field(gt=0)]
    quantity: Annotated[int, Field(gt=0)]
    thumbnail: str
    title: str
    total: Annotated[float, Field(gt=0)]


class Cart(BaseDto):
    id: int
    total: float
    discounted_total: float
    products: List[Product]
    total_products: int
    total_quantity: int
    user_id: int

class CartsDto(BaseDto):
    carts: List[Cart]
    total: int
    skip: int
    limit: int
