import json

def read_jsonl_file(file_path: str) -> list[dict]:
    """
    Reads a .jsonl file and returns a list of JSON objects.

    :param file_path: Route to .jsonl file
    :return: List of dicts with file data
    """
    file_data = []
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                file_data.append(json.loads(line.strip()))
    except FileNotFoundError:
        print(f"El archivo {file_path} no fue encontrado.")
    except json.JSONDecodeError as e:
        print(f"Error al decodificar JSON: {e}")
    except Exception as e:
        print(f"Error al leer el archivo {file_path}: {e}")
    return file_data