# HR Agent: Agentic RAG for HR Policy Queries

![HR Agent Architecture](architecture_diagram.png)

**HR Agent** is an intelligent question-answering system that leverages **Agentic Retrieval-Augmented Generation (RAG)** to provide accurate and context-aware responses to HR policy queries. Built with **CrewAI**, **ChromaDB**, and **Ollama**, it processes HR policy documents (e.g., PDFs) and answers questions like "How does TCS conduct manpower planning?" by retrieving relevant document chunks and generating concise summaries.

Unlike traditional RAG, this system uses a multi-agent architecture, with a **Retriever Agent** to fetch relevant data and a **Generator Agent** to craft answers, orchestrated by CrewAI. The knowledge base is stored in ChromaDB, a vector database, ensuring efficient retrieval.

## Features
- **Agentic RAG**: Multi-agent system with collaborative retriever and generator agents.
- **External Knowledge Base**: Stores HR policy documents in ChromaDB for scalable retrieval.
- **Local LLM**: Uses Ollama’s Mistral model for on-device generation, ensuring privacy.
- **PDF Processing**: Ingests and chunks PDF documents for queryable storage.
- **Extensible**: Easily add more agents or tools for advanced workflows.

## Prerequisites
- **Python**: 3.8 or higher
- **Ollama**: Installed and running locally with the Mistral model (`ollama pull mistral`)
- **ChromaDB**: For vector storage
- **PDFs**: HR policy documents in the `data` folder (e.g., `Hr Policies.pdf`)

## Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/your-username/hr-agent.git
   cd hr-agent
   ```

2. **Set Up a Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```
   Example `requirements.txt`:
   ```
   crewai==0.30.11
   langchain-ollama==0.1.0
   chromadb==0.5.0
   langchain-community==0.2.5
   PyPDF2==3.0.1
   python-dotenv==1.0.1
   ```

4. **Set Up Environment Variables**
   Create a `.env` file in the root directory:
   ```env
   OLLAMA_MODEL=mistral
   ```

5. **Start Ollama Server**
   ```bash
   ollama serve
   ```
   Ensure the Mistral model is available (`ollama list`).

## Usage

### 1. Ingest HR Policy Documents
- Place PDF documents in the `data` folder (e.g., `data/Hr Policies.pdf`).
- Run the ingestion script to process PDFs and store chunks in ChromaDB:
  ```bash
  python ingest.py
  ```
- Output example:
  ```
  Processing data\Hr Policies.pdf...
  Loaded 19 pages from Hr Policies.pdf
  Split into 19 chunks
  Stored 19 chunks for Hr Policies.pdf
  Collection count after storage: 19
  ```

### 2. Query the HR Agent
- Run the crew to answer queries:
  ```bash
  python crew.py
  ```
- Enter a query when prompted, e.g., “How does TCS conduct manpower planning?”
- Example output:
  ```
  TCS conducts manpower planning through the Manpower Allocation Task Committee (MATC), using a just-in-time hiring strategy to match associates’ skills to project needs, with a typical lead time of three weeks for replacements (Source: Hr Policies.pdf).
  ```

### 3. Test the Database
- Verify ChromaDB contents:
  ```bash
  python test_db.py
  ```
- Output: `Collection count: 19`

## Architecture

The system follows an **Agentic RAG** approach, with a multi-agent workflow orchestrated by CrewAI.

### Components
- **`ingest.py`**: Loads PDFs, splits them into chunks, generates embeddings using Ollama’s `nomic-embed-text`, and stores them in ChromaDB.
- **`tools.py`**: Defines `ChromaDBRetrieverTool`, which retrieves relevant chunks from ChromaDB based on query embeddings.
- **`agents.py`**:
  - **Retriever Agent**: Uses the retriever tool to fetch HR policy chunks.
  - **Generator Agent**: Summarizes retrieved chunks into a concise answer using Mistral.
- **`task.py`**:
  - **Retrieval Task**: Fetches relevant chunks.
  - **Generation Task**: Generates an answer using the retrieved context.
- **`crew.py`**: Orchestrates agents and tasks, handling user queries.
- **ChromaDB**: Stores document chunks and embeddings at `C:\Users\SaikumarJarugumalli\Desktop\HR_Agent\chroma_db`.

### Workflow
1. **Ingestion**: PDFs are chunked and stored in ChromaDB.
2. **Query Input**: User provides a query (e.g., “How does TCS conduct manpower planning?”).
3. **Retrieval**: The retriever agent fetches top 5 matching chunks from ChromaDB.
4. **Generation**: The generator agent summarizes the chunks into an answer.
5. **Output**: A concise response is returned.

![Workflow Diagram](workflow_diagram.png)

## Agentic RAG vs. Traditional RAG
- **Traditional RAG**: Single-step retrieval and generation (retrieve → generate).
- **Agentic RAG (This Project)**: Multi-agent system with:
  - Collaborative agents (retriever and generator).
  - Task orchestration via CrewAI.
  - Extensible for additional agents (e.g., planners, validators).
- **Why Agentic?**: Enables dynamic workflows, complex reasoning, and tool integration, making it more robust for advanced applications.

## Troubleshooting
- **Empty ChromaDB**: Ensure `ingest.py` ran successfully and `chroma_db` exists.
- **LLM Failure**: Verify Ollama server is running (`ollama serve`) and Mistral is available (`ollama list`).
- **Retrieval Issues**: Check query format and ChromaDB path in `tools.py`.
- **Logs**: Review `chromadb_tool.log` for errors.

## Contributing
Contributions are welcome! To contribute:
1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/your-feature`).
3. Commit changes (`git commit -m "Add your feature"`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Open a pull request.

Please follow the [code of conduct](CODE_OF_CONDUCT.md) and include tests for new features.

## License
This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

## Acknowledgments
- **CrewAI**: For the agent orchestration framework.
- **ChromaDB**: For vector storage and retrieval.
- **Ollama**: For local LLM inference.
- **LangChain**: For document processing and embeddings.

## Contact
For questions or feedback, open an issue or contact [your-email@example.com](mailto:your-email@example.com).