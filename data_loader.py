import streamlit as st
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.document_loaders.telegram import text_to_docs
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient


def load_data():
    try:
        text = st.session_state.context
        docs = text_to_docs(text=text)
        # print(docs)

        # Splitting the document into chunks
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
        texts = text_splitter.split_documents(docs)

        # print(texts[0])

        # Embeddings
        embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004", google_api_key=st.secrets["GOOGLE_API_KEY"])

        client = QdrantClient(url=st.secrets["QDRANT_CLOUD_CLUSTER_URL"],
            api_key=st.secrets["QDRANT_API_KEY"],)
        
        client.delete_collection(collection_name="my_documents")


        qdrant = QdrantVectorStore.from_documents(
            documents=texts,
            embedding=embeddings,
            url=st.secrets["QDRANT_CLOUD_CLUSTER_URL"],
            prefer_grpc=True,
            api_key=st.secrets["QDRANT_API_KEY"],
            collection_name="my_documents",
        )
        

        # print("Vector Store", st.session_state.vector_store)
        return True
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        raise






