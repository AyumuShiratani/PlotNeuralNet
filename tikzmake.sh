#!/bin/bash


python $1.py 
pdflatex $1.tex
pdf2svg $1.pdf $1.svg

rm *.aux *.log *.vscodeLog
rm *.tex

# if [[ "$OSTYPE" == "darwin"* ]]; then
#     open $1.pdf
# else
#     xdg-open $1.pdf
# fi
