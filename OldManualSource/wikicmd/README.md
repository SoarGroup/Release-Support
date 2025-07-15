# Wiki Command LaTeX Generator

The `gen_tex.sh` script will download the CLI documentation pages on the GitHub wiki and translate them into LaTeX files, one for each command. The output will be located in the tex/ subdirectory. This output is then passed through soarman_format.py for additional LaTeX-specific formatting and margin-handling. These resulting files are referenced and automatically included in `interface.tex`.
