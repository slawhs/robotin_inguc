# Code based on: https://www.youtube.com/watch?v=JLmI0GJuGlY

from llama_index.llms.ollama import Ollama
from llama_parse import LlamaParse
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, PromptTemplate
from llama_index.core.embeddings import resolve_embed_model
from llama_index.core.tools import QueryEngineTool, ToolMetadata
from llama_index.core.agent import ReActAgent
from prompts import context

from dotenv import load_dotenv
load_dotenv()

llm = Ollama(model='llama3', request_timeout=300.0)

parser = LlamaParse(result_type='markdown')
file_extractor={'.pdf': parser}
documents = SimpleDirectoryReader('./data').load_data()

embed_model =  resolve_embed_model('local:BAAI/bge-base-en-v1.5')
vector_index = VectorStoreIndex.from_documents(documents, embed_model=embed_model)

chat_engine = vector_index.as_chat_engine(llm=llm, chat_mode='condense_plus_context', context=context)

while (prompt := input("Enter a prompt (q to quit):")) != "q":
    retries = 0

    while retries < 3:
        try:
            result = chat_engine.chat(prompt)
            print(result)
            break
        except Exception as e:
            retries += 1
            print("Error ocurred, retrying...")
            print(e)
        
    if retries >= 3:
        print("Unable to process request. Please try again.")
        continue

