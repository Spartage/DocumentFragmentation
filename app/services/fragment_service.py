from app.schemas.fragment import FragmentResponse
from app.utils.file_utils import read_jsonl_file
from openai import OpenAI
from fastapi import HTTPException
import json
import asyncio

class FragmentService:
    _id_counter = 1

    def __init__(self, file_path: str, gpt_api_key: str):
        self.file_path = file_path
        self.gpt_api_key = gpt_api_key

    async def get_fragments_from_file(self) -> str:
        """
        Reads .jsonl and and fragments each article data with information generated
        by GPT
        :return: List of FragmentResponse with processed data
        """
        original_data = read_jsonl_file(self.file_path)
        fragments = []
        client = OpenAI(api_key = self.gpt_api_key)

        # We'll do a first chatgpt call with all entries at the same time to find
        # predefined article tags in which we are going to categorize each article after

        combined_data = ""
        for line in original_data:
            if line["type"] == "article":
                combined_data += line["text"] + "\n"

        categories = self._identify_categories_with_gpt(combined_data, client)

        # Add chatgpt Calls to run as coroutines
        tasks = []
        for item in original_data:
            if item.get("type") == "article":
                task = self._process_single_fragment(item, categories, client)
                tasks.append(task)

        fragments = await asyncio.gather(*tasks)

        fragments = self._assign_related_fragments(fragments)

        # Converts fragments to jsonl
        jsonl_fragments = "\n".join(json.dumps(fragment.model_dump()) for fragment in fragments)

        return jsonl_fragments

    
    async def _process_single_fragment(self, item: dict, categories: str, client: OpenAI) -> FragmentResponse:
        """
        Process a single fragment calling chatgpt API
        :param item: Fragment data to process.
        :param categories: Predefined categories.
        :param client: OpenAI client.
        :return: FragmentResponse with processed data.
        """
        title, summary, tags = await self._generate_fragment_details(item["text"], categories, client)

        fragment = FragmentResponse(
            id=self._generate_id(),
            title=title,
            content=item["text"],
            summary=summary,
            tags=tags,
            url=item["url"],
            related_fragments=[]  # We will fill this after all fragments have been processed
        )

        return fragment
    
    def _identify_categories_with_gpt(self, content: str, client: OpenAI) -> dict:
        """
        Call GPT to review all content and find categories for them
        :param content: Text with all .jsonl info.
        :param client: OpenAI client.
        :return: List of suggested categories in json format.
        """
        prompt = f"""
        Aquí tienes un conjunto de textos que forman parte de la documentación de Adereso.ai.
        Necesito que analices todo el contenido y generes una lista de categorías o secciones generales que mejor representen la organización de estos documentos.
        Las categorías deben ser específicas y útiles para clasificar la documentación.

        Contenido:
        \"\"\"{content}\"\"\"

        Por favor, devuelve una lista de categorías en formato JSON pero sin la palabra json al inicio.
        """

        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "Eres un asistente que ayuda a organizar documentación."},
                    {"role": "user", "content": prompt},
                ],
                max_tokens=500,
                temperature=0.3,
            )

            gpt_output = response.choices[0].message.content
            categories = json.loads(gpt_output)
            return categories

        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            raise HTTPException(
                status_code=500,
                detail=f"Error decoding JSON: {e}"
            )
        except Exception as e:
            print(f"Error communicating with OpenAI API: {e}")
            raise HTTPException(
                status_code=500,
                detail=f"Error communicating with OpenAI API: {e}"
            )
    
    async def _generate_fragment_details(self, content:str, categories:str, client:OpenAI) -> list[str, str, list[str]]:
        """
        Calls GPT API to generate title, summary and tags for a fragment.
        :param content: Text with article to process.
        :param categories: Categories that are going to be considered in classification
        :param client: OpenAI client.
        :return: List of resultant title, summary and list of tags respectively.
        """

        prompt = f"""
                Estás ayudando a organizar la documentación técnica de una plataforma llamada Adereso.ai.
                Quiero que leas el siguiente texto y generes un título, un resumen, y elijas un máximo de 3 categorias desde las categorias predefinidas

                1. **títle**: Genera un título corto y descriptivo que capture la esencia del contenido del texto.
                2. **summary**: Proporciona un resumen conciso que explique los puntos principales del texto.
                3. **tags**: Elije entre 1 y 3 etiquetas desde las categorias predefinidas mencionadas a continuacion:

                Categorias predefinidas:
                "{categories}"

                Aquí está el texto:

                "{content}"

                Porfavor proporciona la respuesta en formato json valido para ser procesado por Python,
                sin incluir json al inicio del string.

                {{
                    "title": "Tu titulo generado aqui",
                    "summary": "Un resumen conciso aqui",
                    "tags": ["tag1", "tag2", ...] "tags aqui"
                }}
                """
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Eres un asistente que ayuda a organizar documentación."},
                {"role": "user", "content": prompt},
            ],
            max_tokens=1000,
        )
        print(response.choices[0].message.content)

        gpt_output = response.choices[0].message.content
        generated_data = json.loads(gpt_output)

        title = generated_data.get("title", "Untitled")
        summary = generated_data.get("summary", "No summary available.")
        tags = generated_data.get("tags", [])
        return title, summary, tags
    
    def _assign_related_fragments(self, fragments: list[FragmentResponse]) -> list[FragmentResponse]:
        """
        Assigns articles related to each fragment based on tags similarity.
        :param fragments: FragmentResponse's list with processed fragments.
        :return: Updated FragmentResponse's list with assigned related articles.
        """
        for fragment in fragments:
            related_ids = []
            for other_fragment in fragments:
                if fragment.id != other_fragment.id:
                    shared_tags = set(fragment.tags).intersection(set(other_fragment.tags))
                    if len(shared_tags) >= 2:
                        related_ids.append(other_fragment.id)
            fragment.related_fragments = related_ids
        return fragments


    def _generate_id(self) -> int:
        """
        Generates a unique ID (Resets when the app is restarted)
        """
        new_id = FragmentService._id_counter
        FragmentService._id_counter += 1
        return new_id