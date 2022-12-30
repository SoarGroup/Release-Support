# -*- coding: utf-8 -*-
"""
Created on Tue May 30 14:27:18 2017
@author: bryan stearns

This script takes a .tex file already converted from wiki markdown format to LaTeX format (see gen_tex.sh)
and applies additional formatting specifically for the Soar manual.

This script employs hardcoded knowledge of the CLI commands. If these change, this script should be updated.
(Only INDEX_HEADS and maybe BAD_LABELS should need updating)

Specifically, this script makes the following edits:
    1: Change any "\paragraph{blah:}" into "\paragraph{blah}:"
        # Having colons inside the section or paragraph name prints well in GitHub markdown.
        # But having them outside is a hack in LaTeX to ensure the paragraph title actually appears before ensuing tables.
    2: Remove excessive subsection/paragraph labels, which generate LaTeX warnings.
        # Ex: Any section with a "Description" subsection will get a generated \label{description}.
        # It is nonsensical for a document to have a single label point to more than one piece of text.
    3: Add indexes for CLI commands
        # By default there are no "\index"s generated. So this script inserts indexes for each "\label" it finds that
        # begins with a soar command name. Sub commands are recognized as sub indexes (e.g., "soar init" is indexed as "{soar!init}")
        # As Soar commands change, this script will need to be updated, since the Soar commands are hardcoded. (See 'INDEX_HEADS' below)
    4: Replace special unsupported characters with the corresponding LaTeX commands
        # For example, the unicode character λ is converted to $\lambda$.
    5: Resize table columns for intelligent use of page space
        # The pandoc converter by default does not specify column size, and creates very skinny minipage cells for \longtables.
        # The old method was to replace all table specs with globally fixed column widths, resulting in over/underflow.
        # This script still uses this approach when no widths are otherwise provided in a table (see new_col_strs),
        # to avoid tables that are too wide for a page.
        # However, this script now rescales default minipage table cell widths to fit a page using local text proportions.
    6: Resize verbatim blocks
        # Code formatted text in the source wiki markdown is pandoc-converted into verbatim blocks.
        # Sometimes these blocks are too wide to fit within a page.
        # This script determines how too-wide they are, and surrounds them with text-scaling code accordingly.
"""

import sys
from collections import defaultdict
import fileinput

# Returns the index of the first occurrence of the first list item found in the string
def str_find_list(s, l):
    for item in l:
       ind = s.find(item)
       if ind != -1:
           return ind
    return -1

def normalize(vals, span=1.0):
    ratio = span / sum(vals)
    newvals = [v*ratio for v in vals]
    return newvals

