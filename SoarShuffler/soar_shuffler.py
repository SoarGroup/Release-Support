#!/usr/bin/env python3

# Given paths specified via the environment and a project list file,
# this script will copy the specified files into the output directory,
# creating a release-ready directory structure.

# Note: you need to create a jars/ dir and put the required jars there.
# TODO: that's dumb, fix that

from dataclasses import dataclass, field
from itertools import chain
import os
from pathlib import Path
import re
import shutil
import sys
from typing import Dict, List
import zipfile

VERSION = os.environ.get("SOAR_RELEASE_VERSION")

ROOT_VAR = "$ROOT"
COMPILE_DIR_VAR = "$COMPILE_DIR"
LAUNCH_EXTENSION_VAR = ".$LAUNCH_EXTENSION"
EXECUTABLE_VAR = ".$EXECUTABLE"
DLL_EXTENSION_VAR = ".$DLL_EXTENSION"
PLATFORM_DIR_VAR = "$PLATFORM_DIR"

PLATFORM_SPECIFIC_VARS = [COMPILE_DIR_VAR, LAUNCH_EXTENSION_VAR, EXECUTABLE_VAR, DLL_EXTENSION_VAR, PLATFORM_DIR_VAR]

# any of above strings appearing in a string would indicate that it's platform-specific
PLATFORM_SPECIFIC_RE = re.compile("|".join(map(lambda v: re.escape(v), PLATFORM_SPECIFIC_VARS)))

# Path to directory containing clones of all the SoarGroup repositories
SOAR_GROUP_REPOS_HOME = os.environ["SOAR_GROUP_REPOS_HOME"]

# Maintainer note: these strings must match with those used in various shell scripts
# TODO: would be better to replace those automatically
WINDOWS_PLATFORM_ID = "win_x86-64"
LINUX_PLATFORM_ID = "linux_x86-64"
MAC_x86_64_PLATFORM_ID = "mac_x86-64"
MAC_ARM64_PLATFORM_ID = "mac_ARM64"

PLATFORM_IDs = [WINDOWS_PLATFORM_ID, LINUX_PLATFORM_ID, MAC_x86_64_PLATFORM_ID, MAC_ARM64_PLATFORM_ID]

COMPILED_DIRS = {
    WINDOWS_PLATFORM_ID: os.environ["SOAR_WIN_X86_64_COMPILED_DIR"],
    LINUX_PLATFORM_ID: os.environ["SOAR_LINUX_X86_64_COMPILED_DIR"],
    MAC_x86_64_PLATFORM_ID: os.environ["SOAR_MAC_X86_64_COMPILED_DIR"],
    MAC_ARM64_PLATFORM_ID: os.environ["SOAR_MAC_ARM64_COMPILED_DIR"],
}

OUTPUT_DIR = Path(os.environ["SOAR_SHUFFLER_OUTPUT_DIR"])

@dataclass
class ProjectEntry:
    copyList: List = field(default_factory=list)
    type: str = "zip"
    out: str = ""


def clean_output_dir():
    print ("Cleaning output directory")
    if (OUTPUT_DIR.exists()):
        shutil.rmtree(OUTPUT_DIR)
        while (os.path.exists(OUTPUT_DIR)):
            pass
    OUTPUT_DIR.mkdir()

def __load_release_spec(spec_path):
    print ("Loading projects list...")
    projects: Dict[str, ProjectEntry] = {}
    with open(spec_path, 'r') as f_filelist:
        for line in f_filelist:
            line = str.strip(line)
            if not line or line.startswith("#"):
                continue

            line = line.replace("$VERSION", VERSION)
            line = line.replace("$SOAR_GROUP_REPOS_HOME", SOAR_GROUP_REPOS_HOME)

            split_entry = str.split(line,"=")
            if (len(split_entry) == 1):
                new_project = ProjectEntry()
                projects[split_entry[0]] = new_project
            elif (split_entry[0] == 'type'):
                new_project.type = split_entry[1]
            elif (split_entry[0] == 'out'):
                new_project.out = split_entry[1]
            else:
                new_project.copyList.append((split_entry[0],split_entry[1]))
    print (" - Project list loaded.")
    return projects

def ignore_list(src, names):
    return [n for n in names if n.startswith(".svn") or n.startswith(".git")]

