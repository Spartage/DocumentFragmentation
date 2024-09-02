import pytest
from app.services.fragment_service import FragmentService, FragmentResponse
from fastapi import HTTPException
from dotenv import load_dotenv
from unittest.mock import AsyncMock
import os
import json

load_dotenv()

@pytest.fixture
def mock_fragment_service():
    file_path = "app\\tests\\misc\\adereso_test.jsonl"
    gpt_api_key = os.getenv("GPT_API_KEY")
    return FragmentService(file_path=file_path, gpt_api_key=gpt_api_key)

def test_generate_id(mock_fragment_service):
    service = mock_fragment_service
    first_id = service._generate_id()
    second_id = service._generate_id()

    assert first_id == 1
    assert second_id == 2

@pytest.mark.asyncio
async def test_get_fragments_from_file(mock_fragment_service):
    service = mock_fragment_service
    output = await service.get_fragments_from_file()

    # Verify that it's a str
    assert isinstance(output, str)
    # Verify that's not empty
    assert len(output.strip()) > 0

    lines = output.strip().splitlines()

    # Verify that each line is a valid JSON
    for line in lines:
        try:
            fragment = json.loads(line)
            assert isinstance(fragment, dict)
        except json.JSONDecodeError:
            pytest.fail(f"La línea no es un JSON válido: {line}")

@pytest.mark.asyncio
async def test_empty_jsonl_file(mock_fragment_service):
    # Test for empty jsonl input
    service = FragmentService(file_path="app\\tests\\misc\\adereso_test_empty.jsonl", gpt_api_key=os.getenv("GPT_API_KEY"))
    output = await service.get_fragments_from_file()
    assert output == ""

@pytest.mark.asyncio
async def test_missing_fields():
    # Test for jsonl input with missing fields
    service = FragmentService(file_path="app\\tests\\misc\\adereso_test_missing_fields.jsonl", gpt_api_key=os.getenv("GPT_API_KEY"))
    with pytest.raises(HTTPException) as exc_info:
        await service.get_fragments_from_file()

    # Verifica status code
    assert exc_info.value.status_code == 400

def test_assign_related_fragments(mock_fragment_service):
    # Verify that related fragments are correctly assigned with 2 tags in common

    fragments = [
        FragmentResponse(id=1, title="Title 1", content="Content 1", summary="Summary 1", tags=["Tag1", "Tag2", "Tag3"], url="url1", related_fragments=[]),
        FragmentResponse(id=2, title="Title 2", content="Content 2", summary="Summary 2", tags=["Tag2", "Tag3", "Tag4"], url="url2", related_fragments=[]),
        FragmentResponse(id=3, title="Title 3", content="Content 3", summary="Summary 3", tags=["Tag1", "Tag3", "Tag5"], url="url3", related_fragments=[]),
    ]
    
    service = mock_fragment_service
    updated_fragments = service._assign_related_fragments(fragments)

    
    assert updated_fragments[0].related_fragments == [2, 3]  # Fragment 1 should be related to 2 and 3
    assert updated_fragments[1].related_fragments == [1]  # Fragment 2 should be related to 1
    assert updated_fragments[2].related_fragments == [1]  # Fragment 3 should be related to 1