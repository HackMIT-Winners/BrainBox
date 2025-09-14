from fastapi import APIRouter, Request

router = APIRouter()

@router.post("/notion/events")
async def notion_events(request: Request):
    text = await request.json() 
    print(text)
    return {"message": "ok"}
