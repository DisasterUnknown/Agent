import src.core.sys_msgs as sys_msgs
from src.models.llama_3_3_nemotron_super_49b_v1 import NemotronLLM
from src.utils.context_getter import get_context
from src.agents.web_search_agent import webSearchAgent
from src.agents.rag_agent import rag_agent
from src.agents.ai_agent import ai_agent
from langchain_core.prompts import ChatPromptTemplate

def super_agent(user_prompt: str):
    model = NemotronLLM()
    prompt_template = ChatPromptTemplate.from_template(sys_msgs.USER_AGENT_SELECTION_TEMPLATE)
    prompt = prompt_template.format(question=user_prompt)

    response_text = model.invoke(prompt)
    response_text = response_text.strip().lower()
    
    if response_text == "true":
        rag_agent(user_prompt)
    elif response_text == "false":
        webSearchAgent(user_prompt)
    else:
        decition_agent(user_prompt, model)

def decition_agent(user_prompt: str, model: NemotronLLM):
    context = get_context(user_prompt)
    prompt_template = ChatPromptTemplate.from_template(sys_msgs.AGENT_IDENTIFICATION_TEMPLATE)
    prompt = prompt_template.format(context=context, question=user_prompt)

    response_text = model.invoke(prompt)
    response_text = response_text.strip().lower()
    
    if response_text == "true":
        rag_agent(user_prompt)
    elif response_text == "false":
        webSearchAgent(user_prompt)
    else:
        ai_agent(user_prompt)