from fastapi import APIRouter, Body, Query
from sqlalchemy import insert, select

from schemas.hotels import Hotel, HotelPATCH
from src.api.dependencies import PaginationDep
from src.database import async_session_maker
from src.models.hotels import HotelsOrm

router = APIRouter(prefix="/hotels", tags=["Hotels"])

@router.get("")
async def get_hotels(
    pagination: PaginationDep,
    hotel_id: int | None = Query(None, description="Hotel ID"),
    title: str = Query(None, description="Hotel title"),
):
    offset = pagination.offset or 5
    async with (async_session_maker() as session):
        query = select(HotelsOrm)
        if hotel_id:
            query = query.filter_by(id=hotel_id)
        if title:
            query = query.filter_by(title=title)

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
