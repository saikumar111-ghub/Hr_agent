import chromadb
db_path = r"C:\Users\SaikumarJarugumalli\Desktop\HR_Agent\chroma_db"
client = chromadb.PersistentClient(path=db_path)
collection = client.get_collection("hr_documents")
print(f"Collection count: {collection.count()}")