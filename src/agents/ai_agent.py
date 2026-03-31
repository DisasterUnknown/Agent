from src.models.qwen3_next_80b_a3b_instruct import QwenChatLLM
import src.core.sys_msgs as sys_msgs
from langchain_core.prompts import ChatPromptTemplate
from src.agents.responce_validate_agent import rag_answer_confirmation

def ai_agent(user_prompt: str):
    model = QwenChatLLM()
    context_text = "Context has nothing to do here since this is directly for the LLM"
    prompt_template = ChatPromptTemplate.from_template(sys_msgs.AI_AGENT_TEMPLATE)
    prompt = prompt_template.format(question=user_prompt)

    response_text = model.invoke(prompt)
    rag_answer_confirmation(is_web_search=None, query_text=user_prompt, context_text=context_text, response_text=response_text, sources=[], model=model)
    return