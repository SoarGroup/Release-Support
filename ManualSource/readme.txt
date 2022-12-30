Instructions on compiling the Soar Manual:

Prerequisites:
- pdflatex (install a larger package like texlive to get all the required packages)
- pandoc

- 'make pull': Downloads CLI help, convert stuff and make the final pdf.
- 'make clean': Deletes all intermediate files

Note that the script will copy the compiled manual into the Release-Support/pdf directory.
