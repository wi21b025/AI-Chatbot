import os
import re
import json
from langchain_experimental.text_splitter import SemanticChunker
from multilingual_pdf2text.pdf2text import PDF2Text
from multilingual_pdf2text.models.document_model.document import Document as DocumentModel
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.schema import Document
from settings import OPENAI_API_KEY

openai_embds = OpenAIEmbeddings()
CHROMA_PATH = "config/db/chroma25"
DATA_PATH = "data/books"
LINKS_JSON_PATH = "data/links/links.json"  # Path to JSON file containing moodle links


def main():
    generate_data_store() # pdf
    save_links_to_chroma() # links

def generate_data_store():
    documents, fns, sls, pns = load_documents_v2()
    print(len(documents))
    chunks = split_text_v2(documents, fns, sls)
    save_to_chroma(chunks, 'documents')

# https://github.com/jfilter/german-abbreviations/blob/master/README.md
with open('data/books/storage/german_abbreviation_new.txt', 'r') as fin:
    words = fin.read().split()

re_compiled = [re.compile(word.replace('.', '\.')) for word in words]
sub_value = [word.replace('.', '') for word in words]
re_num_compiled = re.compile(r'[0-9]+\.[^\d]')
def preprocess_data(text):
    new_text = text
    for index in range(len(re_compiled)):
        new_text = re_compiled[index].sub(sub_value[index], new_text)
    # https://github.com/jfilter/german-abbreviations/tree/master  <- This is important for the preprocessing of words in german.
    found_numbers = re_num_compiled.findall(new_text)
    if len(found_numbers) > 0:
        new_found_numbers = []
        for each_found_num in found_numbers:
            new_found_numbers.append(each_found_num.replace('.', ''))
        new_strings = re_num_compiled.split(new_text)
        new_text1 = new_strings[0] + new_found_numbers[0]
        for index in range(1, len(new_strings)):
            if index == len(new_strings) - 1:
                new_text1 += new_strings[index]
            else:
                new_text1 += new_strings[index]  + new_found_numbers[index]
        return new_text1
    else:
        return new_text
def load_documents_v2():
    documents = []
    filenames = []
    source_links = []
    page_numbers = []
    for filename in os.listdir(DATA_PATH):
        if filename.endswith('.pdf'):
            file_path = os.path.join(DATA_PATH, filename)
            pdf_document = DocumentModel(
                document_path=file_path,
                language='deu'
            )
            pdf2text = PDF2Text(document=pdf_document)
            content = pdf2text.extract()
            if "Cleaned_Code_of_Conduct_Deutsch" in filename:
                page_number = 1
                link = 'https://cis.technikum-wien.at/cms/dms.php?id=2032'
                filename_new = 'Code_of_Conduct_Deutsch'
            elif "Cleaned_Hausordnung" in filename:
                page_number = 5
                link = 'https://cis.technikum-wien.at/cms/dms.php?id=213311'
                filename_new = 'Hausordnung'
            else:
                page_number = 3
                link = 'https://cis.technikum-wien.at/cms/dms.php?id=1371'
                filename_new = 'Satzung'
            current_document = []
            for index, each_page in enumerate(content):
                print(type(each_page['text']), len(each_page['text']))
                cleaned_text = each_page['text']
                current_document.append(cleaned_text)
                #filenames.append(filename_new)
                #source_links.append(link)
                page_numbers.append(page_number + index)
            current_document = '\f'.join(current_document)
            documents.append(preprocess_data(current_document))
            filenames.append(filename_new)
            source_links.append(link)
    return documents, filenames, source_links, page_numbers

def split_text_v1(documents):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=500, length_function=len, add_start_index=True)
    chunks = text_splitter.split_documents(documents)
    return chunks

def split_text_v2(documents, fns, sls):
    final_chunks = []

    print(tuple(zip(fns, sls)))
    text_splitter = SemanticChunker(openai_embds)
    for index, each_document in enumerate(documents):
        pages = each_document.split('\f')

        for page_number, page_content in enumerate(pages, start=1):
            # Create chunks using SemanticChunker
            # page_content = each_document
            chunks = text_splitter.create_documents([page_content])

            for each_chunk in chunks:
                each_chunk.metadata = {
                    'filename': fns[index],
                    'link': sls[index]
                }
                final_chunks.append(each_chunk)

    return final_chunks


def save_to_chroma(chunks, data_type):
    if not os.path.exists(CHROMA_PATH):
        os.makedirs(CHROMA_PATH)
    db = Chroma.from_documents(chunks, openai_embds, persist_directory=CHROMA_PATH)

    if data_type == 'links':
        db.persist()

    print(f"Saved {len(chunks)} chunks to {CHROMA_PATH} for {data_type}.")

def save_links_to_chroma():
    with open(LINKS_JSON_PATH, 'r', encoding='utf-8') as file:
        links_data = json.load(file)

    documents = []
    for link_item in links_data:
        doc = Document(
            page_content=link_item['title'] + '\n' + link_item['description'] + '\n' + 'Moodle-Kurs-Link:' + link_item['link'],
            metadata={
                "title": link_item['title'],
                "link": link_item['link'],
                "description": link_item['description']
            }
        )
        documents.append(doc)

    chunks = split_text_v1(documents)
    save_to_chroma(chunks, 'links')

if __name__ == "__main__":
    main()




