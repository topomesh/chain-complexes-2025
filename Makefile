ll: chain-complexes.pdf

%.tikz: %.sk
	sketch $< -o $@

FIGURES2D := $(wildcard figures/*.tikz)
FIGURES3D := $(patsubst %.sk,%.tikz,$(wildcard figures/*.sk))

figures/cone.pdf: figures/cone.py
	cd figures && python cone.py

figures/retria.pdf: figures/retria.py
	cd figures && python retria.py

%.pdf: %.tex %.bib $(FIGURES3D) $(FIGURES2D) figures/cone.pdf figures/retria.pdf
	pdflatex -shell-escape $<
	bibtex $*
	pdflatex -shell-escape $<
	pdflatex -shell-escape $<
