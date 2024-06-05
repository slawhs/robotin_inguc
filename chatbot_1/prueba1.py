import streamlit as st
from llama_index.core import ServiceContext, SimpleDirectoryReader, StorageContext, VectorStoreIndex, set_global_service_context
from llama_index.llms.ollama import Ollama
from llama_parse import LlamaParse

from dotenv import load_dotenv
load_dotenv()

llm = Ollama(model='llama3', request_timeout=30.0)

parser = LlamaParse(result_type='markdown')
file_extractor={'.pdf': parser}
documents = SimpleDirectoryReader('./data', file_extractor=file_extractor).load_data()

# service_context = ServiceContext.from_defaults(llm=llm, embed_model='local:jinaai/jina-embeddings-v2-base-es', chunk_size=500)  # Embedding bilingue 
service_context = ServiceContext.from_defaults(llm=llm, embed_model='local:BAAI/bge-base-en-v1.5', chunk_size=500)  # Embedding en ingles
set_global_service_context(service_context)

# A node representes a chunk of a source Document
nodes = service_context.node_parser.get_nodes_from_documents(documents)
storage_context = StorageContext.from_defaults()
storage_context.docstore.add_documents(nodes)

index = VectorStoreIndex.from_documents(documents, storage_context=storage_context, llm=llm)
chat_engine = index.as_chat_engine(chat_mode="condense_plus_context")
response = chat_engine.chat("Hola me llamo Ignacio")
print(response)

print(chat_engine.chat("cuándo es la galita?"))




