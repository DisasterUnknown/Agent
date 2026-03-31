from src.models.qwen3_next_80b_a3b_instruct import QwenChatLLM
from src.utils.context_getter import get_context
from src.utils.duckduckgo_search import duckduckgo_search
from src.utils.scrape_webpage import scrape_webpage
from src.agents.responce_validate_agent import rag_answer_confirmation
import src.core.sys_msgs as sys_msgs
from langchain_core.prompts import ChatPromptTemplate


def webSearchAgent(user_prompt: str):
    context = None
    page_link = None
    context_found = False
    model = QwenChatLLM()
    count = 0
    
    search_query = webSearchQueryGeneration(user_prompt, model)
    if search_query[0] == '"':
        search_query = search_query[1:-1]
        
    search_results = duckduckgo_search(search_query)
    while not context_found and len(search_results) > 0 and count < 10:
        best_result = best_search_results(user_prompt, search_results, search_query, model)
        try:
            count += 1
            page_link = search_results[best_result]['link']
        except:
            print("Failed to do web search trying again....")
            best_result = 0
        
        page_text = scrape_webpage(page_link)
        search_results.pop(best_result)
        
        if page_text and contains_data_needed(user_prompt, page_text, search_query, model):
            context = page_text
            context_found = True
            
    prompt_template = ChatPromptTemplate.from_template(sys_msgs.WEB_SEARCH_AGENT_RESPONCE)
    prompt = prompt_template.format(context=context, question=user_prompt)

    response_text = model.invoke(prompt)
    rag_answer_confirmation(is_web_search=True, query_text=user_prompt, context_text=context, response_text=response_text, sources=[page_link], model=model)
    return
            
        
    
    
def webSearchQueryGeneration(user_prompt: str, model: QwenChatLLM):
    prompt_template = ChatPromptTemplate.from_template(
        sys_msgs.WEB_SEARCH_QUERY
    )
    prompt = prompt_template.format(question=user_prompt)
    
    response_text = model.invoke(prompt)
    return response_text

def best_search_results(user_prompt: str, s_results: list, query: str, model: QwenChatLLM):
    prompt_template = ChatPromptTemplate.from_template(
        sys_msgs.BEST_SEARCH_MSG
    )
    prompt = prompt_template.format(question=user_prompt, query=query, search_results=s_results, max_index=len(s_results) - 1)
    
    for _ in range(2):
        try:
            response_text = model.invoke(prompt)
            return int(response_text)
        except:
            continue
    
    return 0

def contains_data_needed(user_prompt: str, search_content: str, query: str, model: QwenChatLLM):
    prompt_template = ChatPromptTemplate.from_template(
        sys_msgs.CONTAINS_WEB_DATA_MSG
    )
    prompt = prompt_template.format(question=user_prompt, query=query, search_content=search_content)
    response_text = model.invoke(prompt)
    
    if 'true' in response_text.lower():
        return True
    else:
        return False