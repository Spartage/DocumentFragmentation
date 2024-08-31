from fastapi import APIRouter, Depends
from app.schemas.fragment import FragmentResponse
from app.services.fragment_service import FragmentService
import os

router = APIRouter()

@router.get("/", response_model = list[FragmentResponse])
async def get_fragments():
    """
    Endpoint that returns processed fragments from a .jsonl file
    """
    fragment_service = FragmentService(os.getenv("FILE_PATH"), os.getenv("GPT_API_KEY"))
    return await fragment_service.get_fragments_from_file()