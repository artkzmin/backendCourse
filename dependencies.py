from typing import Annotated

from fastapi import Depends, Query
from pydantic import BaseModel


class PaginationParams(BaseModel):
    page: Annotated[int, Query(1, description="Номер страницы", ge=1)]
    per_page: Annotated[int, Query(
        3, description="Количество отелей на одной странице", ge=1, lt=30
    )]


PaginationDep = Annotated[PaginationParams, Depends()]
