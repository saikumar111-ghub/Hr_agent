# HR Agent: Intelligent HR Policy Query System

**HR Agent** is an advanced question-answering system built to provide accurate and context-aware responses to HR policy-related queries. It leverages **Agentic Retrieval-Augmented Generation (RAG)** to process HR policy documents (e.g., PDFs) and answer questions like "How does TCS conduct manpower planning?" by retrieving relevant information and generating concise summaries.

This project uses **CrewAI** for agent orchestration, **ChromaDB** for vector storage, and **Ollama** for local LLM inference, ensuring privacy and efficiency with on-device processing.

---

## Table of Contents
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
  - [Ingesting HR Policy Documents](#ingesting-hr-policy-documents)
  - [Querying the HR Agent](#querying-the-hr-agent)
  - [Testing the Database](#testing-the-database)
- [Architecture](#architecture)
  - [Components](#components)
  - [Workflow](#workflow)
- [Agentic RAG vs. Traditional RAG](#agentic-rag-vs-traditional-rag)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgments](#acknowledgments)
- [Contact](#contact)

---

## Features
- **Agentic RAG**: Multi-agent system with collaborative retriever and generator agents for enhanced accuracy.
- **External Knowledge Base**: Stores HR policy documents in ChromaDB for scalable retrieval.
- **Local LLM**: Uses Ollama’s Mistral model for on-device generation, ensuring data privacy.
- **PDF Processing**: Ingests and chunks PDFs for efficient querying.
- **Extensible Design**: Add new agents or tools to adapt to advanced workflows.

---

## Prerequisites
Before setting up HR Agent, ensure you have:
- **Python**: Version 3.8 or higher
- **Ollama**: Installed locally with the Mistral model (`ollama pull mistral`)
- **ChromaDB**: For vector storage and retrieval
- **HR Policy PDFs**: Place documents in the `data` folder (e.g., `Hr Policies.pdf`)

---

## Installation

Follow these steps to set up the HR Agent project:

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
   Verify the Mistral model is available:
   ```bash
   ollama list
   ```

---

## Usage

### Ingesting HR Policy Documents
To make HR policy documents queryable, they must be ingested into ChromaDB.

1. Place your PDFs in the `data` folder (e.g., `data/Hr Policies.pdf`).
2. Run one of the ingestion scripts:
   - **Basic Ingestion**:
     ```bash
     python ingest.py
     ```
     **Example Output**:
     ```
     Processing data\Hr Policies.pdf...
     Loaded 19 pages from Hr Policies.pdf
     Split into 19 chunks
     Stored 19 chunks for Hr Policies.pdf
     Collection count after storage: 19
     ```
   - **Optimized Ingestion** (recommended):
     ```bash
     python embeddings.py
     ```
     This script skips already-processed PDFs to avoid duplicates.
     **Example Output**:
     ```
     Processing data\Hr Policies.pdf...
     Skipping data\Hr Policies.pdf as it has already been processed.
     Processing data\Human-Resources-Policy.pdf...
     Loaded 31 pages from Human-Resources-Policy.pdf
     Split into 31 chunks
     Stored 31 chunks for Human-Resources-Policy.pdf
     Collection count after storage: 50
     Marked Human-Resources-Policy.pdf as processed.
     PDF files ingestion completed successfully
     ```

### Querying the HR Agent
Once documents are ingested, query the system:

1. Start the query interface:
   ```bash
   python crew.py
   ```
2. Enter a query, e.g., "How does TCS conduct manpower planning?"
3. **Example Output**:
   ```
   TCS conducts manpower planning through the Manpower Allocation Task Committee (MATC), using a just-in-time hiring strategy to match associates’ skills to project needs, with a typical lead time of three weeks for replacements (Source: Hr Policies.pdf).
   ```

### Testing the Database
Verify that ChromaDB contains the ingested data:
```bash
python test_db.py
```
**Expected Output**:
```
Collection count: 19
```

---

## Architecture

HR Agent uses an **Agentic RAG** architecture orchestrated by CrewAI for a robust, multi-agent workflow.

### Components
- **`ingest.py`**: Loads PDFs, splits them into chunks, generates embeddings with Ollama’s `nomic-embed-text`, and stores them in ChromaDB.
- **`tools.py`**: Defines `ChromaDBRetrieverTool` to fetch relevant chunks based on query embeddings.
- **`agents.py`**:
  - **Retriever Agent**: Retrieves HR policy chunks from ChromaDB.
  - **Generator Agent**: Uses Mistral to summarize retrieved chunks into answers.
- **`task.py`**:
  - **Retrieval Task**: Fetches the top 5 relevant chunks.
  - **Generation Task**: Crafts a concise answer from the retrieved context.
- **`crew.py`**: Orchestrates agents and tasks to process user queries.
- **ChromaDB**: Stores chunks and embeddings at `C:\Users\SaikumarJarugumalli\Desktop\HR_Agent\chroma_db`.

### Workflow
1. **Ingestion**: PDFs are processed, chunked, and stored in ChromaDB with embeddings.
2. **Query Input**: User submits a query (e.g., "How does TCS conduct manpower planning?").
3. **Retrieval**: Retriever agent fetches the top 5 relevant chunks.
4. **Generation**: Generator agent summarizes the chunks into an answer.
5. **Output**: System returns the response.

![Workflow Diagram](workflow_diagram.png)

---

## Agentic RAG vs. Traditional RAG
- **Traditional RAG**: A single-step process (retrieve → generate).
- **Agentic RAG (This Project)**:
  - Collaborative multi-agent system (retriever + generator).
  - Orchestrated by CrewAI for dynamic workflows.
  - Extensible for additional agents (e.g., planners, validators).
- **Advantages**: Enables complex reasoning, tool integration, and scalability for enterprise use cases like HR policy management.

---

## Troubleshooting
- **Empty ChromaDB**: Ensure `ingest.py` or `embeddings.py` completed successfully and check `chroma_db` exists.
- **LLM Failure**: Confirm Ollama server is running (`ollama serve`) and Mistral is available (`ollama list`).
- **Retrieval Issues**: Verify query format and ChromaDB path in `tools.py`.
- **Logs**: Check `chromadb_tool.log` for detailed errors.

---

## Contributing
We welcome contributions! To get started:
1. Fork the repository.
2. Create a feature branch:
   ```bash
   git checkout -b feature/your-feature
   ```
3. Commit your changes:
   ```bash
   git commit -m "Add your feature"
   ```
4. Push to the branch:
   ```bash
   git push origin feature/your-feature
   ```
5. Open a pull request.

Follow the [code of conduct](CODE_OF_CONDUCT.md) and include tests for new features.

---

## License
This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

---

## Acknowledgments
- **CrewAI**: For agent orchestration.
- **ChromaDB**: For vector storage and retrieval.
- **Ollama**: For local LLM inference.
- **LangChain**: For document processing and embeddings.

---

## Contact
For questions or feedback, open an issue or email [saikumarjarugumalli@gmail.com](mailto:saikumarjarugumalli@gmail.com).

---

This README provides everything your team needs to understand, set up, and use the HR Agent project effectively. Happy querying!