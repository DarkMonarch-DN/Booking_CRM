from fastapi import APIRouter

from app.dependencies.auth import AdminDep
from app.dependencies.services import ItemServiceDep
from app.schemas.item import ItemCreate, ItemResponse

router = APIRouter()


# * No auth
@router.get("/", response_model=list[ItemResponse])
async def get_all(item_service: ItemServiceDep):
    return await item_service.find_all()


# * Admin
@router.post("/", response_model=ItemResponse)
async def add_item(
    item_in: ItemCreate, item_service: ItemServiceDep, current_user: AdminDep
):
    return await item_service.add_new_item(item_in)


# * Admin
@router.delete("/{item_id}", response_model=ItemResponse)
async def delete_item(
    item_id: int, item_service: ItemServiceDep, current_user: AdminDep
):
    return await item_service.delete(item_id)
