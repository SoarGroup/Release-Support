# Soar 9.6.5 Release Notes, 2026

This release of Soar is primarily a **build-system transition release**. The CMake-based build is now first-class alongside SCons, with full multi-platform CI, Conan-managed dependencies, and built-in support for SVS, the Java debugger, and SWIG bindings (Python, Java, Tcl, JavaScript, C#). The user-facing install layout is unchanged: SCons users will not notice a difference, and the multi-platform release zip retains the same structure.

This release also includes a small set of user-facing kernel features and a meaningful round of chunking, episodic-memory, and justification bug fixes.

## New Features

* New chunking literalization control via the `$` test
  * Offers more granular control over chunking generalization. If you mark a variable with this test, it will force literalization. Both the shorthand `$` and explicit `$$` syntax are supported.
* `add-wme` now supports adding a WME with a particular target identifier ([commit 951e6436d](https://github.com/SoarGroup/Soar/commit/951e6436d))
  * Note: chunking does not backtrace through WMEs added this way.
* Semantic memory now emits a single `@` per LTI add when storing knowledge (analogous to `*` per `sp`). The previous verbose `<=SMEM:` / `=>SMEM:` per-edge trace lines are still available via `trace --smem on`.

## Bug fixes

* Episodic memory: orphaned-WME refcount and ID-reservation handling fixed for cases involving exclusions. Corrects a UNIQUE-constraint violation observed when a node that had been excluded "comes back" from epmem's perspective.
* Negative numbers can now be passed as CLI arguments without being parsed as option flags. Thanks, [@marsaustinwilliams](https://github.com/marsaustinwilliams)!
* Episodic memory: `child_n_id` is now stored at assignment time to prevent UNIQUE-constraint violations.
* Justifications: refcount-based use-after-free fix for orphaned justifications.
* Chunking: avoid spurious refcount decrement on chunks during state cleanup when OSK knowledge is the last reference holder.
* Chunking: workaround for a long-standing bug with conjunctive conditions; targeted extension for `<` / `>` literalization.
* Initialize `previous_time` to avoid a runtime check failure.
* `findDelimReplaceEscape` now handles escape characters correctly.
* 32-bit architectures: use atomic operations where required.
* Bad `GetParameterValue` calls now throw, with proper SWIG exception propagation ([PR #465](https://github.com/SoarGroup/Soar/pull/465)).


## Backend / Build-system changes

This release introduces a parallel CMake-based build system. Both SCons and CMake are supported and produce binary-compatible output that lands in the same `out/` and multi-platform install layout.

* Full CMake build of:
  * The Soar kernel
  * `soar` CLI executable
  * Soar Java debugger
  * **SVS** integrated into the kernel build (Conan now manages `sqlite3/3.40.0`, `asio/1.36.0`, and `eigen/3.4.0`; `sqlite3` was already required, the other two are new). Thanks, [@amininger](https://github.com/amininger)!
  * SWIG bindings: **Python, Java, Tcl, JavaScript, C#**. Thanks, [@moschmdt](https://github.com/moschmdt)!
* Python SWIG bindings now build against the Python stable ABI (`Py_LIMITED_API`) -- one `.pyd` works across Python 3.x versions on a given platform.
* `compile_commands.json` is generated automatically for IDE / static-analysis tooling.
* Single source-of-truth `project(VERSION)` -- `soarversion.h` is generated from CMake at configure time.
* Conan-based dependency management for SQLite3, asio, and Eigen3.
* Multi-platform release workflow on GitHub Actions (Windows x86-64, macOS universal, Linux x86-64).
  * The macOS build is a universal binary on `macos-latest`, pinned to `CMAKE_OSX_DEPLOYMENT_TARGET=13.0` (Ventura). Replaces the previous `macos-13` x86-only build.
  * The Linux x86-64 build is pinned to `ubuntu-22.04` (glibc 2.35), so the shipped binary requires a glibc-2.34-or-newer distribution (Ubuntu 22.04+, Debian 12+, RHEL 9+, Fedora 36+, or equivalent).
* `mac_universal/` was renamed to `mac_x86-64/` for compatibility with the historical `setup.sh`.
* Java debugger: Java 11 compatibility restored. The launcher now redirects `stderr` to `nul` / `/dev/null` in Release builds only, suppressing GTK/SWT noise without hiding real JNI errors during development.
* SVS: removed deprecated viewer / old test code (use `JavaSVSViewer` instead).
* SoarUnitTests test fixtures are now shipped in the release zip.

> **Forward-looking note:** Future releases plan to move toward platform-native distribution (msi / dmg / deb). 9.6.5 keeps the existing install structure to remain backwards-compatible for current users.

## VisualSoar

* Initial integration of the new `$` literalization-test syntax in the VisualSoar editor / parser.

## Other

* Several places that should have been 64-bit integers were updated.

## Known issues

* The Soar Manual PDF is no longer built automatically by the release workflow. It is built locally and attached to the GitHub release manually. CI for the PDF will return in a future release. The current PDF production pipeline has rendering issues that we haven't fully resolved.
* `Demo_ToH_Recursive` is excluded from `ctest` because a recent chunking bugfix exposed an issue in this demo that hasn't been addressed yet.

## Documentation

The Soar Manual has been updated for 9.6.5 and is attached to this release, though the [website version](https://soar.eecs.umich.edu/soar_manual/) is the preferred format.

The following documents are unchanged from 9.6.4 -- please grab them from the [9.6.4 release page](https://github.com/SoarGroup/Soar/releases/tag/releases/9.6.4):

* [VisualSoar_UsersManual.pdf](https://github.com/SoarGroup/Soar/releases/download/releases/9.6.4/VisualSoar_UsersManual.pdf)
* [Soar Tutorial Part 1 -- Simple Agents](https://github.com/SoarGroup/Soar/releases/download/releases/9.6.4/Soar.Tutorial.Part.1.-.Simple.Agents.pdf)
* [Soar Tutorial Part 2 -- Interacting with an Environment](https://github.com/SoarGroup/Soar/releases/download/releases/9.6.4/Soar.Tutorial.Part.2.-.Interacting.with.an.Environment.pdf)
* [Soar Tutorial Part 3 -- Subgoals](https://github.com/SoarGroup/Soar/releases/download/releases/9.6.4/Soar.Tutorial.Part.3.-.Subgoals.pdf)
* [Soar Tutorial Part 4 -- Simple Problem-Solving](https://github.com/SoarGroup/Soar/releases/download/releases/9.6.4/Soar.Tutorial.Part.4.-.Simple.Problem-Solving.pdf)
* [Soar Tutorial Part 5 -- Planning and Learning](https://github.com/SoarGroup/Soar/releases/download/releases/9.6.4/Soar.Tutorial.Part.5.-.Planning.and.Learning.pdf)
* [Soar Tutorial Part 6 -- Reinforcement Learning](https://github.com/SoarGroup/Soar/releases/download/releases/9.6.4/Soar.Tutorial.Part.6.-.Reinforcement.Learning.pdf)
* [Soar Tutorial Part 7 -- SMem](https://github.com/SoarGroup/Soar/releases/download/releases/9.6.4/Soar.Tutorial.Part.7.-.SMem.pdf)
* [Soar Tutorial Part 8 -- EpMem](https://github.com/SoarGroup/Soar/releases/download/releases/9.6.4/Soar.Tutorial.Part.8.-.EpMem.pdf)

## Installing

1. Download `SoarSuite_9.6.5-Multiplatform.zip` from this release and extract it to a fresh directory.
2. Open the extracted folder. The launcher scripts handle platform setup automatically; just run the one for your OS:
   * **Windows** -- `SoarJavaDebugger.bat` (GUI), `SoarCLI.bat` (command line), `VisualSoar.bat`.
   * **macOS / Linux** -- `SoarJavaDebugger.sh`, `SoarCLI.sh`, `VisualSoar.sh`.
3. The first launch silently runs `setup.bat` (Windows) or `setup.sh` (macOS / Linux), which moves your platform's binaries into `bin/` and removes the other platforms' files. You can also run `setup.*` manually if you'd rather invoke the `bin/soar` executable directly.
4. The Java debugger and tools require **Java 11 or newer** ([Temurin](https://adoptium.net/) recommended).

> **If you have an existing Soar install:** don't extract 9.6.5 directly on top of it. `setup.*` only runs on first extraction (it skips when `bin/pkgIndex.tcl` is already present), so overwriting in place leaves a mix of old and new files. Either extract 9.6.5 into a new directory, or rename the old folder first and then extract 9.6.5 into a fresh directory at the original name. Once you've confirmed 9.6.5 works, delete the old folder.

## General Information

Soar can be downloaded by following the download link on the Soar home page at:

     https://soar.eecs.umich.edu/

Soar releases include source code, demo programs, and a number of applications that serve as examples of how to interface Soar to an external environment. There is support for integrating Soar with C++, Java, Tcl, Python, JavaScript and C# applications. Many tools that aid in development of Soar programs are also available. The download section of the website allows you to browse and download all of the different distributions, tools and agents.

### Help and Contact information

You can find many helpful resources on the Soar home page at:

     https://soar.eecs.umich.edu

To contact the Soar group, you may join and post to one of our mailing lists:

For general Soar-related announcements:

        soar-group@lists.sourceforge.net

For help:

        soar-help@lists.sourceforge.net

Also, please do not hesitate to file bugs or feature requests on our issue tracker at github:

     https://github.com/SoarGroup/Soar/issues

To avoid redundant entries, please search for duplicate issues first.

Pull requests and patches to improve Soar, its documentation or tools are very welcome.

If you would like to fund further development of Soar, please reach out to John Laird:
[laird@umich.edu](mailto:laird@umich.edu).
