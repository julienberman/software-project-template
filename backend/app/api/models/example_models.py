from pydantic import BaseModel, ConfigDict


class ExampleRequest(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int | None
    name: str | None
    desc: str | None


class ExampleResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    desc: str
