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
- Store them in `config/db/chroma25`

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

## 🛡️ Hallucination Prevention

This chatbot applies multiple controls to minimize hallucinations:

- `temperature=0`: ensures deterministic, non-random answers
- Carefully engineered prompts to restrict the model to retrieved context only
- If the answer cannot be supported by the context, the bot responds:
  > *"No information available regarding this topic in the source documents."*

This enforces factual accuracy and guards against model guesswork.

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
├── app.py                  # GUI entry point
├── query_data.py          # RAG + GPT answer generator
├── create_database.py     # PDF embedding & ChromaDB setup
├── clean_abriviations.py  # German abbreviation normalizer
├── settings.py            # Configuration and path resolver
├── requirements.txt
├── config/
│   └── .env                # OpenAI API key configuration
├── data/
│   ├── books/              # Source PDFs
│   └── links/              # Moodle links in JSON format
└── user-testing/          # Saved user logs (CSV)
```

---

## 🔐 Notes

- Place all source PDFs under `data/books/`
- Moodle links must be stored as a JSON file at `data/links/links.json`
- Output logs from chatbot interactions are saved automatically

---

## 📌 Version

**v2.0** — Powered by OpenAI GPT-4o with a modular RAG-based backend and offline GUI support.

---

## 📜 License

This project is intended for academic use at FHTW. Not licensed for commercial distribution.
