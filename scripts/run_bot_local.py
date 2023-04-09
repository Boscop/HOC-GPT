#!/usr/bin/env python3

import os, sys
openai_api_key = os.environ["OPENAI_API_KEY"]
prepared_dir = "docs/prepared"

# model = "gpt-4"
model = "gpt-3.5-turbo"

# import argparse
# parser = argparse.ArgumentParser()
# parser.add_argument("prompt", nargs = "?", type = argparse.FileType("r"), default = sys.stdin)
# args = parser.parse_args()
# chatbot_prompt = args.prompt.read()

chatbot_prompt = sys.argv[1]
print("Prompt:\n" + chatbot_prompt)

from langchain.embeddings.openai import OpenAIEmbeddings
embeddings = OpenAIEmbeddings(openai_api_key = openai_api_key)

from langchain.vectorstores import FAISS
docsearch = FAISS.load_local("faiss_index", embeddings)

from langchain import OpenAI, VectorDBQA
# llm = OpenAI(model_name = model, temperature = 0.1, max_tokens = 256)
llm = OpenAI(model_name = model, temperature = 0.7)
qa = VectorDBQA.from_chain_type(llm = llm, chain_type = "stuff", vectorstore = docsearch, return_source_documents = True)

initial_prompt = "HOC is a startup building tech towards the massively parallel future of computation with a new VM called HVM based on interaction nets, an inherently concurrent computational model. For this conversation, you are a computer scientist working at HOC, helping to onboard a new developer who will be writing a LLVM backend for HVM. Consider the input as a question on explaining technical details about HVM and how different parts of its code relate to interaction net reductions, or how different parts of HVM's interpreter code can be translated to a codegen backend that uses LLVM."

result = qa({ "query": chatbot_prompt, "prompt": initial_prompt })
print(result["result"])

# from langchain.chat_models import ChatOpenAI
# from langchain.chains import RetrievalQA
# llm = ChatOpenAI(model_name = model)
# qa = RetrievalQA.from_chain_type(llm = llm, chain_type = "stuff", retriever = docsearch.as_retriever())
