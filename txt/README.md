# Soar 9.6.5 README

*May 2026*

Welcome to Soar! Soar 9.6.5 is the current stable release. It is primarily a **build-system transition release** -- the CMake-based build is now first-class alongside SCons, with multi-platform CI, Conan-managed dependencies, and built-in support for SVS, the Java debugger, and SWIG bindings (Python, Java, Tcl, JavaScript, C#). The user-facing install layout is unchanged from 9.6.4.

This release also includes:

* New chunking literalization control via the `$` test, for finer-grained control over chunk generalization.
* `add-wme` extended to support adding a WME with a specific target identifier.
* A quieter Semantic Memory trace -- one `@` per LTI add (the verbose per-edge trace is still available via `trace --smem on`).
* A meaningful round of chunking, episodic-memory, and justification bug fixes.

For full details, see `Release_Notes_9.6.5.md` (also attached to the GitHub release).

## Installing

1. Extract this zip to a fresh directory.
2. Run the launcher for your OS from the extracted folder:
   * **Windows** -- `SoarJavaDebugger.bat` (GUI), `SoarCLI.bat` (command line), `VisualSoar.bat`.
   * **macOS / Linux** -- `SoarJavaDebugger.sh`, `SoarCLI.sh`, `VisualSoar.sh`.
3. The first launch silently runs `setup.bat` (Windows) or `setup.sh` (macOS / Linux), which moves your platform's binaries from `bin/<platform>/` up into `bin/` and removes the other platforms' files. You can also run `setup.*` manually if you'd rather invoke the `bin/soar` executable directly.
4. The Java debugger and graphical tools require **Java 11 or newer** ([Temurin](https://adoptium.net/) is recommended).

### If you have an existing Soar install

Don't extract 9.6.5 directly on top of it. `setup.*` only runs on first extraction (it skips when `bin/pkgIndex.tcl` is already present), so overwriting in place leaves a mix of old and new files. Either extract 9.6.5 into a new directory, or rename the old folder first and then extract 9.6.5 into a fresh directory at the original name. Once you've confirmed 9.6.5 works, delete the old folder.

## Soar Manual

The 9.6.5 edition of the Soar Manual is attached to the GitHub release page as `SoarManual_9.6.5.pdf`. The preferred format is the online version:

* https://soar.eecs.umich.edu/soar_manual/

The Soar Tutorial PDFs and the VisualSoar User's Manual are unchanged from 9.6.4 and are available on the [9.6.4 release page](https://github.com/SoarGroup/Soar/releases/tag/releases/9.6.4).

## SoarCLI Command Line Options

```
-l            Listen on, i.e. launches Soar kernel in new thread
-n            No syntax coloring (for light terminals or older Windows
              consoles that don't render ANSI color codes; also speeds
              up printing).
-p <port>     Listens on port <port>
-s <file>     Sources file <file> on load
```

To manage multiple agents, use `create`, `list`, and `switch`. These are SoarCLI commands, not native Soar commands -- they are not available in other interfaces (e.g. the Soar Java Debugger).

## Soar Java Debugger Command Line Options

```
-remote             Use a remote connection (with default ip/port)
-ip xxx             Use this IP value (implies remote connection)
-port ppp           Use this port (implies remote connection; without
                    any remote options we start a local kernel)
-agent <name>       On a remote connection, select this agent as the
                    initial agent. On a local connection, use this as
                    the name of the initial agent.
-source <path>      Load this file of productions on launch (only
                    valid for a local kernel)
-quitonfinish       When combined with -source, the debugger exits
                    after sourcing that one file.
-listen ppp         Use this port to listen for remote connections
                    (only valid for a local kernel)
-maximize           Start with maximized window
-width <width>      Start with this window width
-height <height>    Start with this window height
-x <x> -y <y>       Start with this window position
-cascade            Cascade each window that starts (offsetting from
                    -x/-y if given). This option is now always on.
                    Note that providing width/height/x/y => not a
                    maximized window.
```

If the debugger fails to launch, try deleting any `.soar*` files in your home directory -- corrupt settings can cause launch failures.

## Building from Source

Build instructions live in the [Soar repository](https://github.com/SoarGroup/Soar). The CMake-based build is recommended; see the repo `README.md` and the `cmake-multi-platform.yml` workflow under `.github/workflows/` for the canonical setup.

## Problems?

If you have any issues running Soar, building Soar, or writing Soar agents, the soar-help mailing list is read by many helpful members of the community:

* Join: https://groups.google.com/d/forum/soar-help
* Then send your question to <soar-help@googlegroups.com>

For announcements and high-level discussion of Soar, see the soar-cognitive-architecture list:

* Join: https://groups.google.com/g/soar-cognitive-architecture
* Then send to <soar-cognitive-architecture@googlegroups.com>

To file bugs or feature requests, please use the GitHub issue tracker:

* https://github.com/SoarGroup/Soar/issues

Search for duplicate issues first.

Pull requests and patches to improve Soar, its documentation, or its tools are very welcome.

If you would like to fund further development of Soar, please reach out to John Laird: [laird@umich.edu](mailto:laird@umich.edu).
