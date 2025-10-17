from pydantic import BaseModel, Field


class TokenDto(BaseModel):
    token: str = Field(min_length=5)
    type: str = Field(min_length=5)