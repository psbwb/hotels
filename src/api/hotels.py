from fastapi import APIRouter, Body, Query
from sqlalchemy import insert, select, func

from schemas.hotels import Hotel, HotelPATCH
from src.api.dependencies import PaginationDep
from src.database import async_session_maker
from src.models.hotels import HotelsOrm

router = APIRouter(prefix="/hotels", tags=["Hotels"])

@router.get("")
async def get_hotels(
    pagination: PaginationDep,
    title: str | None = Query(None, description="Hotel title"),
    location: str | None = Query(None, description="Hotel location"),
):
    offset = pagination.offset or 5
    async with (async_session_maker() as session):
        query = select(HotelsOrm)
        if title:
            query = query.filter(func.lower(HotelsOrm.title).contains(title.strip().lower()))
        if location:
            query = query.filter(func.lower(HotelsOrm.location).contains(location.strip().lower()))

        query = (
            query
            .limit(offset)
            .offset(offset * (pagination.page - 1))
        )

        result = await session.execute(query)
        hotels = result.scalars().all()

        return hotels


@router.delete("/{hotel_id}")
def delete_hotel(hotel_id: int):
    return {"status": "ok"}


@router.post("/hotels")
async def create_hotel(
    hotel_data: Hotel = Body(
        openapi_examples={
            "1": {
                "summary": "New-York",
                "value": {"title": "New-York Hotel", "location": "nyc"},
            },
            "2": {
                "summary": "Test",
                "value": {"title": "testTitle", "location": "testName"},
            },
        }
    ),
):
    async with async_session_maker() as session:
        add_hotel_stmt = insert(HotelsOrm).values(**hotel_data.model_dump())
        await session.execute(add_hotel_stmt)
        # print(add_hotel_stmt.compile(compile_kwargs={"literal_binds": True}))
        await session.commit()

    return {"status": "ok"}


@router.put("/{hotel_id}")
def put_hotel(hotel_id: int, hotel_data: Hotel):
    return {"status": "ok"}


@router.patch("/{hotel_id}")
def patch_hotel(hotel_id: int, hotel_data: HotelPATCH):
    return {"status": "ok"}
