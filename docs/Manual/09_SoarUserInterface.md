# The Soar User Interface

- [The Soar User Interface](#the-soar-user-interface)
      - [Notation](#notation)
  - [Basic Commands for Running Soar](#basic-commands-for-running-soar)
    - [exit](#exit)
      - [Default Aliases](#default-aliases)
  - [Procedural Memory Commands](#procedural-memory-commands)
  - [Short-term Memory Commands](#short-term-memory-commands)
  - [Learning](#learning)
  - [Long-term Declarative Memory](#long-term-declarative-memory)
  - [Other Debugging Commands](#other-debugging-commands)
  - [File System I/O Commands](#file-system-io-commands)


This chapter describes the set of user interface commands for Soar. All
commands and examples are presented as if they are being entered at the
Soar command prompt.

This chapter is organized into 7 sections:

1.  Basic Commands for Running Soar
1.  Examining Memory
1.  Configuring Trace Information and Debugging
1.  Configuring Soar’s Run-Time Parameters
1.  File System I/O Commands
1.  Soar I/O commands
1.  Miscellaneous Commands

Each section begins with a summary description of the commands covered
in that section, including the role of the command and its importance to
the user. Command syntax and usage are then described fully, in
alphabetical order.

The following pages were automatically generated from the git repository
at

on the date listed on the title page of this manual. Please consult the
repository directly for the most accurate and up-to-date information.

For a concise overview of the Soar interface functions, see the Function
Summary and Index on page . This index is intended to be a quick
reference into the commands described in this chapter.

## Notation

The notation used to denote the syntax for each user-interface command
follows some general conventions:

  - The command name itself is given in a font.
  - Optional command arguments are enclosed within square brackets, and
  - A vertical bar, , separates alternatives.
  - Curly braces, , are used to group arguments when at least one
    argument from the set is required.
  - The commandline prompt that is printed by Soar, is normally the
    agent name, followed by ’’. In the examples in this manual, we use
    “”.
  - Comments in the examples are preceded by a ’’, and in-line comments
    are preceded by ’’.

For many commands, there is some flexibility in the order in which the
arguments may be given. (See the online help for each command for more
information.) We have not incorporated this flexible ordering into the
syntax specified for each command because doing so complicates the
specification of the command. When the order of arguments will affect
the output produced by a command, the reader will be alerted.

Note that the command list was revamped and simplified in Soar 9.6.0.
While we encourage people to learn the new syntax, aliases and some
special mechanism have been added to maintain backwards compatibility
with old Soar commands. As a result, many of the sub-commands of the
newer commands may use different styles of arguments.

## Basic Commands for Running Soar

This section describes the commands used to start, run and stop a Soar
program; to invoke on-line help information; and to create and delete
Soar productions. It also describes how to configure some general
settings for Soar.

The specific commands described in this section are:

>   - soar  
>     \- Commands and settings related to running Soar. Use **soar ?**
>     for a summary of sub-commands listed below.
>     
>       - soar init  
>         \- Reinitialize Soar so a program can be rerun from scratch.
>     
>       - soar stop  
>         \- Interrupt a running Soar program.
>     
>       - soar max-chunks  
>         \- Limit the number of chunks created during a decision cycle.
>     
>       - soar max-dc-time  
>         \- Set a wall-clock time limit such that the agent will be
>         interrupted when a single decision cycle exceeds this limit.
>     
>       - soar max-elaborations  
>         \- Limit the maximum number of elaboration cycles in a given
>         phase.
>     
>       - soar max-goal-depth  
>         \- Limit the sub-state stack depth.
>     
>       - soar max-memory-usage  
>         \- Set the number of bytes that when exceeded by an agent,
>         will trigger the memory usage exceeded event.
>     
>       - soar max-nil-output-cycles  
>         \- Limit the maximum number of decision cycles executed
>         without producing output.
>     
>       - soar max-gp  
>         \- Set the upper-limit to the number of productions generated
>         by the gp command.
>     
>       - soar stop-phase  
>         \- Controls the phase where agents stop when running by
>         decision.
>     
>       - soar tcl  
>         \- Controls whether Soar Tcl mode is enabled.
>     
>       - soar timers  
>         \- Toggle on or off the internal timers used to profile Soar.
>     
>       - soar version  
>         \- Returns version number of Soar kernel.
>     
>       - soar waitsnc  
>         \- Generate a wait state rather than a state-no-change
>         impasse.
> 
>   - run  
>     \- Begin Soar’s execution cycle.
> 
>   - exit  
>     \- Shut down the Soar environment.
> 
>   - help  
>     \- Provide formatted, on-line information about Soar commands.
> 
>   - decide   
>     \- Commands and settings related to the selection of operators
>     during the Soar decision process
>     
>       - decide indifferent-selection  
>         \- Controls indifferent preference arbitration.
>     
>       - decide numeric-indifferent-mode  
>         \- Select method for combining numeric preferences.
>     
>       - decide predict  
>         \- Predict the next selected operator
>     
>       - decide select  
>         \- Force the next selected operator
>     
>       - decide set-random-seed  
>         \- Seed the random number generator.
> 
>   - alias  
>     \- Define a new alias, or command, using existing commands and
>     arguments.

These commands are all frequently used anytime Soar is run.

### exit

Terminates Soar and exits the kernel.

#### Default Aliases

`stop exit`

## Procedural Memory Commands

This section describes the commands used to create and delete Soar
productions, to see what productions will match and fire in the next
Propose or Apply phase, to watch when specific productions fire and
retract, and to configure options for selecting between mutually
indifferent operators, along with various other methods for examining
the contents and statistics of procedural memory.

The specific commands described in this section are:

>   - sp  
>     \- Create a production and add it to production memory.
> 
>   - gp  
>     \- Define a pattern used to generate and source a set of Soar
>     productions.
> 
>   - production  
>     \- Commands to manipulate Soar rules and analyze their usage
>     
>       - production break  
>         \- Set interrupt flag on specific productions.
>     
>       - production excise  
>         \- This command removes productions from Soar’s memory.
>     
>       - production find  
>         \- Find productions that contain a given pattern.
>     
>       - production firing-counts  
>         \- Print the number of times productions have fired.
>     
>       - production matches  
>         \- Print information about the match set and partial matches.
>     
>       - production memory-usage  
>         \- Print memory usage for production matches.
>     
>       - production optimize-attribute  
>         \- Declare an attribute as multi-attributes so as to increase
>         Rete production matching efficiency.
>     
>       - production watch  
>         \- Trace firings and retractions of specific productions.

is of course used in virtually all Soar programming. Of the remaining
commands, and are most often used. is especially useful when the number
of productions loaded is high. is used to see if how many times certain
rules fire. is related to , but applies only to specific, named
productions.

## Short-term Memory Commands

This section describes the commands for interacting with working memory
and preference memory, seeing what productions will match and fire in
the next Propose or Apply phase, and examining the goal dependency set.
These commands are particularly useful when running or debugging Soar,
as they let users see what Soar is “thinking.” Also included in this
section is information about using Soar’s Spatial Visual System (SVS),
which filters perceptual input into a form usable in symbolic working
memory.

The specific commands described in this section are:

>   - print  
>     \- Print items in working, semantic and production memory. Can
>     also print the print the WMEs in the goal dependency set for each
>     goal.
> 
>   - wm  
>     Commands and settings related to working memory and working memory
>     activation.
>     
>       - wm activation  
>         \- Get/Set working memory activation parameters.
>     
>       - wm add  
>         \- Manually add an element to working memory.
>     
>       - wm remove  
>         \- Manually remove an element from working memory.
>     
>       - wm watch  
>         \- Print information about wmes that match a certain pattern
>         as they are added and removed.
> 
>   - preferences  
>     \- Examine items in preference memory.
> 
>   - svs  
>     \- Perform spatial visual system commands.

Of these commands, **print** is the most often used (and the most
complex). **print –gds** is useful for examining the goal dependency set
when subgoals seem to be disappearing unexpectedly. **preferences** is
used to examine which candidate operators have been proposed.

## Learning

This section describes the commands for enabling and configuring Soar’s
mechanisms of chunking and reinforcement learning. The specific commands
described in this section are:

>   - chunk  
>     \- Set the parameters for explanation-based chunking, Soar’s
>     learning mechanism.
> 
>   - rl  
>     \- Get/Set RL parameters and statistics.

## Long-term Declarative Memory

This section describes the commands for enabling and configuring Soar’s
long-term semantic memory and episodic memory systems. The specific
commands described in this section are:

>   - smem  
>     \- Get/Set semantic memory parameters and statistics.
> 
>   - epmem  
>     \- Get/Set episodic memory parameters and statistics.

## Other Debugging Commands

This section describes the commands used primarily for debugging or to
configure the trace output printed by Soar as it runs. Many of these
commands provide options that simplify or restrict runtime behavior to
enable easier and more localized debugging. Users may specify the
content of the runtime trace output, examine the backtracing information
that supports generated justifications and chunks, or request details on
Soar’s performance.

The specific commands described in this section are:

>   - trace  
>     \- Control the information printed as Soar runs. *(was )*
> 
>   - output  
>     \- Controls sub-commands and settings related to Soar’s output.
>     
>       - output enabled  
>         \- Toggles printing at the lowest level.
>     
>       - output console  
>         \- Redirects printing to the the terminal. Most users will not
>         change this.
>     
>       - output callbacks  
>         \- Toggles standard Soar agent callback-based printing.
>     
>       - output log  
>         \- Record all user-interface input and output to a file.
>     
>       - output command-to-file  
>         \- Dump the printed output and results of a command to a file.
>     
>       - output print-depth  
>         \- Set how many generations of an identifier’s children that
>         Soar will print
>     
>       - output warnings  
>         \- Toggle whether or not warnings are printed.
>     
>       - output verbose  
>         \- Control detailed information printed as Soar runs.
>     
>       - output echo-commands  
>         \- Set whether or not commands are echoed to other connected
>         debuggers.
> 
>   - explain  
>     \- Provides interactive exploration of why a rule was learned.
> 
>   - visualize  
>     \- Creates graph visualizations of Soar’s memory systems or
>     processing.
> 
>   - stats  
>     \- Print information on Soar’s runtime statistics.
> 
>   - debug  
>     \- Contains commands that provide access to Soar’s internals. Most
>     users will not need to access these commands
>     
>       - debug allocate  
>         \- Allocate additional 32 kilobyte blocks of memory for a
>         specified memory pool without running Soar.
>     
>       - debug port  
>         \- Returns the port the kernel instance is listening on.
>     
>       - debug time  
>         \- Uses a default system clock timer to record the wall time
>         required while executing a command.
>     
>       - debug internal-symbols  
>         \- Print information about the Soar symbol table.

Of these commands, is the most often used (and the most complex).  
is related to the command. is useful for understanding how much work
Soar is doing.

## File System I/O Commands

This section describes commands which interact in one way or another
with operating system input and output, or file I/O. Users can
save/retrieve information to/from files, redirect the information
printed by Soar as it runs, and save and load the binary representation
of productions. The specific commands described in this section are:

>   - cd  
>     \- Change directory.
> 
>   - dirs  
>     \- List the directory stack.
> 
>   - load  
>     \- Loads soar files, rete networks, saved percept streams and
>     external libraries.
>     
>       - load file  
>         \- Sources a file containing soar commands and productions.
>         May also contain Tcl code if Tcl mode is enabled.
>     
>       - load library  
>         \- Loads an external library that extends functionality of
>         Soar.
>     
>       - load rete-network  
>         \- Loads a rete network that represents rules loaded in
>         production memory.
>     
>       - load library  
>         \- Loads soar files, rete networks, saved percept streams and
>         external libraries.
> 
>   - ls  
>     \- List the contents of the current working directory.
> 
>   - popd  
>     \- Pop the current working directory off the stack and change to
>     the next directory on the stack.
> 
>   - pushd  
>     \- Push a directory onto the directory stack, changing to it.
> 
>   - pwd  
>     \- Print the current working directory.
> 
>   - save  
>     \- Saves chunks, rete networks and percept streams.
>     
>       - save agent  
>         \- Saves the agent’s procedural and semantic memories and
>         settings to a single file.
>     
>       - save chunks  
>         \- Saves chunks into a file.
>     
>       - save percepts  
>         \- Saves future input link structures into a file.
>     
>       - save rete-network  
>         \- Saves the current rete networks that represents rules
>         loaded in production memory.
> 
>   - echo  
>     \- Prints a string to the current output device.

(See also the output command in Section [\[output\]](#output) on page .)

The command, previously known as , is used for nearly every Soar
program. The directory functions are important to understand so that
users can navigate directories/folders to load/save the files of
interest. Saving and loading percept streams are used mainly when Soar
needs to interact with an external environment. Soar applications that
include a graphical interface or other simulation environment will often
require the use of . Users might take advantage of these commands when
debugging agents, but care should be used in adding and removing WMEs
this way as they do not fall under Soar’s truth maintenance system.
