from fastapi import APIRouter, Body, Query

from schemas.hotels import Hotel, HotelPATCH
from src.api.dependencies import PaginationDep

router = APIRouter(prefix="/hotels", tags=["Hotels"])

hotels = [
    {"id": 1, "title": "Dubai", "name": "dubai"},
    {"id": 2, "title": "Sochi", "name": "sochi"},
    {"id": 3, "title": "Kemerovo", "name": "kem"},
    {"id": 4, "title": "Minsk", "name": "min"},
    {"id": 5, "title": "Kazan", "name": "kzn"},
    {"id": 6, "title": "Moscow", "name": "msc"},
    {"id": 7, "title": "Saint-Petersburb", "name": "spb"},
]


@router.get("")
def get_hotels(
    pagination: PaginationDep,
    id: int | None = Query(None, description="Hotel ID"),
    title: str = Query(None, description="Hotel title"),
):
    result = []
    for hotel in hotels:
        if id and hotel["id"] != id:
            continue

        if title and hotel["title"] != title:
            continue

        result.append(hotel)

    if pagination.page and pagination.offset:
        return result[pagination.offset * (pagination.page - 1) :][: pagination.offset]

    return result


@router.delete("/{hotel_id}")
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"status": "ok"}


@router.post("/hotels")
def create_hotel(
    hotel_data: Hotel = Body(
        openapi_examples={
            "1": {
                "summary": "New-York",
                "value": {"title": "New-York Hotel", "name": "nyc"},
            },
            "2": {
                "summary": "Test",
                "value": {"title": "testTitle", "name": "testName"},
            },
        }
    ),
):
    global hotels
    hotels.append(
        {
            "id": hotels[-1]["id"] + 1,
            "title": hotel_data.title,
            "name": hotel_data.title,
        }
    )

    return {"status": "ok"}


@router.put("/{hotel_id}")
def put_hotel(hotel_id: int, hotel_data: Hotel):
    global hotels
    hotel = [hotel for hotel in hotels if hotel["id"] == hotel_id][0]
    hotel["title"] = hotel_data.title
    hotel["name"] = hotel_data.name

    return {"status": "ok"}


@router.patch("/{hotel_id}")
def patch_hotel(hotel_id: int, hotel_data: HotelPATCH):
    global hotels
    hotel = [hotel for hotel in hotels if hotel["id"] == hotel_id][0]
    if hotel_data.title:
        hotel["title"] = hotel_data.title

    if hotel_data.name:
        hotel["name"] = hotel_data.name

    return {"status": "ok"}