## Takes a .tex file and returns a list of edits for the apply_edits function.
def get_edit_list(pathname):
    #PAGE_CM_WIDTH = 16          # How many cm to allocate for a table
    NORMAL_WIDTH = 76           # How many characters wide is allowed for normal verbatim text size
    SMALL_WIDTH = 81            # " for small verbatim text
    FOOTNOTE_WIDTH = 89         # " for footnotesize verbatim text
    SCRIPT_WIDTH = 110          # " for scriptsize verbatim text

    # These are the (prefixes of) labels to remove from text if encountered (they are used more than once across various sections).
    BAD_LABELS = ['\\label{synopsis','\\label{options','\\label{description','\\label{summary-screen',
                  '\\label{parameters','\\label{examples','\\label{example','\\label{default-aliases','\\label{see-also',
                  '\\label{performance-parameters','\\label{watch}','\\label{warnings}','\\label{timers}','\\label{usage}','\\label{statistics}']

    # These are the prefixes of section labels to recognize for creating index markers.
    INDEX_HEADS = ['soar', 'gp', 'help', 'run', 'sp', 'preferences', 'production', 'print', 'wm', 'echo', 'output','stats', 'trace',
                   'visualize', 'chunk', 'explain', 'decide', 'epmem', 'rl', 'smem', 'svs', 'load', 'save', 'alias', 'debug']

    # These are special characters that latex doesn't support by defult (unless we upgrade to unicode?) and need replacement.
    # NOTE: The λ replacement assumes that the replaced text is not already in a math environment.
    #       This shouldn't ever be an issue, since the source GitHub markdown format doesn't support math environments anyway,
    #       and thus won't have any in the converted .tex files, but it should be noted in markdown ever changes that.
    CHAR_REPLACEMENTS = {'λ':'$\lambda$'}

    # The old pandoc-generated table specs. More 'l's denote more columns
    OLD_COL_STRS = ['@{}ll@{}', '@{}lll@{}', '@{}llll@{}']
    # If no column proportions are given, use preset dimensions:
    NEW_COL_STRS = ['@{}p{5cm}p{11cm}@{}', '@{}p{4.75cm}p{3.75cm}p{7cm}@{}', 'p{4.5cm}p{4.7cm}p{4cm}p{2cm}@{}']

    index = -1                  # Variable for keeping string.find results
    lnum = 0                    # Current line number
    edit_lstart = 0             # Which line does the edit start on?

    col_count = 2               # If editing a table, how many columns in it?
    oldcols = []                # If editing a table, what old proportions?

    max_lwidth = -1             # If editing a verbatim, how wide is the section?

    mode = 'none'               # What is being edited right now?

    edit_list = defaultdict(list)   # The returned map of start_line:[(end_line, old, new)] tuple lists

    with open(pathname, "r") as f:
        # Scan for important tokens
        for line in f:
            lnum += 1

            # Ready for anything:
            if mode == 'none':
                ### ONE-LINE FIXES:

                # Paragraph ':'s (Move these outside the paragraph title)
                #   Colons outside headers are a hack for ensuring that headers appear before subsequent tables.
                index = line.find(":}\\label{")
                if index != -1:
                    edit_list[lnum].append( (lnum, line[index:index+2], '}:') ) #line[index+1:-1]+':') )

                # Remove useless reused labels (separate to cheaply avoid conflict with colon removal)
                index = str_find_list(line, BAD_LABELS)
                if index != -1:
                    index2 = line.find('}',index)
                    edit_list[lnum].append( (lnum, line[index:index2+1], '') )

                # Labels: Make index markers for CLI commands
                index = line.find("\\label{")
                if index != -1:
                    endind = index + line[index:].find("}")
                    labstr = line[index+7:endind]
                    oldstr = line[index:endind+1]
                    newstr = labstr.replace("-", "!", 1)

                    endind = newstr.find("!")
                    if endind == -1:
                        endind = len(newstr)
                    newstr = newstr[:endind] + " (command)" + newstr[endind:]
                    if newstr[:endind] in INDEX_HEADS:
                        edit_list[lnum].append( (lnum, oldstr, oldstr+"\\index{" + newstr + "}") )

                # Single-character replacements
                for key, value in CHAR_REPLACEMENTS.items():
                    index = line.find(key)
                    if index != -1:
                        edit_list[lnum].append( (lnum, key, value) )

                ### SCANNING FIXES:

                # Search for tables
                index = line.find("@{}ll")
                if index != -1:
                    mode = 'table'
                    edit_lstart = lnum
                    col_count = 2
                    oldcols = []

                    # How many columns: "ll", "lll", or "llll"?
                    if line[index+5] == 'l':
                        col_count = 3
                        if line[index+6] == 'l':
                            col_count = 4

                # Search for verbatims (NOTE: this assumes there isn't already any size formatting for verbatim blocks)
                index = line.find("\\begin{verbatim}",0)
                if index != -1:
                    mode = 'verbatim'
                    edit_lstart = lnum
                    max_lwidth = -1

            # In table mode: find minipage widths from multiple lines, remembering the table-start line
            elif mode == 'table':
                # Search for the previously generated column widths - keep those proportions
                if col_count > 0:
                    index = line.find("{0.")
                    index2 = line.find("\\col", index+2)   # find the end of the number
                    if index != -1 and index2 != -1:
                        try:
                            oldcols.append(float(line[index+1:index2]))
                        except ValueError:
                            print(f'ERROR with float conversion: ****\n  {pathname}:\n   {line}:\n   "{line[index+1:index2]}"')
                        col_count -= 1

                # Look for the end of the table
                index = line.find("\\bottomrule")
                if index != -1:
                    # Check which kind of table - non-minipage tables don't have automatic width info

                    if col_count <= 0:
                        # Calculate and make changes using given proportions
                        newcols = normalize(oldcols)

                        ## Replace the table header definition of column widths
                        ## (removed - uncomment this to use fixed column sizes in addition to minipage sizes)
                        #scaled_width = PAGE_CM_WIDTH - 0.3 * (len(oldcols)-1)
                        #newcms = [scaled_width * x for x in newcols]
                        #newcm_str = '@{\\extracolsep{\\fill}}' + ''.join(['p{'+'{0:.4f}'.format(x)+'cm}' for x in newcms]) + '@{}'
                        #edit_list[edit_lstart].append( (edit_lstart, old_col_strs[len(oldcols)-2], newcm_str) )

                        # Replace the minipage cell widths
                        item_shift = 0.013 + 0.0078*(len(oldcols))
                        for i, p in enumerate(newcols):
                            edit_list[edit_lstart].append( (lnum, str(oldcols[i])+"\\", '{0:.4f}\\'.format(p-item_shift)) )
                    else:
                        # No minipages were found - use fixed proportions for the columns (so it doesn't overflow the page)
                        edit_list[edit_lstart].append( (edit_lstart, OLD_COL_STRS[col_count-2], NEW_COL_STRS[col_count-2]) )

                    # Reset
                    mode = 'none'
            # In verbatim mode: find the max text width of the block, remembering the start line
            elif mode == 'verbatim':
                # Search for the end
                index = line.find("\\end{verbatim}")
                if index != -1:
                    # Reset
                    mode = 'none'

                    # Calculate size needed
                    if max_lwidth <= NORMAL_WIDTH:
                        continue
                    elif max_lwidth <= SMALL_WIDTH:
                        size = 'small'
                    elif max_lwidth <= FOOTNOTE_WIDTH:
                        size = 'footnotesize'
                    elif max_lwidth <= SCRIPT_WIDTH:
                        size = 'scriptsize'
                    else:
                        size = 'tiny'

                    edit_list[edit_lstart].append( (edit_lstart, '\\begin{verbatim}', '{\\'+size+'\n\\begin{verbatim}'))
                    edit_list[lnum].append( (lnum, '\\end{verbatim}', '\\end{verbatim}\n}') )
                elif len(line) > max_lwidth:
                    max_lwidth = len(line)

    return edit_list

## Take a list of changes and do them.
##   edit_list = list of {start_line:(end_line, old_str, new_str)} maps
## All occurrences of old_str that fall between start_line and end_line (inclusive) are replaced with new_str.
def apply_edits(pathname, edit_list):

    lnum = 0
    active_edits = set()

    # Scan for lines to be edited
    for line in fileinput.input(pathname, inplace=True):
        lnum += 1

        # Check for new edits to use
        if lnum in edit_list:
            for tup in edit_list[lnum]:
                active_edits.add(tup)

        # Apply any current edits
        for edit in active_edits:
            line = line.replace(edit[1], edit[2])

        # Remove completed edits
        active_edits = set(filter(lambda x:x[0] > lnum, active_edits))

        print(line)
    return



def apply_soar_formatting(pathname):
    edit_list = get_edit_list(pathname) # Get the line-by-line changes to make
    apply_edits(pathname, edit_list)    # Make the changes for each line



if __name__ == '__main__':
    #print '\n**** FORMATTING: {} ****\n'.format(sys.argv[1])
    apply_soar_formatting(sys.argv[1])
