from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from app.schemas.fragment import FragmentResponse
from app.services.fragment_service import FragmentService
from dotenv import load_dotenv
import os

router = APIRouter()
load_dotenv()

@router.get("/", response_model=FragmentResponse, response_class=StreamingResponse)
async def get_fragments():
    """
    Endpoint that returns processed fragments from a .jsonl file
    """
    fragment_service = FragmentService(os.getenv("FILE_PATH"), os.getenv("GPT_API_KEY"))
    response = await fragment_service.get_fragments_from_file()
    return StreamingResponse(response, media_type="text/plain")