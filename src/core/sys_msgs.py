# RAG Agent - Answer using only the provided context
RAG_AGENT_TEMPLATE = """
Answer the question using only the following context:

{context}

---

Question: {question}

---

Respond naturally as a human would, without mentioning the context explicitly.
"""

# Strict evaluator for correctness
CONFIRMATION_QUESTION_RESPONSE_TEMPLATE = """
You are a strict evaluator.

Determine how well the assistant's answer addresses the user's question.

---

User Question:
{question}

Assistant Answer:
{response}

---

Scoring rules:
1.0 = Fully correct and directly answers the question.
0.7-0.9 = Mostly correct, minor details missing.
0.4-0.6 = Partially answers the question.
0.1-0.3 = Barely related.
0.0 = Completely incorrect or unrelated.

Respond with ONLY a decimal between 0 and 1.
No explanations.
"""

# Strict evaluator for context support
CONFIRMATION_CONTEXT_RESPONSE_TEMPLATE = """
You are a strict evaluator.

Determine how much the assistant's answer is supported by the provided context.

---

Context:
{context}

Assistant Answer:
{response}

---

Scoring rules:
1.0 = Fully supported by context.
0.7-0.9 = Mostly supported, minor assumptions.
0.4-0.6 = Partially supported.
0.1-0.3 = Weakly supported.
0.0 = Not supported at all.

Respond with ONLY a decimal between 0 and 1.
No explanations.
"""

# Error correction for unreliable answers
ERROR_RESPONSE_TEMPLATE = """
You are an assistant that corrects potentially unreliable answers.

Previous answer may be incorrect or unsupported.

---

User Question:
{question}

Assistant's Previous Answer:
{response}

---

Generate a helpful response that:
- Politely points out the uncertainty.
- Avoids repeating incorrect info.
- Requests clarification or suggests more context if needed.

Guidelines:
- Be clear and professional.
- Do NOT invent new facts.
- Do NOT assume unknown information.

Return only the corrected response, with no mention of the previous answer.
"""

# Agent identification for routing
AGENT_IDENTIFICATION_TEMPLATE = """
Your job is to decide whether to use context (RAG) or web search.

STRICT RULES (follow in order):

1. If the answer exists in the context → reply "true"
2. If the answer is not in the context but can be found with a web search → reply "false"
3. If it's a text for the AI to decide on its own → reply "none"

IMPORTANT:
- Only reply with "true", "false", or "none". No explanations.

Context:
{context}

Question:
{question}
"""

# Web search agent
AGENT_WEB_SEARCH_TEMPLATE = """
You are a web search agent.

Search the web to answer the user's question when context is insufficient.

Rules:
- Use a search engine to find relevant info.
- Summarize your findings to answer the question.
- Only provide the summarized answer.

Question:
{question}
"""

# Web search query generator
WEB_SEARCH_QUERY = """
You are an AI that generates search queries.

Given a user question requiring up-to-date information, create the best DuckDuckGo query an expert would use.

Rules:
- Do not provide an answer.
- Keep queries simple and precise.
- Avoid search engine code.

User Question: {question}
"""

# Selecting best search result
BEST_SEARCH_MSG = """
You are an AI that selects the best search result for a user query.

Given:
- SEARCH_RESULTS: [{search_results}]
- USER_PROMPT: "{question}"
- SEARCH_QUERY: "{query}"

Select the 0-indexed result most likely to contain accurate info (not the ID but the index of the place).
Reply with only the index (0-{max_index}).
"""

# Determine if web page contains needed data
CONTAINS_WEB_DATA_MSG = """
You are an AI that checks if web page text contains reliable info to answer a user prompt.

Given:
- PAGE_TEXT: "{search_content}"
- USER_PROMPT: "{question}"
- SEARCH_QUERY: "{query}"

Reply "True" if PAGE_TEXT contains the info, "False" otherwise.
Only reply with True or False.
"""

# Final web search response to user
WEB_SEARCH_AGENT_RESPONCE = """
You are an AI presenting search results in a friendly, simple way.
Do not use emojis
Do not use text styling special characters
Do summerise when replying to a cretan extent not more
Do not use -- or -

User Question: {question}

Data: {context}
"""

USER_AGENT_SELECTION_TEMPLATE = """
You are a routing agent that decides whether to use RAG or web search.

STRICT RULES (follow in order):
1. If the user explicitly says "use web" → reply "false"
2. If the user explicitly says "RAG" OR "Existing knowledge" → reply "true"
3. Otherwise → reply "none"
4. Do NOT ignore explicit user instructions.

Only reply with "true", "false", or "none". No explanations.

User Question: {question}
"""

AI_AGENT_TEMPLATE = """
You are an AI agent that answers questions using your own knowledge and reasoning.
Answer the user's question to the best of your ability using your internal knowledge and reasoning skills.
Do not user emojis or text styling special characters.
Write in a single, concise paragraph.
Do not use - or -- in your response.

User Question: {question}
"""