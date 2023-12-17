all: chain-complexes.pdf

%.tikz: %.sk
	sketch $< -o $@

%.pdf: %.tex %.bib figures/tetrahedra.tikz
	pdflatex -shell-escape $<
	bibtex $*
	pdflatex -shell-escape $<
	pdflatex -shell-escape $<
