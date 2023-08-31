**_Sam Wintermute 2008-09-10:_ Add numeric equality operator**

Soar has numeric tests for >,<,<=,>=, but not plain equality. This is apparently because that should be handled by just matching values, but that does not work when one number is internally an integer and the other is internally a float. So, Soar can detect that 1 <= 1.0 and 1 >= 1.0, but 1 != 1.0 as detected by matching.

There should be a operator for equality across ints and floats, or the matcher should do implicit conversions, since these types are hidden from the user, and for symmetry with the rest of the numeric tests. If this isn't done, the manual should be updated to note this when the comparison operators are discussed.

_Mazin_:  My guess is that this was not added because it would introduce a computational cost to all equality tests that the rete makes, a very small portion of which would be numeric tests.  Right now, it just compares pointers to symbols.  The other relational tests all do conditional stuff based on the type of the symbols.   It may be less elegant, but another option would be to add a special equality and inequality tests that agents can use when they know they have to compare floats and ints.

***

**_Bob Marinier 2008-02-28:_ add #define/ifdef/ifndef/endif -like functionality**

Sometimes I find myself with a large group of productions that I want to easily enable or disable. I could add a flag to the top state and change every production to test this flag, but this is a pain (and error prone, if I mistype something). A much easier solution would be to incorporate #define-like syntax in Soar, so entire blocks of code can be included or excluded easily.

Syntax: Since # already has a meaning, we should probably use something else, e.g., just the words define, ifdef, ifndef, and endif. (Note that I am not arguing for a fully functional macro language like C/C++; I just want to be able to easily flag which blocks of code to use). Here's a possible example:

define DEBUG

ifdef DEBUG sp {monitor*.... ... endif

Implementation: There are at least two ways I can see implementing this: in the kernel, as a new syntax, or as commands (in which case they would be part of commandline interface). I favor the command approach for simplicity (changing Soar's parser is probably hard). Basically, the define command will keep a list of constants that have been defined, and the ifdef/ifndef commands will set CLI switches (if the test fails, ignore all commands until endif is reached; otherwise execute commands as usual). I suppose the switch could be set in the parser directly, but telling CLI to ignore commands is probably simpler.

Also, these do not have to all be separate commands. There can be just one command, e.g. define, with arguments to do all this, and the rest can just be aliases.

One source of confusion for C/C++ programmers may be the fact that, in Soar,

define FOO actually does NOT define FOO, since the line is commented out.

But I think they'll get used to it (the alternative is to add special-case processing to code to recognize the difference between a comment and a define, and that sounds like a buggy situation).

There are some issues like, will we support nesting, or logical tests of flags? I say we start simple, and see what people really want as far as more complex features go.

Incidentally, this approach also gives Soar the ability to block-comment code, e.g.:

ifdef COMMENT #COMMENT is not define'd anywhere ... endif

...which is something I've wanted for a long time.

_Dave Ray on March 03, 2008 12:37:49:_

I think this is a good idea... just a few requests from the Tcl world:

Please don't add special purpose code to distinguish comments and #define. Avoid built-in Tcl function names. "define", "ifdef", "ifndef", "endif" are fine. Also, you probably also want an "undef" command. You might also want to say that the if and endif have to be in the same file. Otherwise, things could get pretty confusing when this stuff is mixed with source commands.

***
**_Mazin Sep 29, 2016_:  Ability to put tcl library in a different directory**

Soar is now more aggressive about finding the tcl library, but something about how the libraries are linked prevents them from finding each other unless they're in the same directory or they put their directory in their system path or LD_LIBRARY_PATH variables, which we don't want to deal with. Someone with more knowledge about shared library linking might be able to figure out a simple fix or a better design that would be more flexible.

***
**_Mazin Sep 29, 2016_:  Ability to turn tcl library on in the same file that Tcl is used**
```
tcl on
puts "hello world"
```
does not work with the current tcl plug-in.

The problem is that an event needs to fire to load the Tcl interpreter, which is on hold while the agent is sourcing the file that told the agent to turn tcl on. So, we need to either change that requirement or do something to allow us to interrupt and resume sourcing. (I forget the exact reason we needed an event, but there was one.)

Right now the easy workaround is to turn tcl on in the settings.soar file that is automatically sourced whenever an agent is created before any other files.