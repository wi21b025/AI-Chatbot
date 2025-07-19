
# 🤖 AI Chatbot for FHTW – v2.0

A context-aware, OpenAI-powered chatbot designed to answer administrative and academic queries using university-specific documents and Moodle links. It uses semantic search and GPT-based generation to deliver fast, filtered, and source-aware answers.

---

## 🚀 Features

- 🔍 Retrieval-Augmented Generation (RAG) using ChromaDB + GPT
- 💬 GPT-4o-powered answer generation via LangChain
- 🧠 Context parsing with template-driven prompts
- 📄 Processes official documents (PDF) and Moodle links
- ✅ Feedback collection with thumbs-up/down and reasons
- 🧑‍💻 User session logging to CSV for analysis
- 🖥️ GUI built using `tkinter` for local interaction

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

Set your OpenAI API key in a `.env` file under `config/`:

```env
OPENAI_API_KEY=your-openai-key-here
```

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

## 🧠 Query Logic

- Uses a **Retrieval-Augmented Generation (RAG)** pipeline
- Retrieves semantically relevant content from ChromaDB
- Injects the results into a prompt using LangChain
- GPT-4o generates a response strictly based on the context
- If no match is found, the chatbot responds accordingly

---

## 🧰 Environment

This project was developed using:

- **Conda**: 22.9
- **Python**: 3.10

Using a Conda environment is recommended for managing dependencies consistently.

---

## 🛡️ Hallucination Prevention

To ensure the chatbot stays accurate and doesn't "make things up," several controls were implemented:

- It only shows answers if at least one source in the top 10 search results scores above 0.50 relevance.
- after wards thorug the promt the answares would be filtered if they are relevant ot the question
- The GPT model is prompted to respond strictly based on the retrieved context and nothing else.
- With `temperature=0`, the model always returns the most likely, non-random output.

If there’s not enough context to answer the question properly, the chatbot will clearly say:
> *"Sorry, I can't find any information on this topic."*

---


## 🧾 Feedback Logging

User interactions are saved in CSV format, including:

```csv
ID, Question, Answer, Thumbsup, Thumbsdown, Reason, ResponseTime
```

Files are stored in the `user-testing/` directory and auto-generated per session.

---

## 📁 Project Structure

```bash
.
├── app.py                 # GUI entry point
├── query_data.py          # RAG + GPT answer generator
├── create_database.py     # PDF embedding & ChromaDB setup
├── clean_abriviations.py  # German abbreviation normalizer
├── settings.py            # Configuration and path resolver
├── requirements.txt
├── config/
│   └── db/               
│   └── .env                # OpenAI API key configuration
├── data/
│   ├── books/              # Source PDFs
│   └── links/              # Source Links
└── user-testing/           # Saved user logs (CSV)
```

---

## 🎓 Lessons Learned


**Garbage in, garbage out**       ~ Preprocessing and cleaning was crutial in chatbot accuracy 

**Hallucinations happens**        ~ Key is how to control and filter it confidently

**User feedback is everything**   ~ Real user interaction surfaces issues and gaps that internal testing simply can't replicate

---

## 📌 Version

**v2.0** — Powered by OpenAI GPT-4o with a modular RAG-based backend and offline GUI support.

---

## 📜 License

This project is intended for academic use at FHTW. Not licensed for commercial distribution.
