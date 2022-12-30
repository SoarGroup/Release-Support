# Makefile to generate the Soar manual
#
# use 'make pull' if you want to first pull the latest CLI help entry from the wiki
# use 'make' to just do the manual recompilation
#

LATEX = pdflatex -halt-on-error # need to use pdf latex to insert some of the pdf figures correctly

SRC = architecture.tex chunking.tex functions.tex interface.tex intro.tex manual.tex syntax.tex funclist.tex rl.tex smem.tex epmem.tex svs.tex

.PHONY : trans_wiki

all : manual.pdf
pull : trans_wiki manual.pdf

trans_wiki ::
	cd wikicmd && bash gen_tex.sh

manual.pdf : manual.ind $(SRC)
	$(LATEX) manual
	$(LATEX) manual # has to be compiled twice to get references right
	cp manual.pdf ../pdf/SoarManual.pdf

manual.ind : $(SRC)
	$(LATEX) manual
	makeindex manual
	awk -f fix_index.awk manual.ind > tmp.ind
	mv tmp.ind manual.ind

funclist.tex : wikicmd/tex
	sh genfunclist.sh

clean :
	rm -f manual.lof manual.log manual.toc manual.out manual.pdf manual.ind manual.ilg manual.glo manual.idx *.aux
	rm -f funclist.tex
	rm -rf wikicmd/wiki wikicmd/tex

