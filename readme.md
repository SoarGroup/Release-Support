# Soar Release Tools

## Current Release Process

* Changes to `SoarTutorial/*.docx` need to be manually exported from Word to `pdf/`.
* Update version numbers in Soar everywhere (see `example_version_bump.patch`). TODO: write some awk to do this automatically.
* Update version numbers in `txt/README`.
* Add a new release notes file under the `txt/` directory
* Add some cursory release notes in `txt/README`
* Clone all of SoarGroup's repos into a directory
* generate the manual via the makefile under `ManualSource`, or grab the built one from this repository's GH action workflow result. It should be placed in the `pdf/` directory.
* Download the Windows, macos-12 (x86-64), macos-latest (ARM) and Linux builds of Soar from the desired GH action workflow result.
* Fix the classpath in the manifest (https://github.com/SoarGroup/VisualSoar/issues/1) and build VisualSoar
* Convert VisualSoar's manual to pdf:
  - `brew install basictex`
  - open new shell
  - `sudo tlmgr install soul`
  - `cd VisualSoar/doc/usersman`
  - `pandoc -o VisualSoar_UsersManual.pdf VisualSoar_UsersManual.docx`
* Gather the following jar's under SoarShuffler/jars:
    - Eaters_TankSoar.jar
    - commons-logging-1.1.1.jar
    - log4j-1.2.15.jar
    - stopwatch-0.4-with-deps.jar

VisualSoar and Eaters_TankSoar must be built from their repositories (although I had to fix VisualSoar, see https://github.com/SoarGroup/VisualSoar/issues/1), and the others are in the `lib/` directory in the VisualSoar repository. Note that the log4j one is *not* affected by the famous security bug.

* Set your environment variables for SoarShuffler. Here's my .env for an example (you can source this automatically using tools like [dotenv](https://github.com/ohmyzsh/ohmyzsh/tree/master/plugins/dotenv)):

```bash
export SOAR_RELEASE_VERSION=9.6.3
export SOAR_SHUFFLER_OUTPUT_DIR=./Soar-Release-$SOAR_RELEASE_VERSION
export SOAR_WIN_X86_64_COMPILED_DIR=~/Downloads/Soar_windows-x86-64_out
export SOAR_LINUX_X86_64_COMPILED_DIR=~/Downloads/Soar_linux-x86-64_out
export SOAR_MAC_X86_64_COMPILED_DIR=~/Downloads/Soar_mac-x86-64_out
export SOAR_MAC_ARM64_COMPILED_DIR=~/dev/workspaces/release_soar_workspace/Soar/out
export SOAR_GROUP_REPOS_HOME=~/dev/workspaces/release_soar_workspace
echo -e "\e[93mReminder: Check that $SOAR_MAC_ARM64_COMPILED_DIR is checked out at the tag you desire and is freshly recompiled\e[0m"
```

* Run SoarShuffle:

    cd SoarShuffle
    python3 soar_shuffler.py Soar_Projects_Filelist.txt

The script will tell you if it can't find any files that it needs. You'll probably need to run it a couple of times to hunt down all of the files you need. You'll probably want to `rm -rf SoarSuite` between runs, just to make sure you aren't keeping any old files in the release.

You'll get the release directories wherever you specified in the `SOAR_SHUFFLER_OUTPUT_DIR` env var.

* Finally, unzip the release directories in `SoarRelease/SoarSuite` and check that VisualSoar, the debugger, TankSoar, and SoarCLI all work with a simple double-click.
* Share the release with others and get feedback.
* Once you're happy with it, delete the directories you unzipped and, then zip/tarball up the `SoarRelease` directory and upload to the release on GitHub.
  - `zip -r Soar-Release-<version>.zip Soar-Release-<version>`
  - `tar -czvf Soar-Release-<version>.tar.gz Soar-Release-<version>`
* Upload the Soar and VisualSoar manuals to the release, as well
* Push a releases/$VERSION tag for Soar, and $VERSION tags for other Release-Support and VisualSoar.
* Update the Soar website with the new release information: https://github.com/SoarGroup/SoarGroup.github.io
