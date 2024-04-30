# Soar 9.6.3 Release Notes, 2024

This release of Soar includes TODO: summary here

## Breaking Changes

* New chunking setting, automatically-create-singletons, on by default
  * In our work we've found that we usually want all attributes to be singletons by default unless explicitly specified otherwise. This setting attempts creating singletons for every string attribute. We expect this to be a saner default for all users, and think it unlikely to have a negative effect on existing projects. If you have a project that relies on non-singleton attributes, you can disable this setting by setting `chunking automatically-create-singletons off`.

## New Features

* TODO header
    * TODO line item
    * TODO line item

## Other Changes

* Bug fixes
    * TODO

* VisualSoar bug fixes (thanks to amnuxoll):
  * TODO

* Infrastructure improvements
    * TODO

* Cruft and cleanup
    * TODO

## General Information

Soar can be downloaded by following the download link on the Soar home
page at:

     http://soar.eecs.umich.edu/articles/downloads/soar-suite

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