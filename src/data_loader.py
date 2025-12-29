from pathlib import Path
import pandas as pd
from typing import List, Any
from langchain_community.document_loaders import PyPDFLoader, TextLoader,JSONLoader
from langchain_core.documents import Document
import tempfile
import logging
logging.basicConfig(level=logging.INFO)


#read all files pdf, txt ,excel etc directory
def load_all_documents(data_dir:str) -> List[Any]:

    all_doc = []
    data_path = Path(data_dir).resolve()

    print(f'[DEBUG] Data path: {data_path}')
    
    #pdf files
    pdf_files = list(data_path.glob('**/*.pdf'))
    print(f'found {len(pdf_files)} PDF files :{[str(pdf_file) for pdf_file in pdf_files]}')
    for pdf_file in pdf_files:
        print(f"proccessing {pdf_file.name}")
        try:
            loader = PyPDFLoader(str(pdf_file))
            loaded = loader.load()
            print(f'loaded {len(loaded)} PDF docs from {pdf_file}')
            all_doc.extend(loaded)
        except Exception as e:
            print(f'faild to load {pdf_file} withrror: {e}')
    
    #textfiles
    text_files = list(data_path.glob('**/*.txt'))
    print(f'found {len(text_files)} text files :{[str(text_file) for text_file in text_files]}')
    for text_file in text_files:
        print(f"proccessing {text_file.name}")
        try:
            loader = TextLoader(str(text_file))
            loaded = loader.load()
            print(f'loaded {len(loaded)} text docs from {text_file}')
            all_doc.extend(loaded)
        except Exception as e:
            print(f'faild to load {text_file} withrror: {e}')

    #excelfiles
    excel_files = list(data_path.glob('**/*.xlsx'))
    print(f'found {len(excel_files)} excel files :{[str(excel_file) for excel_file in excel_files]}')
    for excel_file in excel_files:
        print(f"proccessing {excel_file.name}")
        try:
            df = pd.read_excel(excel_file)
            docs = [
                Document(
                    page_content=row.to_json(),
                    metadata={"source": str(excel_file)}
                )
                for _, row in df.iterrows()
            ]
            print(f'loaded {len(docs)} excel rows from {excel_file}')
            all_doc.extend(docs)
        except Exception as e:
            print(f'faild to load {excel_file} withrror: {e}')

    #JSONfiles
    json_files = list(data_path.glob('**/*.json'))
    print(f'found {len(json_files)} json files :{[str(json_file) for json_file in json_files]}')
    for json_file in json_files:
        print(f"proccessing {json_file.name}")
        try:
            loader = JSONLoader(str(json_file),jq_schema=".[ ]".replace(" ", ""),text_content=False)
            loaded = loader.load()
            print(f'loaded {len(loaded)} json docs from {json_file}')
            all_doc.extend(loaded)
        except Exception as e:
            print(f'faild to load {json_file} withrror: {e}')

    return all_doc

def load_pdf(pdf_file):
    try:
        all_doc = []
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            pdf_file.save(tmp.name)
            loader = PyPDFLoader(tmp.name)
            loaded = loader.load()
            all_doc.extend(loaded)
        return all_doc
    except Exception as e:
        logging.info(f'faild to load {pdf_file} withrror: {e}')
        return []


# def process_all_documents(data_dir:str) -> List[Any]:
#     documents = load_all_documents(data_dir)
#     all_docs = []
#     if len(all_docs) > 0:
#         for doc in documents:
#             doc.metadata['source_file'] = doc.name
#             doc.metadata['file_type'] = 
#             all_docs.extend(documents)
#             print(f'loaded {len(documents)} pages')  



# all_pdf_docs = process_all_pdfs("../data")
# all_pdf_docs