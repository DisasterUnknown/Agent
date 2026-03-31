from src.models.qwen3_next_80b_a3b_instruct import QwenChatLLM
from src.utils.context_getter import get_context
from src.agents.responce_validate_agent import rag_answer_confirmation
import src.core.sys_msgs as sys_msgs
from langchain_core.prompts import ChatPromptTemplate


def rag_agent(user_prompt: str):
    model = QwenChatLLM()

    context, results = get_context(user_prompt)
    sources = [doc.metadata.get("id", None) for doc, _score in results]
    chat_history = []

    prompt_template = ChatPromptTemplate.from_template(sys_msgs.RAG_AGENT_TEMPLATE)
    prompt = prompt_template.format(context=context, question=user_prompt)

    response_text = model.invoke(prompt)
    rag_answer_confirmation(is_web_search=False, query_text=user_prompt, context_text=context, response_text=response_text, sources=sources, model=model)
    return