def copy_project(projectName, projects: Dict[str, ProjectEntry]):
    print (f"Copying project {projectName}")
    destination_path = OUTPUT_DIR / projects[projectName].out
    if (not destination_path.exists()):
        print (f"Creating directory {destination_path}")
        destination_path.mkdir(parents=True)

    for a,b in projects[projectName].copyList:
        source = Path(a)
        if b == ROOT_VAR:
            destination = destination_path
        else:
            destination = destination_path / b
            print(f" - Checking if destination {destination} exists")
            if (not destination.exists() and not source.is_dir()):
                print (f"Creating directory {destination}")
                destination.mkdir(parents=True)
        if (source.is_dir()):
            # destination = destination / os.path.basename(source)
            if destination.exists():
                print (f" - Skipping directory copy: {source} --> {destination} (already exists)")
                continue
            print (f" - Performing dir copy: {source} --> {destination}")
            shutil.copytree(source, destination, ignore=ignore_list)
        else:
            print (f" - Performing file copy: {source} --> {destination}")
            shutil.copy2(source, destination)

def zip_project(projectName, projects: Dict[str, ProjectEntry]):
    print(f"Zipping up project {projectName}")
    seen_list = list()

    project = projects[projectName]

    destination_zip = OUTPUT_DIR / project.out / (projectName+".zip")
    destination_dir = destination_zip.parent
    if (not destination_dir.exists()):
        print (" - Creating directory"), destination_dir
        destination_dir.mkdir(parents=True)

    with zipfile.ZipFile(destination_zip, 'w', compression=zipfile.ZIP_DEFLATED) as dest_zip:
        for a,b in project.copyList:
            source = Path(a)
            platform_suffix = ""
            for platform_id in PLATFORM_IDs:
                if (f"$SPECIALIZE-{platform_id}" in b):
                    b = b.replace(f"$SPECIALIZE-{platform_id}", "")
                    platform_suffix = "-" + platform_id
            if b == ROOT_VAR:
                destination = Path(projectName)
            else:
                destination = Path(projectName, b)
            if (source.is_dir()):
                # destination = destination / os.path.basename(source)
                for root, dirs, files in os.walk(source):
                    if (".svn" in root or ".git" in root):
                        print (f" - Ignoring version control directory {root}")
                        continue
                    for f in files:
                        f = f + platform_suffix
                        fname = os.path.join(root, f)
                        dname = os.path.join(destination, os.path.relpath(fname, source))
                        if (dname in seen_list):
                            print (f" - Skipping already added file from directory: {dname}")
                        else:
                            print (f" - Adding file from directory to zip: {fname}")
                            dest_zip.write(fname, dname , zipfile.ZIP_DEFLATED)
                            seen_list.append(str(dname))
                    if not files and not dirs:
                        dname = os.path.join(destination, os.path.relpath(root, source)) + "/"
                        if (dname in seen_list):
                            print (f" - Skipping already added empty directory: {dname}")
                        else:
                            print (f" - Adding empty directory to zip: {fname}\n"
								f"                                     {dname}")
                            zipInfo = zipfile.ZipInfo(dname + "/")
                            #Some web sites suggest using 48 or 64.  Don't know if this line is necessary at all.
                            zipInfo.external_attr = 16
                            dest_zip.writestr(zipInfo, "")
                            seen_list.append(str(dname))
            else:
                dname = os.path.join(destination, os.path.basename(source) + platform_suffix)
                if (dname in seen_list):
                    print (f" - Skipping already added file: {dname}")
                else:
                    print(f" - Adding single file to zip: {dname}")
                    dest_zip.write(source, dname , zipfile.ZIP_DEFLATED)
                    seen_list.append(str(dname))
        for zinfo in dest_zip.filelist:
            if ('.sh' in zinfo.filename):
                zinfo.external_attr = 2180841472
                zinfo.internal_attr = 1
                zinfo.create_system = 3
            if ('.command' in zinfo.filename):
                zinfo.external_attr = 2180988928
                zinfo.internal_attr = 0
                zinfo.create_system = 3

def _specialize_for_windows(a: str, b:str):
    a = a.replace(LAUNCH_EXTENSION_VAR, ".bat")
    a = a.replace(EXECUTABLE_VAR, ".exe")
    a = a.replace(COMPILE_DIR_VAR, COMPILED_DIRS[WINDOWS_PLATFORM_ID])
    b = b.replace("^", "")
    b = b.replace(PLATFORM_DIR_VAR, WINDOWS_PLATFORM_ID)
    if (DLL_EXTENSION_VAR in a):
        if ("_Python_sml_ClientInterface" in a):
            a = a.replace(DLL_EXTENSION_VAR, ".pyd")
        else:
            a = a.replace(DLL_EXTENSION_VAR, ".dll")
            d,f = os.path.split(a)
            if f.startswith('lib'):
                a = os.path.join(d,f[3:])
    return a, b

