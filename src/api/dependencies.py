from typing import Annotated

from fastapi import Query, Depends
from pydantic import BaseModel

class PaginationParams(BaseModel):
    page:   Annotated[
        int | None,
        Query(None, ge=1)
    ]
    offset: Annotated[
        int | None,
        Query(None, ge=1, le=30)
    ]

PaginationDep = Annotated[PaginationParams, Depends()]