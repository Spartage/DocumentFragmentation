from app.schemas.fragment import FragmentResponse
from app.utils.file_utils import read_jsonl_file
import openai

class FragmentService:
    def __init__(self, file_path: str, gpt_api_key: str):
        self.file_path = file_path
        self.gpt_api_key = gpt_api_key
        openai.api_key = gpt_api_key

    async def get_fragments_from_file(self) -> list[FragmentResponse]:
        """
        Reads .jsonl and and fragments each article data with information generated
        by GPT
        :return: List of FragmentResponse with processed data
        """
        original_data = read_jsonl_file(self.file_path)
        fragments = []


