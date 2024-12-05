from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from config import llm
import random

def get_system_overview():
    # Simulate fetching data from various systems
    systems = [
        "Database Server",
        "Web Server",
        "Application Server",
        "Authentication Service",
        "Network Infrastructure",
        "Storage System"
    ]
    
    raw_data = {}
    for system in systems:
        status = random.choice(["Online", "Offline", "Degraded"])
        cpu_usage = random.randint(0, 100)
        memory_usage = random.randint(0, 100)
        
        raw_data[system] = {
            "status": status,
            "cpu_usage": cpu_usage,
            "memory_usage": memory_usage
        }
    
    # Generate a summary using LangChain
    template = """
    You are an AI operations assistant. Summarize the current status of the following systems:
    {systems_status}
    Provide a brief overview of the overall system health, highlighting any issues or areas that need attention.
    Be concise and clear, using no more than 3-4 sentences.
    """
    prompt = PromptTemplate(template=template, input_variables=["systems_status"])
    chain = LLMChain(llm=llm, prompt=prompt)
    
    systems_status_str = "\n".join([f"{system}: {data['status']} (CPU: {data['cpu_usage']}%, Memory: {data['memory_usage']}%)" for system, data in raw_data.items()])
    response = chain.invoke({"systems_status": systems_status_str})
    
    return {
        "raw_data": raw_data,
        "summary": response['text']
    }