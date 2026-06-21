from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Response

from app.api.models.example_models import (
    ExampleRequest,
    ExampleResponse,
)
from app.init.dicontainer import AppContainer
from app.services.example_service import ExampleService

router = APIRouter(prefix="/v1", tags=["example_endpoint"])

@router.get("/example_endpoint")
@inject
async def get_item(
    params: ExampleRequest = Depends(),
    example_service: ExampleService = Depends(Provide[AppContainer.example_service]),
) -> ExampleResponse:
    item = example_service.get_item(id=params.id)
    return ExampleResponse(
        id=item.id,
        name=item.name,
        desc=item.desc,
    )


@router.post("/example_endpoint")
@inject
async def add_item(
    params: ExampleRequest = Depends(),
    example_service: ExampleService = Depends(Provide[AppContainer.example_service]),
) -> ExampleResponse:
    item = example_service.add_item(
        name=params.name,
        desc=params.desc,
    )
    return ExampleResponse(
        id=item.id,
        name=item.name,
        desc=item.desc,
    )


