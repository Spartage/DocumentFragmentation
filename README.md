# Desafio Técnico Desarrollador FullStack Adereso

Este proyecto es un servicio de procesamiento de fragmentos diseñado para analizar documentos JSONL, generar títulos, resúmenes y etiquetas categorizadas mediante la API de GPT, y luego devolver el resultado en formato .jsonl. Además, el servicio identifica y asigna fragmentos relacionados basados en la similitud de etiquetas.

## Características

- *Identificación de categorías:* Realiza una llama a GPT con todo el contenido para identificar categorías predefinidas.
- *Procesamiento de framentos:* Genera títulos, resúmenes y etiqueta de acuerdo a las categorias predefinidas para cada fragmento de un documento JSONL.
- *Asignación de fragmentos relacionados:* Determina qué fragmentos están relacionados al menos en 2 etiquetas.
- *Salida en formato .jsonl:* Devuelve el resultado en un formato JSONL fácil de procesar.

## Requisitos

- Python 3.12+
- Pip
- OpenAI API Key
- Dependencias definidas en requirements.txt

## Instalación Windows

1. Clonar el repositorio:

```
git clone https://github.com/Spartage/DocumentFragmentation.git
cd DocumentFragmentation
```

2. Crear un entorno virtual:

```
python -m venv .venv
.venv\Scripts\activate
```

3. Instalar dependencias:

```
pip install -r requirements.txt
```

4. Configurar Environment:

Utilizando el .env.example es necesario generar un archivo .env en la misma ruta que tenga la informacion necesaria,

## Uso

Al levantar la aplicación FastAPI tendrás acceso al endpoint /Fragments/get_fragments_api_fragments__get.

Esto tomará el archivo .jsonl y OpenAI API Key definidos en .env para llevar a cabo el procedimiento.

## Formato del Archivo de Entrada:

El archivo de entrada debe ser un archivo .jsonl donde cada línea contiene un fragmento en formato JSON. Ejemplo:

```
{"type": "article", "url": "https://example.com/1", "text": "Contenido del artículo 1"}
{"type": "article", "url": "https://example.com/2", "text": "Contenido del artículo 2"}
```

## Salida

La salida será una cadena en formato .jsonl, donde cada línea es un objeto JSON con los detalles procesados del fragmento, incluyendo los artículos relacionados. Ejemplo:

```
{"title": "Titulo del articulo 1", "summary": "Resumen del artículo 1", "url": "Url del artículo 1", "tags": ["Etiqueta 1 del artículo 1", "Etiqueta 2 del artículo 1", "Etiqueta 3 del artículo 1"], "related_fragments": [id de artículo relacionado 1, id de artículo relacionado 2, ...], "id": id de artículo 1}
{"title": "Titulo del articulo 2", "summary": "Resumen del artículo 2", "url": "Url del artículo 2", "tags": ["Etiqueta 1 del artículo 2", "Etiqueta 2 del artículo 2", "Etiqueta 3 del artículo 2"], "related_fragments": [id de artículo relacionado 1, id de artículo relacionado 2, ...], "id": id de artículo 2}
```

