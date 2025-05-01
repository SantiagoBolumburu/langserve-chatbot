import bs4
from .text_files import load_text_file
from langchain import hub
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from typing_extensions import List, TypedDict


def get_all_document_splits(data_file_path):
    file_path = data_file_path
    file_content = load_text_file(file_path)

    document_promtior_linkedin_about = Document(
        page_content=file_content,
        metadata={"source": file_path}
    )

    loader = WebBaseLoader(
        web_paths=("https://www.promtior.ai/",
                    "https://www.promtior.ai/service",),
        bs_kwargs=dict(
            parse_only=bs4.SoupStrainer(
                class_=("wixui-rich-text__text")
            )
        ),
    )
    docs = loader.load()
    docs.append(document_promtior_linkedin_about)

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    all_splits = text_splitter.split_documents(docs)

    return all_splits

