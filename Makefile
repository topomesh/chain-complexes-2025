all: chain-complexes.pdf

%.tikz: %.sk
	sketch $< -o $@

FIGURES2D := $(wildcard figures/*.tikz)
FIGURES3D := $(patsubst %.sk,%.tikz,$(wildcard figures/*.sk))
FIGURESPY := $(patsubst %.py,%.pdf,$(wildcard figures/*.py))

figures/%.pdf: figures/%.py
	cd figures && python $*.py

chain-complexes.pdf: chain-complexes.tex chain-complexes.bib $(FIGURES3D) $(FIGURES2D) $(FIGURESPY)
	pdflatex -shell-escape $<
	bibtex chain-complexes
	pdflatex -shell-escape $<
	pdflatex -shell-escape $<
