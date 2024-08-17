# Code based on: https://www.youtube.com/watch?v=JLmI0GJuGlY

from llama_index.llms.ollama import Ollama
from llama_index.core.indices.struct_store import JSONQueryEngine
from llama_index.core import ServiceContext
from IPython.display import Markdown, display
from os import path
import json

with open(path.join('data', 'places.json')) as f:
    json_dict = json.load(f)

with open(path.join('data', 'places_schema.json')) as f:
    json_schema = json.load(f)

llm = Ollama(model='llama3', request_timeout=60.0)

nl_query_engine = JSONQueryEngine(
    json_value=json_dict,
    json_schema=json_schema,
    llm=llm
)



nl_response = nl_query_engine.query("donde queda la sala M1")
print(nl_response.metadata["json_path_response_str"])

# display(Markdown(nl_response))