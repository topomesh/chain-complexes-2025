ll: chain-complexes.pdf

%.tikz: %.sk
	sketch $< -o $@

FIGURES2D := $(wildcard figures/*.tikz)
FIGURES3D := $(patsubst %.sk,%.tikz,$(wildcard figures/*.sk))

figures/cone.pdf: figures/cone.py
	cd figures && python cone.py

%.pdf: %.tex %.bib $(FIGURES3D) $(FIGURES2D) figures/cone.pdf
	pdflatex -shell-escape $<
	bibtex $*
	pdflatex -shell-escape $<
	pdflatex -shell-escape $<
