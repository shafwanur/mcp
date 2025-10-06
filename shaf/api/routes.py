from fastapi import APIRouter, HTTPException
from .models import QueryRequest
from .helpers import process_agent_query

router = APIRouter(prefix="/api", tags=["api"])


@router.post("/query")
async def handle_query(request: QueryRequest) -> str:
    result = await process_agent_query(request)
    return result
