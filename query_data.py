import logging
from settings import OPENAI_API_KEY
from langchain_community.vectorstores import Chroma
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_openai.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

CHROMA_PATH = "config/db/chroma25"

# Set logging level to CRITICAL to reduce verbosity
logging.basicConfig(level=logging.CRITICAL)
embedding_function = OpenAIEmbeddings(api_key=OPENAI_API_KEY)
db = Chroma(
    persist_directory=CHROMA_PATH,
    embedding_function=embedding_function,
    collection_metadata={"hnsw:space": "cosine"} # cosine similarity search
)


model = ChatOpenAI(
    api_key=OPENAI_API_KEY,
    temperature=0,
    model="gpt-4o",
    max_tokens=4000,
    streaming=True,
)

input_prompt = ("""You are a context parser that parses the context given below and checks for grammar. Correct any grammatical mistakes in the text for the output. Extract answer from the context. Answer should be relevant to the question asked, and ensure it makes complete sense.
Strictly follow these formatting rules for answer and ensure all the placeholder values in the format below are filled with no hallucinations:
Template guideline:
1. If content from a file is found, format it as:
    A. File: [Filename] [file-link] "content"
    B. File: [Filename] [file-link] "content"
2. If a relevant Moodle link is found, format it as:
    A. Moodle: [Moodle-Name] [Moodle-Link]
    B. Moodle: [Moodle-Name] [Moodle-Link]
{context}
QUESTION: 
{question}
You don’t answer questions that you have no context about the question, by stating it in German in 3 Words.
The information should be focused to comprehensively answer the only question!
For broad questions give all the relevant info you have in the context.
In answering about time or specific date, please be careful to include if applicable warnings such as changes of time in a different time!
The answer should be sanitized from tabs, spaces, half-sentences, left alone tokens and double whitespaces!
Don’t give redundant info read and give the answer accordingly to the question.
Don’t alter the content in the direct quotation to answer the question.
Give precise info.
You never talk on your own!
Pls respect the Template guideline.

ANSWER:
""")

prompt = PromptTemplate(template=input_prompt, input_variables=["context", "question"])

llm_chain = LLMChain(llm=model, prompt=prompt)

def generate_answer(user_input):
    query_text = user_input
    if not query_text.strip():
        return "Please ask a specific question."

    try:
        results = db.similarity_search_with_relevance_scores(query_text, score_threshold=0.50, k=10)
        print(results)
        adjusted_results = [(doc, score) for doc, score in results]
    except Exception as e:
        logging.error(f"Error during similarity search: {e}")
        return "An error occurred while searching for relevant information."

    if not adjusted_results or all(score < 0.50 for _, score in adjusted_results):
        return "Sorry, I can't find any information on this topic."


    combined_context = "\n\n".join(
        f"[Filename: {doc.metadata['filename']}] "
        #f"[Page {doc.metadata['page-number']}] "
        f"[file-Link: {doc.metadata['link']}]"
        f"<{doc.page_content}>"
        if doc.metadata.get('filename', None) is not None
        else (
            f"[Moodle-Name: {doc.metadata.get('title', '')}] "
            f"[Moodle-Link: {doc.metadata.get('link', '')}]"
            f"[Moodle-Description: {doc.metadata.get('description', 'nada')}]"
        )
        for doc, score in adjusted_results if score >= 0.10
    )


    print("test + test + test + test + test")
    print(combined_context)
    print("test + test + test + test + test")

    # Useing the QA chain to generate the final response
    final_result = llm_chain({"context": combined_context, "question": "Filter the lines according to the question: " + query_text})

    # Extract and format the final result
    print(final_result.keys())
    answer = final_result['text']

    return answer


# Example Test Cases
if __name__ == "__main__":
    user_query = "Wie setzt sich der Bachelor Wirtschaftsinformatik zusammen?"
    user_query = "Who is the director of FHTW?"
    user_query="wer sind die geschäftsführer der fhtw?"
    user_query="wie sieht die Bachelorpräsentation aus?"
    user_query = "Information about the fire safety."
    user_query = "bis wann kann ich  mein sprachzertifikat  vorlegen?"
    print("Sie: " + user_query)
    answer = generate_answer(user_query)
    print("Assistent: " + answer)
