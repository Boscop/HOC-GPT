#!/bin/bash

# Downloads data from the web

set -Eeuxo pipefail

DST_DIR=./docs/input-data/scrape

rm -rf $DST_DIR
mkdir -p $DST_DIR
cd $DST_DIR

wget -O "Interaction Nets, Combinators, and Calculus _ @Zicklag's Blog.html" https://zicklag.github.io/blog/interaction-nets-combinators-calculus/
wget -O "IC.kind2" https://raw.githubusercontent.com/HigherOrderCO/Wikind/master/IC/_.kind2

git clone git@github.com:HigherOrderCO/HVM.git
cd HVM
rm -rf .git .github .vscode bench .gitignore *.lock *.toml LICENSE NIX.md *.nix
cd ..

wget --mirror -A html -I /15.0.0/docs --no-parent --compression=auto https://releases.llvm.org/15.0.0/docs/index.html
wget --mirror -A html -I /inkwell/inkwell --no-parent --compression=auto https://thedan64.github.io/inkwell/inkwell/index.html
wget --mirror -A html -I /llvm-sys/latest/llvm_sys --no-parent --compression=auto https://docs.rs/llvm-sys/latest/llvm_sys/

# Remove unnecessary files
rm -rf releases.llvm.org/15.0.0/docs/{AMDGPU*,PDB,Proposals}

# Download llvm-dev mailing list archives
# wget -r -l1 -nd -P llvm-dev -A "*.txt.gz" https://lists.llvm.org/pipermail/llvm-dev/ && gunzip llvm-dev/*.txt.gz
# Only download threads from 2018 onwards because the LLVM API changed a lot over the years
wget -nc -r -l1 -nd -P llvm-dev -A "201[8-9]-*.txt.gz" -A "202[0-9]-*.txt.gz" https://lists.llvm.org/pipermail/llvm-dev/ && gunzip llvm-dev/*.txt.gz

cd ..

# List all extensions of files in directory
echo `find . -type f -printf '%f\n' | awk -F'.' '{print $NF}' | sort -u`
