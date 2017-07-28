=========================
=    Soar 9.6.0 README  =
=      July  2017       =
=========================

Welcome to Soar!  Soar 9.6.0 is the current, stable version of Soar. It is the 
first major release in a few years and includes six key new features and 
hundreds of important bug fixes and code improvements:

- Explanation-Based Chunking: ​ The first official release of a new, far more
powerful rule learning algorithm that replaces chunking, Soar's original general
learning mechanism

- Instance-based model of semantic memory: Can be used in a greater variety of
ways and integrates with other aspects of Soar much more cleanly

- Streamlined user interface: Has far fewer top-level commands with improved
presentation and feedback

- Explanations: A new explain command provides interactive exploration of an
agent's rule learning experiences

- Visualizations: A new visualize command creates graphical representations of
Soar's memory systems and even some of its processing

- Spreading activation: The first beta release of a model of spreading activation
in semantic memory

The full release notes can be found in its own file.

====================
Official Soar Manual
====================

To facilitate continual updating and improvement of the Soar manual, it is no
longer distributed as part of the binary release.  The latest version can be
found at:

https://soar.eecs.umich.edu/downloads/SoarManual.pdf

=========
Launching
=========

- Navigate to the folder you extracted to
- Launch Soar
  - To launch Soar within a graphical user interface
    - Windows users, run SoarJavaDebugger.bat
    - Linux and Mac users, run SoarJavaDebugger.sh
  - To launch Soar using a command line interface,
    - Windows users, run Soar_CLI.bat
    - Linux and Mac users, run Soar_CLI.sh
    - You can also navigate to the /bin directory in a terminal and run the Soar executable directly

Launch options for the CLI and the java debugger are listed at the bottom of this document.

=============================
Soar-CLI Command Line Options
=============================
    -l            Listen on, i.e. launches Soar kernel in new thread
    -n            No syntax coloring (for people on light background or on 
                  Windows, which doesn't support our color codes.  Also turning 
                  off color does speed up printing.)
    -p <port>     Listens on port <port>
    -s <file>     Sources file <file> on load

To manage multiple agents, you can use the commands "create", "list", and 
"switch".  These are Soar-CLI commands, not native Soar commands.  They are 
not available in other interfaces, for example the Soar Java Debugger.

=======================================
Soar Java Debugger Command Line Options
=======================================
    -remote             Use a remote connection (with default ip/port)
    -ip xxx             Use this IP value (implies remote connection)
    -port ppp           Use this port (implies remote connection, without any 
                        remote options we start a local kernel)
    -agent <name>       On a remote connection select this agent as initial 
                        agent
    -agent <name>       On a local connection use this as the name of the 
                        initial agent
    -source <path>      Load this file of productions on launch (only valid 
                        for local kernel)
    -quitonfinish       When combined with source causes the debugger to exit 
                        after sourcing that one file
    -listen ppp         Use this port to listen for remote connections (only 
                        valid for a local kernel)
    -maximize           Start with maximized window
    -width <width>      Start with this window width
    -height <height>    Start with this window height
    -x <x> -y <y>       Start with this window position
    -cascade            Cascade each window that starts (offseting from the 
                        -x <x> -y <y> if given). This option now always on. 
                        Note that providing width/height/x/y => not a maximized 
                        window.

If you have problems with the debugger, try deleting any .soar* files in your 
home directory.  Corrupt settings can cause the java debugger to fail to launch.

===================================================
Transitioning To Soar 9.6.0's New Command Structure
===================================================

The following shows the new command structure for Soar 9.6.0 and how the 
commands from previous versions of Soar map to it. All of the new commands
and their sub-commands will guess the command based on partial input.

Note:  Soar 9.6.0 translates old commands in a way that it maintains 99.9% 
       backwards compatibility with 9.5.1, so this transition should not be 
       painful.

------------------                  ---------------------
Soar 9.5.0 Command                  Soar 9.6.0 Equivalent
------------------                  ---------------------
add-wme                             wm add
alias
allocate                            debug allocate
capture-input                       save percepts
cd
chunk-name-format                   chunk naming-style
cli                                 soar tcl
clog                                output log
command-to-file                     output command-to-file
default-wme-depth                   output print-depth
dirs
echo
echo-commands                       output echo-commands
edit-production                     (DEPRECATED)
epmem
excise                              production excise
explain-backtraces                  (DEPRECATED)
firing-counts                       production firing-counts
gds-print                           print --gds
gp
gp-max                              soar gp-max
help
indifferent-selection               decide indifferent-selection
init-soar                           soar init
internal-symbols                    debug internal-symbols
learn                               chunk
load-library                        load library
ls
matches                             production matches
max-chunks                          chunk max-chunks
max-dc-time                         soar max-dc-time
max-elaborations                    soar max-elaborations
max-goal-depth                      soar max-goal-depth
max-memory-usage                    soar max-memory-usage
max-nil-output-cycles               soar max-nil-output-cycles
memories                            production memory-usage
multi-attributes                    production optimize-attribute
numeric-indifferent-mode            decide numeric-indifferent-mode
o-support-mode                      (DEPRECATED)
pbreak                              production break
popd
port                                debug port
predict                             decide predict
preferences
print
production-find                     production find
pushd
pwatch                              production watch
pwd
rand                                (DEPRECATED)
remove-wme                          wm remove
replay-input                        load percepts
rete-net                            load rete-network
rl
run
save-backtraces                     (DEPRECATED)
select                              decide select
set-library-location                (DEPRECATED)
set-stop-phase                      soar stop-phase
smem
soarnews                            (DEPRECATED)
source                              load file
sp
srand                               soar set-random-seed
stats
stop-soar                           soar stop
svs
time                                debug time
timers                              soar timers
unalias                             alias -r
verbose                             (DEPRECATED)
version                             soar version
waitsnc                             soar wait-snc
warnings                            output warnings
watch                               trace
watch-wmes                          wm watch
wma                                 wm activation


=========
Problems?
=========

If you have any issues, send a message to the soar-help mailing list, which is 
read by many helpful members of the community.

- First join the mailing list at https://lists.sourceforge.net/lists/listinfo/soar-help
- Then send your question to soar-help@lists.sourceforge.net
