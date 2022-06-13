import json
from typing import Union
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional

from ..depends.auth import verify_auth

class LcdPage(BaseModel):
    body: str
    type: Optional[str] = None

router = APIRouter(
    tags=["LCD Manager"],
    #dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)

@router.get("/v1/lcdman/{page_num}", dependencies=[Depends(verify_auth)])
async def get_page(page_num: int):
    """
    Get 16x2 LCD contents for page @page_num `page_num` {page_num}
    """
    contents = "Hello, SBC Users\nThis is it!"
    return contents

@router.post("/v1/lcdman/{page_num}", dependencies=[Depends(verify_auth)])
async def set_page(page_num: int, page: LcdPage):
    print("TODO: set body", page.body)
    return {"code": 0, "msg": "OK"}
