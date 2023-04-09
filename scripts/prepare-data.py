#!/usr/bin/env python3

# This script is used to prepare the data for the custom embeddings
# Adapted from https://xai.arya.ai/article/how-to-build-copilot-using-gpt4
# Processes files from ./docs/input-data into ./docs/prepared

import os

input_dir = "docs/input-data"
prepared_dir = "docs/prepared"

if not os.path.exists(prepared_dir):
  os.makedirs(prepared_dir)

# Merge all docs into this single list
documents = []

from pathvalidate import sanitize_filename
input_dir_prefix = sanitize_filename(input_dir)
def process_doc(doc):
  filename = sanitize_filename(doc.metadata["source"]).removeprefix(input_dir_prefix) + ".txt"
  print("Saving: " + filename)
  with open(os.path.join(prepared_dir, filename), "w", encoding = "utf-8") as f:
    f.write(doc.page_content)
  documents.append(doc)

def process_docs(docs):
  for doc in docs:
    process_doc(doc)

# # Load URLs
# urls = [
#   "https://zicklag.github.io/blog/interaction-nets-combinators-calculus/",
#   # "https://raw.githubusercontent.com/HigherOrderCO/Wikind/master/IC/_.kind2",
# ]
# from langchain.document_loaders import UnstructuredURLLoader
# process_docs(UnstructuredURLLoader(urls = urls).load())

# Load markdown files
# TODO: Maybe better results by loading them with TextLoader?
from langchain.document_loaders import DirectoryLoader
# from langchain.document_loaders import UnstructuredMarkdownLoader
# process_docs(DirectoryLoader(input_dir, glob = "**/*.md", loader_cls = UnstructuredMarkdownLoader, loader_kwargs = None).load()) # recursive = True

# Load text/source files
from langchain.document_loaders import TextLoader
# for ext in ["hs", "hvm", "js", "kind2", "rs", "txt"]:
for ext in ["hs", "hvm", "js", "kind2", "rs", "txt", "md"]:
  process_docs(DirectoryLoader(input_dir, glob = "**/*." + ext, loader_cls = TextLoader).load())

# Load PDFs
import glob
from langchain.document_loaders import PyPDFLoader
# from langchain.document_loaders import UnstructuredPDFLoader

# Get a list of all PDF files in the directory
for filepath in glob.glob(os.path.join(input_dir, "**/*.pdf")):
  if "Yves Lafont" not in filepath or "Yves Lafont - Interaction Combinators (1 column).pdf" in filepath:
    for (page, doc) in enumerate(PyPDFLoader(filepath).load_and_split()):
      doc.metadata["source"] += " (page {})".format(page)
      process_doc(doc)

print("Documents so far (without HTML files): ", len(documents))

from langchain.document_loaders.html_bs import BSHTMLLoader
process_docs(DirectoryLoader(input_dir, glob = "**/*.html", loader_cls = BSHTMLLoader, loader_kwargs = { "open_encoding": "utf-8" }).load()) # silent_errors = True

print("Documents: ", len(documents))
