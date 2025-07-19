
# 🤖 AI Chatbot for FHTW – v2.0

A context-aware, OpenAI-powered chatbot designed to answer administrative queries using university-specific documents and links. 
It uses semantic search and GPT-based generation to deliver fast, filtered, and source-aware answers. 

---

## 🚀 Features

- 📄 Processes official documents (PDF) and links (JSON)  
- 🔢 Embedding using OpenAI's `text-embedding-ada-002` via LangChain  
- 🔍 Retrieval-Augmented Generation (RAG) using ChromaDB + GPT  
- 🧠 Context parsing with template-driven prompts  
- 💬 GPT-4o-powered answer generation via LangChain  
- 🖥️ GUI built using `tkinter` for local interaction  
- ✅ Feedback collection with thumbs-up/down and reasons  
- 🧑‍💻 User session logging to CSV for analysis  

---

## 🛠 Architecture Overview

```text
PDFs + Moodle Links
        ↓
Preprocessing (abbreviation cleanup)
        ↓
ChromaDB vector store (semantic chunks)
        ↓
RAG → LangChain + GPT-4o
        ↓
Answer generation + source attribution
        ↓
GUI Interface + Feedback Collection
```
---

## 📁 Project Structure
```bash
.
├── app.py                 # GUI entry point
├── query_data.py          # RAG + GPT answer generator
├── create_database.py     # PDF embedding & ChromaDB setup
├── clean_abbreviations.py  # German abbreviation normalizer
├── settings.py            # Configuration and path resolver
├── requirements.txt
├── config/
│   └── db/                 # Embedded data saved in ChromaDB
│   └── .env                # OpenAI API key configuration
├── data/
│   ├── books/              # Source PDFs
│   └── links/              # Source Links
└── user-testing/           # Saved user logs (CSV)
```
---

## 🧰 Environment

This project was developed using:

- **Conda**: 22.9
- **Python**: 3.10

Using a Conda environment is recommended for managing dependencies consistently.

---

## 📦 Dependencies

Install all required packages using:

```bash
pip install -r requirements.txt
```

Key libraries used:

- `langchain`, `langchain-community`, `openai`
- `chromadb`, `multilingual-pdf2text`
- `tkinter`, `nltk`, `spacy`, `torch`
- `fastapi`, `typer`, `pyngrok`

---
## 🛡️ Hallucination Prevention

To ensure the chatbot stays accurate and doesn't "make things up," several controls were implemented:

- Only the top 10 most relevant results will kept. However to be accepted, the similarity score must be at least 0.50 or above.
- The RAG pipeline builds a context based on the user query, retrieved results, and rules.
- The GPT model (LLM) then responds strictly using this context.
- If there’s no relevant context to answer the question properly, the chatbot will clearly say:
> *"Sorry, I can't find any information on this topic."*
- Setting temperature=0 should result in deterministic (non-random) output.



---

## 🧾 Feedback Logging

User interactions are saved in CSV format, including:

```csv
ID, Question, Answer, Thumbsup, Thumbsdown, Reason, ResponseTime
```
`ResponseTime` is recorded automatically.

Files are stored in the `user-testing/` directory and auto-generated per session.

---


## 🎓 Lessons Learned


**Garbage in, garbage out**       ~ Preprocessing and cleaning was crutial in chatbot accuracy 

**Hallucinations happen**        ~ Key is how to control and filter it confidently

**User feedback is everything**   ~ Real user interaction surfaces issues and gaps that internal testing simply can't replicate

---

## 🧠 Query Logic

- Uses a **Retrieval-Augmented Generation (RAG)** pipeline
- Retrieves semantically relevant content from ChromaDB
- Injects the results into a prompt using LangChain
- GPT-4o generates a response strictly based on the context
- If no match is found, the chatbot responds accordingly

---
## ⚙️ Getting Started

### 1. Create Chroma Vector DB

```bash
python create_database.py
```

This will:
- Process all PDF files in `data/books`
- Generate embeddings
- Store them in `config/db`

### 2. Launch the Chatbot GUI

```bash
python app.py
```

The application opens a GUI where users can type questions and receive AI-generated responses with source references.

---

## 📌 Version

**v2.0** — Powered by OpenAI GPT-4o with a modular RAG-based backend and offline GUI support.

---

## 📜 License

This project is intended for academic use at FHTW. Not licensed for commercial distribution.
