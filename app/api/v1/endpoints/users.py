from fastapi import APIRouter
import httpx
router = APIRouter()

@router.get("/")
def get_users():
    return [{"id": 1, "name": "Nishant"}]
@router.post("/")
async def another_api():
    async with httpx.AsyncClient(timeout=5.0) as client:
        response = await client.get("https://api.github.com")
        return response.json()

