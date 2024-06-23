from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.templating import Jinja2Templates
from ..dependencies import get_token_header

router = APIRouter(
    prefix="/items",
    tags=["items"],
    dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)

templates = Jinja2Templates(directory="templates")


fake_items_db = {"plumbus": {"name": "Plumbus"}, "gun": {"name": "Portal Gun"}}


@router.get("/")
async def read_items():
    return fake_items_db


@router.get("/{item_id}")
async def read_item(request: Request, item_id: str):
    if item_id not in fake_items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return templates.TemplateResponse(
        request=request,
        name="item.html",
        context={"name": fake_items_db[item_id]["name"], "id": item_id},
    )


@router.put(
    "/{item_id}",
    tags=["custom"],
    responses={403: {"description": "Operation forbidden"}},
)
async def update_item(item_id: str):
    if item_id != "plumbus":
        raise HTTPException(
            status_code=403, detail="You can only update the item: plumbus"
        )
    return {"item_id": item_id, "name": "The great Plumbus"}
