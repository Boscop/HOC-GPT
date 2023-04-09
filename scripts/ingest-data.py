#!/usr/bin/env python3

import os
openai_api_key = os.environ["OPENAI_API_KEY"]
prepared_dir = "docs/prepared"

# Merge all docs into this single list
documents = []

def process_doc(doc):
#   print("Loading: " + doc.metadata["source"])
  documents.append(doc)

def process_docs(docs):
  for doc in docs:
    process_doc(doc)

print("Loading docs from dir: " + prepared_dir)

from langchain.document_loaders import DirectoryLoader
from langchain.document_loaders import TextLoader
# process_docs(DirectoryLoader(prepared_dir, glob = "**/*.*", loader_cls = TextLoader, loader_kwargs = { "encoding": "utf-8" }, silent_errors = True).load())
process_docs(DirectoryLoader(prepared_dir, glob = "**/*.txt", loader_cls = TextLoader, loader_kwargs = { "encoding": "utf-8" }).load())

# Split the documents into text chunks
from langchain.text_splitter import RecursiveCharacterTextSplitter
texts = RecursiveCharacterTextSplitter(chunk_size = 1000, chunk_overlap = 200).split_documents(documents)

from langchain.embeddings.openai import OpenAIEmbeddings
embeddings = OpenAIEmbeddings(openai_api_key = openai_api_key)

from langchain.vectorstores import FAISS
docsearch = FAISS.from_documents(texts, embeddings)
docsearch.save_local("faiss_index")

# # When loading embeddings from pinecone, use this instead:
# import pinecone
# from langchain.vectorstores.pinecone import Pinecone
# docsearch = Pinecone.from_documents(texts, embeddings, pinecone_client = pinecone)

# # When loading embeddings from chroma, use this instead:
# from langchain.vectorstores import Chroma
# docsearch = Chroma.from_documents(texts, embeddings)
