from .utils.document_splits import get_all_document_splits
from langchain.chat_models import init_chat_model #chat model
from langchain_openai import OpenAIEmbeddings #embeddings model
from langchain_core.vectorstores import InMemoryVectorStore #vector store
from langchain_core.tools import tool
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent

def get_agent_executor(document_path):
    embeddings = OpenAIEmbeddings(model="text-embedding-3-large") #chat model
    llm = init_chat_model("gpt-4o-mini", model_provider="openai")  #embeddings model
    vector_store = InMemoryVectorStore(embeddings) #vector store

    all_splits = get_all_document_splits(document_path)

    _ = vector_store.add_documents(documents=all_splits)

    @tool(response_format="content_and_artifact")
    def retrieve(query: str):
        """Retrieve information related to a query."""
        retrieved_docs = vector_store.similarity_search(query, k=2)
        serialized = "\n\n".join(
            (f"Source: {doc.metadata}\n" f"Content: {doc.page_content}")
            for doc in retrieved_docs
        )
        return serialized, retrieved_docs


    memory = MemorySaver()

    agent_executor = create_react_agent(llm, [retrieve], checkpointer=memory)

    return agent_executor