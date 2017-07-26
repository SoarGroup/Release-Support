Instructions on compiling the Soar Manual:

Prerequisites:
- Perl modules:
    - HTML::TreeBuilder
    - HTML::Latex
    - These are obtainable from CPAN (Comprehensive Perl Archive Network). If 
      you have the cpan command line program, you can just run:
      
      cpan -i HTML::TreeBuilder HTML::Latex
- pdflatex
- Other possible prerequisites:
    - pandoc
    - html2text

- 'make':  Will download CLI help, convert stuff and make the final pdf.
- 'make fast': Same as make but does not download and convert CLI help, which may not be actively changing
- 'make clean': Deletes all intermediate files

Note that the script will copy the compiled manual into the Release-Support/pdf directory.