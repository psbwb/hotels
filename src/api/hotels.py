from fastapi import APIRouter, Body, Query

from schemas.hotels import Hotel, HotelPATCH, HotelAdd
from src.repositories.hotels import HotelsRepository
from src.api.dependencies import PaginationDep
from src.database import async_session_maker


router = APIRouter(prefix="/hotels", tags=["Hotels"])

@router.get("")
async def get_hotels(
    pagination: PaginationDep,
    title: str | None = Query(None, description="Hotel title"),
    location: str | None = Query(None, description="Hotel location"),
):
    per_page = pagination.per_page or 5
    async with async_session_maker() as session:
        return await HotelsRepository(session).get_all(
            title,
            location,
            limit=per_page,
            offset=per_page * (pagination.page - 1)
        )


@router.get("/{hotel_id}")
async def get_hotel(hotel_id: int):
    async with async_session_maker() as session:
        hotel = await HotelsRepository(session).get_one_or_none(id=hotel_id)
        return hotel


@router.delete("/{hotel_id}")
async def delete_hotel(hotel_id: int):
    async with async_session_maker() as session:
        await HotelsRepository(session).delete(id=hotel_id)
        await session.commit()
    return {"status": "ok"}


@router.post("/hotels")
async def create_hotel(
    hotel_data: HotelAdd = Body(
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
        hotel = await HotelsRepository(session).add(hotel_data)
        await session.commit()

    return {"status": "ok", "data": hotel}


@router.put("/{hotel_id}")
async def put_hotel(hotel_id: int, hotel_data: Hotel):
    async with async_session_maker() as session:
        await HotelsRepository(session).edit(hotel_data, id=hotel_id)
        await session.commit()
    return {"status": "ok"}


@router.patch("/{hotel_id}")
async def patch_hotel(hotel_id: int, hotel_data: HotelPATCH):
    async with async_session_maker() as session:
        await HotelsRepository(session).edit(hotel_data, id=hotel_id, exclude_unset=True)
        await session.commit()
    return {"status": "ok"}
