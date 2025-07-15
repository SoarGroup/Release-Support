This is the OLD LaTeX source for the Soar Manual. We use the SoarGroup.github.io repository
to build the manual now, so this source is no longer maintained. It's only here for reference
in case there's something we need to migrate to the new source, as well as for historical purposes.

Instructions on compiling the Soar Manual:

Prerequisites:
- pdflatex (install a larger package like texlive to get all the required packages)
- pandoc

- 'make pull': Downloads CLI help, convert stuff and make the final pdf.
- 'make clean': Deletes all intermediate files

Note that the script will copy the compiled manual into the Release-Support/pdf directory.
