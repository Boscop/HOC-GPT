#!/usr/bin/env python3

import os, sys
openai_api_key = os.environ["OPENAI_API_KEY"]

# model = "gpt-4"
model = "gpt-3.5-turbo"

prepared_dir = "docs/prepared"

# import argparse
# parser = argparse.ArgumentParser()
# parser.add_argument("prompt", nargs = "?", type = argparse.FileType("r"), default = sys.stdin)
# args = parser.parse_args()
# chatbot_prompt = args.prompt.read()

chatbot_prompt = sys.argv[1]
print("Prompt:\n" + chatbot_prompt)

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

# # When loading embeddings from pinecone, use this instead:
# import pinecone
# from langchain.vectorstores.pinecone import Pinecone
# docsearch = Pinecone.from_documents(texts, embeddings, pinecone_client = pinecone)

# # When loading embeddings from chroma, use this instead:
# from langchain.vectorstores import Chroma
# docsearch = Chroma.from_documents(texts, embeddings)

from langchain import OpenAI, VectorDBQA
# llm = OpenAI(temperature = 0.1, model_name = model, max_tokens = 256)
llm = OpenAI(model_name = model)
qa = VectorDBQA.from_chain_type(llm = llm, chain_type = "stuff", vectorstore = docsearch, return_source_documents = True)

initial_prompt = "HOC is a startup building tech towards the massively parallel future of computation with a new VM called HVM based on interaction nets, an inherently concurrent computational model. For this conversation, you are a computer scientist working at HOC, helping to onboard a new developer who will be writing a LLVM backend for HVM. Consider the input as a question on explaining technical details about HVM and how different parts of its code relate to interaction net reductions, or how different parts of HVM's interpreter code can be translated to a codegen backend that uses LLVM."

result = qa({ "query": chatbot_prompt, "prompt": initial_prompt })
print(result["result"])

# from langchain.chat_models import ChatOpenAI
# from langchain.chains import RetrievalQA
# llm = ChatOpenAI(model_name = model)
# qa = RetrievalQA.from_chain_type(llm = llm, chain_type = "stuff", retriever = docsearch.as_retriever())