def multiplatformize_project(projectName:str, project: ProjectEntry):
    # remove leading "multiplatform-"
    project_type = project.type[project.type.find("-")+1:]

    print (f"Creating multi-platform project {projectName}")
    new_entry = ProjectEntry(type=project_type, out=project.out)

    print (" - Specializing files for Windows...")
    for a,b in project.copyList:
        a, b = _specialize_for_windows(a, b)
        new_entry.copyList.append((a,b))
        print (f"   - Adding zip operation: {a} --> {b}")

    print (" - Specializing files for Linux...")
    for a,b in project.copyList:
        if (b.find("^") == -1):
            a = a.replace(DLL_EXTENSION_VAR, ".so")
            a = a.replace(EXECUTABLE_VAR, "")
            a = a.replace(LAUNCH_EXTENSION_VAR, ".sh")
            a = a.replace(COMPILE_DIR_VAR, COMPILED_DIRS[LINUX_PLATFORM_ID])
            b = b.replace(PLATFORM_DIR_VAR, LINUX_PLATFORM_ID)
            new_entry.copyList.append((a,b))
            print(f"   - Adding zip operation: {a} --> {b}")

    print (" - Specializing files for macOS x86-64...")
    for a,b in project.copyList:
        if (b.find("^") == -1):
            a = a.replace(COMPILE_DIR_VAR, COMPILED_DIRS[MAC_x86_64_PLATFORM_ID])
            a = a.replace(LAUNCH_EXTENSION_VAR, ".sh")
            a = a.replace(EXECUTABLE_VAR, "")
            if ("libJava_sml_ClientInterface" in a):
                a = a.replace(DLL_EXTENSION_VAR, ".jnilib")
            elif ("_Python_sml_ClientInterface" in a):
                a = a.replace(DLL_EXTENSION_VAR, ".so")
            else:
                a = a.replace(DLL_EXTENSION_VAR, ".dylib")
            b = b.replace(PLATFORM_DIR_VAR, MAC_x86_64_PLATFORM_ID)
            new_entry.copyList.append((a,b))
            print(f"   - Adding zip operation: {a} --> {b}")

    print (" - Specializing files for macOS ARM64...")
    for a,b in project.copyList:
        if (b.find("^") == -1):
            a = a.replace(COMPILE_DIR_VAR, COMPILED_DIRS[MAC_ARM64_PLATFORM_ID])
            a = a.replace(LAUNCH_EXTENSION_VAR, ".sh")
            a = a.replace(EXECUTABLE_VAR, "")
            if ("libJava_sml_ClientInterface" in a):
                a = a.replace(DLL_EXTENSION_VAR, ".jnilib")
            elif ("_Python_sml_ClientInterface" in a):
                a = a.replace(DLL_EXTENSION_VAR, ".so")
            else:
                a = a.replace(DLL_EXTENSION_VAR, ".dylib")
            b = b.replace(PLATFORM_DIR_VAR, MAC_ARM64_PLATFORM_ID)
            new_entry.copyList.append((a,b))
            print(f"   - Adding zip operation: {a} --> {b}")

    return new_entry

def print_attr(fileName):
    with zipfile.ZipFile(fileName, 'r') as dest_zip:
        for zinfo in dest_zip.filelist:
            print (zinfo.filename, zinfo.internal_attr, zinfo.external_attr, zinfo.create_system)

def __generate_multiplatform_projects(projects: Dict[str, ProjectEntry]):
    new_projects: Dict[str, ProjectEntry] = {}
    for name, project in projects.items():
        project_type = projects[name].type
        if project_type.startswith("multiplatform-"):
            new_projects[name + "-Multiplatform"] = multiplatformize_project(name, project)

    return new_projects


def shuffle(spec_path):
    for path in chain(COMPILED_DIRS.values(), [SOAR_GROUP_REPOS_HOME]):
        if not Path(path).exists():
            raise ValueError(f"Error: {path} does not exist")

    clean_output_dir()
    all_projects = __load_release_spec(spec_path)

    mp_projects = __generate_multiplatform_projects(all_projects)
    all_projects.update(mp_projects)

    for name in all_projects:
        if all_projects[name].type == "zip":
            zip_project(name, all_projects)
        elif all_projects[name].type == "copy":
            copy_project(name, all_projects)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 release.py <Soar_Projects_Filelist.txt>", file=sys.stderr)
        exit(1)
    shuffle(sys.argv[1])
