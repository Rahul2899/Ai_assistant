from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from config import llm

def resolve_incident(issue_description, system_context):
    template = """
    You are an AI assistant for IT operations. The user has described the following issue:
    {issue_description}
    
    Here's the current system overview:
    {system_context}
    
    Based on this information, please provide:
    1. A brief analysis of the potential root cause
    2. Step-by-step resolution instructions
    3. Any preventive measures to avoid similar issues in the future

    Be concise and clear in your response.
    """
    prompt = PromptTemplate(template=template, input_variables=["issue_description", "system_context"])
    chain = LLMChain(llm=llm, prompt=prompt)
    
    response = chain.invoke({"issue_description": issue_description, "system_context": system_context})
    return response['text']

def get_alternative_solution(issue_description, system_context):
    template = """
    You are an AI assistant for IT operations. The user has described the following issue:
    {issue_description}
    
    Here's the current system overview:
    {system_context}
    
    Please provide an alternative solution to this issue, different from the standard approach. Include:
    1. A brief explanation of why this alternative might be beneficial
    2. Step-by-step instructions for implementing this alternative solution
    3. Any potential drawbacks or considerations for this approach

    Be concise and clear in your response.
    """
    prompt = PromptTemplate(template=template, input_variables=["issue_description", "system_context"])
    chain = LLMChain(llm=llm, prompt=prompt)
    
    response = chain.invoke({"issue_description": issue_description, "system_context": system_context})
    return response['text']