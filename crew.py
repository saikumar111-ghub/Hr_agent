import os
import sys
from dotenv import load_dotenv
from crewai import Crew, Process
from agents import retriever_agent, generator_agent
from task import retrieval_task, generation_task

load_dotenv()
os.environ["LITELLM_LOG"] = "ERROR"
os.environ["CREWAI_DISABLE_TELEMETRY"] = "true"

# Get the query from command-line argument or user input
if len(sys.argv) < 2:
    query = input("Please enter your query: ")
else:
    query = sys.argv[1]
print(f"Processing query: {query}")

# Initialize the crew with agents and tasks
crew = Crew(
    agents=[retriever_agent, generator_agent],
    tasks=[retrieval_task, generation_task],
    process=Process.sequential,
    verbose=True,
    embedder={
        "provider": "ollama",
        "config": {
            "model": "nomic-embed-text",
            "base_url": "http://localhost:11434"
        }
    }
)

# Run the crew and handle any errors
try:
    result = crew.kickoff(inputs={"query": query})
    print("\nFinal Answer:")
    print(result)
except Exception as e:
    print(f"Error processing query: {str(e)}")