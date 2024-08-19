# Soar 9.6.3 Release Notes, 2024

This release of Soar includes lots of VisualSoar goodies.

## Addendum Aug. 19, 2024

The release was re-created due to issues running on Mac.

## Breaking Changes

* New chunking setting, automatically-create-singletons, on by default
  * In our work we've found that we usually want all attributes to be singletons by default unless explicitly specified otherwise. This setting attempts creating singletons for every string attribute. We expect this to be a saner default for all users, and think it unlikely to have a negative effect on existing projects. If you have a project that relies on non-singleton attributes, you can disable this setting by setting `chunking automatically-create-singletons off`.

* Linux users: Soar was compiled on the recent Ubuntu 24.04, so you may need to update your system or libstdc++ to run the included binaries (or else build from source yourself).

## New Features

* Visual-Soar improvements (thanks to amnuxoll)
  * A datamap can import the datamap of another project
  * Projects can be opened read-only
  * Less change noise, i.e. more friendly towards version control
  * Automatically opens the last project on startup; new "Open Recent" menu option
  * Parser now supports LTI predicates
  * Lots more smaller improvements

* You can pip-install Soar! (thanks to ShadowJonathan)
  * `pip install soar-sml[compat]` is a drop-in replacement for manually installing Soar somewhere and adding its path to your PYTHONPATH environment variable.
  * Note that this does not come with the debugger or other Java applications.
* New svs commands `--disable-in-substates` and `--enable-in-substates`. By default SVS copies the entire scene graph into each substate. This can be disabled with `--disable-in-substates` to save memory and improve performance. This can be re-enabled with `--enable-in-substates` if you need to access the scene graph in substates.
* Python bindings are now compatible with all Python versions 3.2 and up, rather than only with the minor version that was used to build Soar. This is thanks to the work of ShadowJonathan.

## New Website

Thanks to Moritz Schmidt, we have a new website! The URL remains the same: https://soar.eecs.umich.edu. New features include:

* HTML versions of the manual and the tutorial
* Snappy full-text search based on lunr.js
* Much improved editing/deployment workflow based on GitHub pages. We also get the full power of GitHub actions, and use it to automatically check for dead links, for example.

Note that some pages and download links still need to be ported. The manual and tutorial still need to be fully inspected for correctness, and the images in particular still need work.

## Other Changes

* Bug fixes
  * Improved Java Debugger stability when adding/removing multiple agents during an application lifetime
  * SVS can no longer be disabled when the current state is a subgoal. Allowing this previously led to undefined behavior.
  * Fixed `Agent.GetLastCommandLineResult()` returning true when the last command actually failed
  * Lots of Visual-Soar bug fixes (thanks to amnuxoll) around parsing, file saving, data preservation, and more

* Java debugger can now be built for ARM Linux (though this is not distributed at this time)

* Infrastructure improvements
    * ARM Mac now built in CI

* Cruft and cleanup
    * lots of compiler warning fixes, and compiler strictness increased

## General Information

Soar can be downloaded by following the download link on the Soar home
page at:

     https://soar.eecs.umich.edu/

Soar releases include source code, demo programs, and a number of
applications that serve as examples of how to interface Soar to an
external environment.  There is support for integrating Soar with C++,
Java, Tcl and Python applications.  Many tools that aid in development
of Soar programs are also available.  The download section of the web site
allows you to browse and download all of the different distributions,
tools and agents.

### Help and Contact information

You can find many helpful resources on the Soar home page at:

     https://soar.eecs.umich.edu

To contact the Soar group, you may join and post to one of our mailing
lists:

For general Soar-related announcements:

        soar-group@lists.sourceforge.net

For help:

        soar-help@lists.sourceforge.net

Also, please do not hesitate to file bugs or feature requests on our issue
tracker at github:

     https://github.com/SoarGroup/Soar/issues

To avoid redundant entries, please search for duplicate issues first.

Pull requests and patches to improve Soar, its documentation or tools are very welcome.

If you would like to fund further development of Soar, please reach out to John Laird:
[laird@umich.edu](mailto:laird@umich.edu).
