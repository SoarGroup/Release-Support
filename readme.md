# Soar Release Tools

## Current Release Process

* Update version numbers in Soar everywhere (see `example_version_bump.patch`). TODO: write some awk to do this automatically.

* Add a new release notes file under the `txt/` directory
* Clone all of SoarGroup's repos into a directory
* generate the manual via the makefile under `ManualSource`, or grab the built one from this repository's GH action workflow result. It should be placed in the `pdf` directory.
* Download the Windows, Mac (x86-64) and Linux builds of Soar from the desired GH action workflow result
* Build the mac_ARM64 version locally (hope you have an M1 or M2 computer :) GH doesn't offer CI for it yet)
* Gather the following jar's under SoarShuffler/jars:
    - Eaters_TankSoar.jar
    - VisualSoar.jar
    - commons-logging-1.1.1.jar
    - log4j-1.2.15.jar
    - stopwatch-0.4-with-deps.jar

VisualSoar and Eaters_TankSoar must be built from their repositories (although I had to fix VisualSoar, see https://github.com/SoarGroup/VisualSoar/issues/1), and the others are in the `lib/` directory in the VisualSoar repository. Note that the log4j one is *not* affected by the famous security bug.

* Set your environment variables for SoarShuffler. Here's my .env for an example:

```bash
export SOAR_RELEASE_VERSION=9.6.2
export SOAR_SHUFFLER_OUTPUT_DIR=./SoarRelease
export SOAR_WIN_X86_64_COMPILED_DIR=~/Downloads/Soar_windows-x86-64_out
export SOAR_LINUX_X86_64_COMPILED_DIR=~/Downloads/Soar_linux-x86-64_out
export SOAR_MAC_X86_64_COMPILED_DIR=~/Downloads/Soar_mac-x86-64_out
export SOAR_MAC_ARM64_COMPILED_DIR=~/dev/workspaces/c_workspace/Soar/out
export SOAR_GROUP_REPOS_HOME=~/dev/workspaces/c_workspace/
```

* Run SoarShuffle:

    cd SoarShuffle
    python3 soar_shuffler.py Soar_Projects_Filelist.txt

You'll get the release directories wherever you specified in the `SOAR_SHUFFLER_OUTPUT_DIR` env var.
