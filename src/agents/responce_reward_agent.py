from src.models.llama_3_1_nemotron_70b_reward import NemotronRewardModel
from langchain_core.prompts import ChatPromptTemplate
import src.core.sys_msgs as sys_msgs

def responce_reward(context_text: str, response_text: str, scorer: NemotronRewardModel):
    verification_template = ChatPromptTemplate.from_template(
        sys_msgs.CONFIRMATION_CONTEXT_RESPONSE_TEMPLATE
    )

    prompt = verification_template.format(context=context_text, response=response_text)

    return scorer.score(prompt)
