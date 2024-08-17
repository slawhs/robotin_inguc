# Code based on: https://www.youtube.com/watch?v=JLmI0GJuGlY

from llama_index.llms.ollama import Ollama
from llama_index.core import (VectorStoreIndex, SimpleDirectoryReader,
                              StorageContext, load_index_from_storage)
from llama_index.core.agent import ReActAgent
from llama_index.core.embeddings import resolve_embed_model
from llama_index.core.tools import QueryEngineTool, ToolMetadata
from llama_parse import LlamaParse
from prompts import context
import os

from dotenv import load_dotenv

load_dotenv()

PERSIST_DIR = "./storage/"

llm = Ollama(model='llama3.1', request_timeout=60.0)
embed_model = resolve_embed_model('local:jinaai/jina-embeddings-v2-base-es')

parser = LlamaParse(result_type='markdown')
file_extractor = {'.pdf': parser}

data_list = ["practica", "data"]

data_docs = {}

data_indexes = {}

for name in data_list:
    if not os.listdir(PERSIST_DIR + name):
        # print("No existe :(")
        data_docs[name] = SimpleDirectoryReader(
            input_files=[f"./data/{name}.pdf"],
            file_extractor=file_extractor
        ).load_data()
        storage_context = StorageContext.from_defaults()
        data_indexes[name] = VectorStoreIndex.from_documents(
            data_docs[name], embed_model=embed_model,
            storage_context=storage_context
        )

        storage_context.persist(persist_dir=PERSIST_DIR+name)
    else:
        # print("Existe :)")
        storage_context = StorageContext.from_defaults(
            persist_dir=PERSIST_DIR+name,
        )
        data_indexes[name] = load_index_from_storage(
            storage_context,
            embed_model=embed_model
        )

practica_engine = data_indexes["practica"].as_query_engine(
    similarity_top_k=3, llm=llm)

data_engine = data_indexes["data"].as_query_engine(similarity_top_k=3, llm=llm)

query_engine_tools = [
    QueryEngineTool(
        query_engine=practica_engine,
        metadata=ToolMetadata(
            name="practica_1_manual",
            description="Entrega información sobre el manual de instrucciones y especificaciones de la práctica 1")
    ),
    QueryEngineTool(
        query_engine=data_engine,
        metadata=ToolMetadata(
            name="eventos",
            description="Entrega información sobre fechas y precios de distintos eventos y evaluaciones")
    ),
]

agent = ReActAgent.from_tools(query_engine_tools,
                              llm=llm,
                              verbose=False,
                              context=context,
                              max_iterations=20,
                              )

while True:
    text_input = input(">> ")
    if text_input == "q":
        break
    streaming_response = agent.stream_chat(text_input)
    streaming_response.print_response_stream()
    print()
