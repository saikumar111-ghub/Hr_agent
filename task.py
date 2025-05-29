from crewai import Task
from agents import retriever_agent, generator_agent

# Retrieval task: Retrieve relevant document chunks
retrieval_task = Task(
    description="Retrieve relevant HR policy chunks from the database based on the query: {query}",
    expected_output="A paragraph of relevant document chunks with sources listed at the end.",
    agent=retriever_agent
)

# Generation task: Generate an answer using the retrieved chunks
generation_task = Task(
    description="Generate a clear and concise answer based on the retrieved document chunks (up to 1000 words) for the query: {query}",
    expected_output="A well-structured and concise answer to the user's query from the knowledge base.",
    agent=generator_agent,
    context=[retrieval_task]  # Use retrieval_task output as context
)