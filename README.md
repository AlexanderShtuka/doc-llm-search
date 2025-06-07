# Perplexity-Style AI Search Tool

A lightweight, open-source AI-powered search and answer engine inspired by Perplexity.ai. This tool uses LangChain and OpenAI to answer natural language questions based on your local `.txt` files, and optionally falls back to live web search using Tavily when needed.

## Features

- Ask natural language questions
- Retrieves answers from your own `.txt` documents
- Falls back to web search when local context is insufficient
- Summarizes results using GPT-4 or GPT-3.5
- Displays source citations for transparency
- Streamlit web interface

## Requirements

- Python 3.9+
- OpenAI API key
- Tavily API key (for optional web search)
- Text files placed in the `docs/` directory

## Technologies Used

| Feature            | Library / Tool           |
|--------------------|--------------------------|
| LLM                | OpenAI (via LangChain)   |
| Vector Search      | Chroma                   |
| Document Embedding | OpenAI Embeddings        |
| Web Search         | Tavily                   |
| UI Framework       | Streamlit                |
| File Format        | Plain `.txt` files       |

## How to Use

### 1. Add Your `.txt` Files

Place plain text documents into the `docs/` folder. These will serve as the knowledge base for answering questions.

### 2. Set Your API Keys

Create a `.env` file in the root directory with your OpenAI and Tavily API keys:

If you don’t want web search fallback, you can omit the `TAVILY_API_KEY` and the app will just use your local documents.

### 3. Create a Python Virtual Environment

```bash
python -m venv llmenv
source llmenv/bin/activate         # On Windows: llmenv\Scripts\activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Start the App
```bash
streamlit run app.py
Open the link shown in the terminal (usually http://localhost:8501) to use the app in your browser.
```