import os
from dotenv import load_dotenv
from crewai import Agent
from tools import ChromaDBRetrieverTool
from langchain_ollama import OllamaLLM

load_dotenv()

model_name = "ollama/" + os.getenv("OLLAMA_MODEL", "mistral")

llm = OllamaLLM(
    model=model_name,
    base_url="http://localhost:11434",
    verbose=True
)

# Create an instance of the retriever tool
retriever_tool = ChromaDBRetrieverTool()

# Document Retriever Agent: Finds relevant HR document chunks
retriever_agent = Agent(
    role="Document Retriever",
    goal="Retrieve relevant HR policy chunks from the database based on the user's query.",
    backstory="You are an expert at finding relevant information in HR documents.",
    tools=[retriever_tool],
    llm=llm,
    verbose=True,
    allow_delegation=False
)

# Answer Generator Agent: Generates answers based on retrieved chunks
generator_agent = Agent(
    role="Answer Generator",
    goal="Generate a clear and concise answer based on the retrieved document chunks.",
    backstory="You are an HR specialist who can summarize policy information accurately.",
    llm=llm,
    verbose=True,
    allow_delegation=False
)