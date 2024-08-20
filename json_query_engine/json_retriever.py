# Code based on: https://www.youtube.com/watch?v=JLmI0GJuGlY

from llama_index.llms.ollama import Ollama
from llama_index.core.indices.struct_store import JSONQueryEngine
from os import path
import json


with open(path.join('data', 'corrected_places.json')) as f:
    json_dict = json.load(f)

with open(path.join('data', 'places_schema.json')) as f:
    json_schema = json.load(f)

llm = Ollama(model='llama3', request_timeout=300.0)

# Crear instancia de JSONQueryEngine con la función personalizada
nl_query_engine = JSONQueryEngine(
    json_value=json_dict,
    json_schema=json_schema,
    llm=llm,
    verbose=True
)

try:
    query = f"donde queda la sala M1"
    nl_response = nl_query_engine.query(query)
    print(nl_response.metadata["json_path_response_str"])
except ValueError as e:
    print(f"Error: {e}")