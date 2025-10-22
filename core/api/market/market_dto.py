from typing import List, Annotated

from pydantic import Field

from core.api.base_dto import BaseResponse, ExtendedBaseModel


class ProductItem(ExtendedBaseModel):
    id: Annotated[int, Field(ge=1)]
    title: Annotated[str, Field(min_length=1)]
    price: Annotated[float, Field(ge=0)]

class ProductsData(ExtendedBaseModel):
    items: List[ProductItem]
    current: Annotated[int, Field(ge=0)]
    total_pages: Annotated[int, Field(ge=0)]
    total_items: Annotated[int, Field(ge=0)]


class CartItem(ExtendedBaseModel):
    product: ProductItem
    quantity: Annotated[int, Field(ge=1)]
    total_price: Annotated[float, Field(ge=0)]


class CartData(ExtendedBaseModel):
    items: List[CartItem]
    total_price: Annotated[float, Field(ge=0)]


class CartDto(BaseResponse[CartData]):
    pass

class ProductsDto(BaseResponse[ProductsData]):
    pass