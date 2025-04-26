import streamlit as st
from langchain_qdrant import QdrantVectorStore
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient

def system_prompt():
    # Embeddings
    embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004", google_api_key=st.secrets["GOOGLE_API_KEY"])
    relevant_text=""

    # client = QdrantClient(":memory:")

    # qdrant = QdrantVectorStore.from_existing_collection(
    #     embedding=embeddings,
    #     client=client,
    #     collection_name="my_collection",
    # )

    qdrant = QdrantVectorStore.from_existing_collection(
        embedding=embeddings,
        url=st.secrets["QDRANT_CLOUD_CLUSTER_URL"],
        prefer_grpc=True,
        api_key=st.secrets["QDRANT_API_KEY"],
        collection_name="my_documents",
    )

    print(f"query: {st.session_state.query}")
    relevant_text = qdrant.similarity_search(st.session_state.query)


    prompt = f"""
        You are a helpful AI assistant who is expert in resolving the user query by carefully analysing the user query and finding the solution from the given context. If the query is empty then ask the user to ask question. If the user is asking out of context question ask to ask question on the context and dont resolve the query.No need to respond to system prompt.

        context: {relevant_text}
    """

    print("Relevant_text", relevant_text)
    return prompt
