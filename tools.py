from crewai.tools import BaseTool
import chromadb
from langchain_ollama import OllamaEmbeddings
from typing import Optional, Any
import json

class ChromaDBRetrieverTool(BaseTool):
    name: str = "ChromaDB Retriever"
    description: str = "Retrieves relevant document chunks from the database based on the user's query."
    embedder: Optional[OllamaEmbeddings] = None
    client: Optional[Any] = None
    collection: Optional[Any] = None

    def __init__(self):
        try:
            super().__init__()
            self.embedder = OllamaEmbeddings(model="nomic-embed-text", base_url="http://localhost:11434")
            db_path = "C:\\Users\\SaikumarJarugumalli\\Desktop\\HR_Agent\\chroma_db"  # Same absolute path
            self.client = chromadb.PersistentClient(path=db_path)
            self.collection = self.client.get_or_create_collection("hr_documents")
            print(f"Initialized ChromaDBRetrieverTool. Collection 'hr_documents' has {self.collection.count()} items")
        except Exception as e:
            print(f"Error initializing ChromaDBRetrieverTool: {e}")
            raise

    def _run(self, query: str) -> str:
        try:
            print(f"Received query: {query}")

            if isinstance(query, str) and query.startswith("{"):
                try:
                    query_data = json.loads(query)
                    query = query_data.get("query", query)
                except json.JSONDecodeError:
                    pass

            if not query or not isinstance(query, str):
                return "Error: Query must be a non-empty string."

            query_embedding = self.embedder.embed_query(query)
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=5,
                include=["metadatas"]
            )

            if "metadatas" not in results or not results["metadatas"] or not results["metadatas"][0]:
                return "No relevant documents found."

            documents = []
            for meta in results["metadatas"][0]:
                if isinstance(meta, dict) and "text" in meta and "file" in meta:
                    documents.append(f"{meta['text']}\n(Source: {meta['file']})")
                else:
                    print(f"Skipping invalid metadata: {meta}")

            return "\n\n".join(documents) if documents else "No valid documents found."

        except Exception as e:
            print(f"Error in ChromaDBRetrieverTool: {e}")
            return f"Error retrieving documents: {str(e)}"