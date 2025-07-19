# Soar Release Tools

## Current Release Process

* Set your environment variables for SoarShuffler. Here's my .env for an example (you can source this automatically using tools like [dotenv](https://github.com/ohmyzsh/ohmyzsh/tree/master/plugins/dotenv)):

```bash
export SOAR_RELEASE_VERSION=9.6.4
export SOAR_SHUFFLER_OUTPUT_DIR=./Soar-Release-$SOAR_RELEASE_VERSION
export SOAR_WIN_X86_64_COMPILED_DIR=~/Downloads/Soar_windows-x86-64_out
export SOAR_LINUX_X86_64_COMPILED_DIR=~/Downloads/Soar_linux-x86-64_out
export SOAR_MAC_X86_64_COMPILED_DIR=~/Downloads/Soar_mac-x86-64_out
export SOAR_MAC_ARM64_COMPILED_DIR=~/Downloads/Soar_mac-ARM64_out
export SOAR_GROUP_REPOS_HOME=~/dev/workspaces/release_soar_workspace
```

* Run `python3 release.py`, which will walk you through all of the steps to create a release. Most of them are currently manual, unfortunately.
