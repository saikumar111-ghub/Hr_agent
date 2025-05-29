import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
import chromadb

# Set up the embedder and ChromaDB client with an absolute path
embedder = OllamaEmbeddings(model="nomic-embed-text", base_url="http://localhost:11434")
db_path = "C:\\Users\\SaikumarJarugumalli\\Desktop\\HR_Agent\\chroma_db"  # Absolute path
client = chromadb.PersistentClient(path=db_path)
collection = client.get_or_create_collection("hr_documents")

# Process PDF files in the "data" folder
data_folder = "data"

for file_name in os.listdir(data_folder):
    file_path = os.path.join(data_folder, file_name)
    print(f"Processing {file_path}...")
    
    try:
        loader = PyPDFLoader(file_path)
        documents = loader.load()
        print(f"Loaded {len(documents)} pages from {file_name}")
        print(f"Sample text: {documents[0].page_content[:200]}")

        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        chunks = text_splitter.split_documents(documents)
        print(f"Split into {len(chunks)} chunks")

        for i, chunk in enumerate(chunks):
            embedding = embedder.embed_query(chunk.page_content)
            print(f"Chunk {i} embedding generated, length: {len(embedding)}")
            collection.add(
                ids=[f"{file_name}_{i}"],
                embeddings=[embedding],
                metadatas=[{"text": chunk.page_content, "file": file_name}]
            )
        print(f"Stored {len(chunks)} chunks for {file_name}")
        print(f"Collection count after storage: {collection.count()}")

    except Exception as e:
        print(f"Error processing {file_name}: {e}")

print("PDF files ingestion completed successfully")