Soar Java Debugger Command Line Options

-remote => use a remote connection (with default ip and port values)
-ip xxx => use this IP value (implies remote connection)
-port ppp => use this port (implies remote connection, without any remote options we start a local kernel)
-agent <name> => on a remote connection select this agent as initial agent
-agent <name> => on a local connection use this as the name of the initial agent
-source "<path>" => load this file of productions on launch (only valid for local kernel)
-quitonfinish => when combined with source causes the debugger to exit after sourcing that one file
-listen ppp => use this port to listen for remote connections (only valid for a local kernel)
-maximize => start with maximized window
-width <width> => start with this window width
-height <height> => start with this window height
-x <x> -y <y> => start with this window position
-cascade => cascade each window that starts (offseting from the -x <x> -y <y> if given). This option now always on. (Providing width/height/x/y => not a maximized window)