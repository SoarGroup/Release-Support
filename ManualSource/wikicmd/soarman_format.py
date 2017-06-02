# -*- coding: utf-8 -*-
"""
Created on Tue May 30 14:27:18 2017

@author: bryan stearns
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

def get_edit_list(pathname):
    PAGE_CM_WIDTH = 16          # How many cm to allocate for a table
    NORMAL_WIDTH = 76           # How many characters wide is allowed for normal verbatim text size
    SMALL_WIDTH = 81            # " for small verbatim text
    FOOTNOTE_WIDTH = 89         # " for footnotesize verbatim text
    SCRIPT_WIDTH = 110          # " for scriptsize verbatim text
    
    BAD_LABELS = ['\\label{synopsis','\\label{options','\\label{description','\\label{summary-screen',
                  '\\label{parameters','\\label{examples','\\label{example','\\label{default-aliases','\\label{see-also',
                  '\\label{performance-parameters','\\label{watch}','\\label{warnings}','\\label{timers}','\\label{usage}','\\label{statistics}']
    
    index = -1                  # Variable for keeping string.find results
    lnum = 0                    # Current line number
    edit_lstart = 0             # Which line does the edit start on?
    
    col_count = 2               # If editing a table, how many columns in it?
    oldcols = []                # If editing a table, what old proportions?
    old_col_strs = ['@{}ll@{}', '@{}lll@{}', '@{}llll@{}']
    new_col_strs = ['@{}p{5cm}p{11cm}@{}', '@{}p{4.5cm}p{4cm}p{7cm}@{}', 'p{4.7cm}p{4.5cm}p{4cm}p{2cm}@{}']
    
    max_lwidth = -1             # If editing a verbatim, how wide is the section?
    
    mode = 'none'               # What is being edited right now?
    
    edit_list = defaultdict(list)   # The returned map of start_line:[(end_line, old, new)] tuple lists
    
    with open(pathname, "r") as f:
        # Scan for important tokens
        for line in f: 
            lnum += 1
            
            if mode == 'none':
                ### ONE-LINE FIXES:
                # Paragraph ':'s (Move these outside the paragraph title)
                #   Colons outside headers are a hack for ensuring that headers appear before subsequent tables.
                index = line.find(":}\\label{")
                if index != -1:
                    edit_list[lnum].append( (lnum, line[index:-1], '}:') ) #line[index+1:-1]+':') )
                else:
                    # Remove useless reused labels (separate to cheaply avoid conflict with colon removal)
                    index = str_find_list(line, BAD_LABELS)
                    if index != -1:
                        index2 = line.find('}',index)
                        edit_list[lnum].append( (lnum, line[index:index2+1], '') )
                
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
            
            elif mode == 'table':
                # Search for the previously generated column widths - keep those proportions
                if col_count > 0:
                    index = line.find("{0.")
                    index2 = line.find("\\col", index+2)   # find the end of the number
                    if index != -1 and index2 != -1:
                        try:
                            oldcols.append(float(line[index+1:index2]))
                        except ValueError:
                            print '  ERROR with float conversion: ****\n  {}:\n   {}:\n    {}, {}'.format(pathname, line, index, index2)
                        col_count -= 1
                
                # Look for the end of the table
                index = line.find("\\bottomrule")
                if index != -1:
                    # Check which kind of table - non-minipage tables don't have automatic width info
                    if col_count > 0:
                        # No minipages were found - use fixed proportions
                        edit_list[edit_lstart].append( (edit_lstart, old_col_strs[col_count-2], new_col_strs[col_count-2]) )
                    else:
                        # Calculate and make changes using given proportions
                        newcols = normalize(oldcols)
                        scaled_width = PAGE_CM_WIDTH - 0.3 * (len(oldcols)-1)
                        newcms = [scaled_width * x for x in newcols]
                        newcm_str = '@{\\extracolsep{\\fill}}' + ''.join(['p{'+'{0:.4f}'.format(x)+'cm}' for x in newcms]) + '@{}'
                        
                        edit_list[edit_lstart].append( (edit_lstart, old_col_strs[len(oldcols)-2], newcm_str) )
                        item_shift = 0.013 + 0.0078*(len(oldcols))
                        for i, p in enumerate(newcols):
                            edit_list[edit_lstart].append( (lnum, str(oldcols[i]), '{0:.4f}'.format(p-item_shift)) )
                    # Reset
                    mode = 'none'
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
            line = line.replace(edit[1], edit[2], 1)
            
        # Remove completed edits
        active_edits = set(filter(lambda x:x[0] > lnum, active_edits))
        
        print line,
    return

def apply_soar_formatting(pathname):
    edit_list = get_edit_list(pathname)
    apply_edits(pathname, edit_list)
    
    

if __name__ == '__main__':
    #print '\n**** FORMATTING: {} ****\n'.format(sys.argv[1])
    apply_soar_formatting(sys.argv[1]) #'./tex/production_test.tex')
    #apply_soar_formatting('./tex/explain.tex')
    