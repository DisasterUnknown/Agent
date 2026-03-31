## Project overview

This repository contains a Python first artificial intelligence assistant that combines retrieval augmented generation web search and direct model calls The goal is to provide a complete example that another engineer can understand and explain just by reading this document and browsing the code

The assistant reads configuration from YAML files uses language models for routing answering and scoring searches the open web when needed and builds a vector database from PDF documents for retrieval augmented answers

## Repository layout

config holds YAML configuration files for keys model names API URLs and data paths
src agents contains routing agents retrieval agents web search agents direct AI agents and validation scoring agents
src models wraps external chat embedding and reward models behind small Python classes
src utils contains utilities for embeddings persistence PDF loading document chunking web search HTML scraping context construction and database population
main py is the command line entry point that wires everything together

## Configuration files

There are two main YAML configuration files

config yaml is a shared template used by different people and should not be ignored in version control
config_dev yaml is for local development settings and is ignored through the git ignore file so each contributor can keep private keys and local paths outside version control

Typical configuration values include

API keys and secret tokens
model names and endpoints
search provider settings
database and vector store configuration
feature flags and debug options

## Required Python packages

Install the dependencies from `requirements.txt` so the code can run in a fresh environment

openai is used by the model wrappers for chat completion and scoring
langchain core provides prompt templates used by multiple agents
langchain community and langchain text splitters handle PDF loading and text chunking for RAG
langchain chroma and chromadb provide the persistent vector store used by the retrieval flow
playwright is used to gather DuckDuckGo search results
trafilatura converts fetched HTML into clean text for use by the web search flow
pypdf is required by the PDF loader used during database population
pyyaml is used to load YAML configuration

If you add new imports in the code you should also update `requirements.txt` so a new user can install everything from one place

### Install in one command

Create and activate a virtual environment then run a single pip command that reads from the requirements file so every dependency is installed together

```text
pip install all packages listed in requirements txt
```

## Setup and run commands

The following steps describe how to prepare a fresh environment for this project

Create a Python virtual environment using the built in venv module and activate it for your platform
Install dependencies inside the active environment using pip

```powershell
python -m pip install -r requirements.txt
python -m playwright install chromium
```

Prepare configuration

Edit `config/config.yaml` and put your API keys and any local overrides in that file
The loader in `config/load_config.py` looks for `config/config.yaml`

Prepare data for RAG

Put your input PDF files under `src/data/pdf`
On first run you should build the vector database so retrieval has content to search

Run modes

Interactive chat mode starts a prompt loop by calling `super_agent` for each user message

```powershell
python .\main.py
```

Update mode populates the Chroma database from PDFs under `src/data/pdf`

```powershell
python .\main.py --update
```

Reset mode removes the existing vector database directory and then repopulates it from the PDFs

```powershell
python .\main.py --reset
```

Recommended first run on a new machine is `python .\main.py --update` and then `python .\main.py`

Interactive input details

When running without arguments the program reads from stdin and expects you to type one prompt per line
Type `exit` or `bye` to stop the loop

Configured paths used by the database

By default `config/config_dev.yaml` sets `paths.data_dir` to `src/data/pdf` and `paths.db_dir` to `src/data/chroma_db`
During `--update` and `--reset` the code loads PDFs from `src/data/pdf` and stores vectors persistently under `src/data/chroma_db`

Key modules and what they do

`main.py` provides the command line entry point and the interactive prompt loop
It reads `--update` and `--reset` then calls `populate_database` to build or rebuild the Chroma database

`src/agents/routing_agent.py` contains `super_agent` which routes a user prompt to one of the flows
It uses `NemotronLLM` and a routing prompt template to decide between RAG web search or direct AI answering

`src/agents/rag_agent.py` contains `rag_agent`
It calls `get_context` to retrieve relevant passages from Chroma then invokes `QwenChatLLM` using the RAG prompt template

`src/agents/web_search_agent.py` contains `webSearchAgent`
It generates a DuckDuckGo query using `QwenChatLLM` then uses `duckduckgo_search` and `scrape_webpage`
It finally asks `QwenChatLLM` to produce the answer from the extracted page text

`src/agents/ai_agent.py` contains `ai_agent`
It directly prompts `QwenChatLLM` without RAG or web search context

`src/agents/responce_validate_agent.py` contains `rag_answer_confirmation`
It uses `NemotronRewardModel` to compute how well the generated answer matches the question and the provided context then prints a credibility report

`src/utils/context_getter.py` contains `get_context`
It builds a `Chroma` retriever with an embedding function then runs similarity search against the stored vectors

`src/utils/populate_database.py` contains `populate_database`
It loads PDFs from `src/data/pdf` splits them into chunks and writes vectors to the Chroma persistence directory

`src/utils/duckduckgo_search.py` uses Playwright to scrape DuckDuckGo HTML results
`src/utils/scrape_webpage.py` uses Trafilatura to download and extract clean text from a URL

## How the system works end to end

At startup the code loads configuration from the YAML files using the loader in the config folder This provides values for model selection API endpoints search provider settings and any feature flags that affect behavior

Then the entry script constructs agent objects defined under src agents Each agent focuses on a single task For example a routing agent decides which path to take for a given query a web search agent calls external search a retrieval agent talks to the embedding store while separate reward and validation agents score and check outputs from language models

Model wrapper modules under src models hide provider specific details They receive prompts plus configuration values and return responses in a consistent format so the rest of the code does not depend on any provider specific client

Utility modules under src utils support all agents For instance one module may call a search API another may fetch and parse HTML pages another may build context windows around retrieved passages and another may manage embedding and database interaction for retrieval augmented generation

For every user query the high level flow is

Configuration provides which models tools and parameters to use
Routing or planner logic decides what sequence of agents or tools should run
Web search and scraping utilities gather external information where needed
Embedding utilities convert text into vector form and query the store for relevant context
Language model wrappers generate answers possibly scored or filtered by reward and validation agents
The final response is returned to the caller in either text or structured form
