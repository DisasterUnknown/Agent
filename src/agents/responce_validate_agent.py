from src.models.qwen3_next_80b_a3b_instruct import QwenChatLLM
from src.models.llama_3_1_nemotron_70b_reward import NemotronRewardModel
from src.agents.responce_reward_agent import responce_reward
import src.core.sys_msgs as sys_msgs
from langchain_core.prompts import ChatPromptTemplate

def rag_answer_confirmation(
    query_text: str,
    context_text: str,
    response_text: str,
    sources: list,
    model: QwenChatLLM,
    is_web_search: bool | None = None,
):
    scorer = NemotronRewardModel()
    question_answer_score = responce_reward(query_text, response_text, scorer)
    context_answer_score = responce_reward(context_text, response_text, scorer)

    question_answer_score = max(0.0, min(1.0, question_answer_score))
    context_answer_score = max(0.0, min(1.0, context_answer_score))

    if abs(question_answer_score - context_answer_score) > 0.4:
        final_score = min(question_answer_score, context_answer_score) * 0.5
    else:
        final_score = (question_answer_score + context_answer_score) / 2

    if final_score < 0.04:
        verification_template = ChatPromptTemplate.from_template(
            sys_msgs.ERROR_RESPONSE_TEMPLATE
        )

        prompt = verification_template.format(question=query_text, response=response_text)
        error_response_text = model.invoke(prompt)

        formatted_result = (
            f"Response: {error_response_text}\n"
            f"Question: {query_text}\n"
            f"Question-Answer Score: {question_answer_score:.3f}\n"
            f"Context-Answer Score: {context_answer_score:.3f}\n"
            f"Final Credibility Score: {final_score:.3f}\n"
            f"Sources: {sources}\n"
            f"Type: {'Web Search' if is_web_search is True else 'RAG' if is_web_search is False else 'AI'}"
        )
    else:
        formatted_result = (
            f"Response: {response_text}\n"
            f"Question-Answer Score: {question_answer_score:.3f}\n"
            f"Context-Answer Score: {context_answer_score:.3f}\n"
            f"Final Credibility Score: {final_score:.3f}\n"
            f"Sources: {sources}\n"
            f"Type: {'Web Search' if is_web_search is True else 'RAG' if is_web_search is False else 'AI'}"
        )

    print(formatted_result)
