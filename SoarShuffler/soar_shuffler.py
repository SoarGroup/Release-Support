import os
import zipfile
import shutil
import re
import pdb

SPL = dict()
Repository_Dir = "/Users/mazzin/git/Soar/"
Input_Dir = "/Users/mazzin/git/Soar/Release-Support/Shuffler_Input/"
Output_Dir = "/Users/mazzin/git/Soar/Release-Support/Shuffler_Output/"
# Note that there are some hard-coded path info in Soar_Projects_Filelist as well, for example the name of the Agents repo

def clean_output_dir():
    print "Cleaning output directory"
    if (os.path.exists(Output_Dir)):
        shutil.rmtree(Output_Dir)
        while (os.path.exists(Output_Dir)):
            pass
    os.makedirs(Output_Dir)

def load_project_list():
    print "Loading projects list"
    with open('Soar_Projects_Filelist.py', 'r') as f_filelist:
        for line in f_filelist:
            #print " - Parsing ", line,
            line = str.strip(line)
            if (not line[0]=="#"):
                split_entry = str.split(line,"=")
                if (len(line) > 0):
                    if (len(split_entry) == 1):
                        SPL[split_entry[0]] = dict([('copyList', list()), ('type', 'zip'), ('out', '')])
                        current_project = split_entry[0]
                    elif (split_entry[0] in ('type', 'out')):
                        SPL[current_project][split_entry[0]] = split_entry[1]
                    else:
                        SPL[current_project]['copyList'].append((split_entry[0],split_entry[1]))
    print " - Project list loaded."

def ignore_list(src, names):
    import pdb
    pdb.set_trace()
    return [n for n in names if n.startswith(".svn") or n.startswith(".git")]

def copy_project(projectName):
    destination_path = os.path.join(Output_Dir, SPL[projectName]['out'])
    print "Copying project", projectName
    if (not os.path.exists(os.path.dirname(destination_path))):
        os.makedirs(os.path.dirname(destination_path))

    for a,b in SPL[projectName]["copyList"]:
        source = os.path.join(Repository_Dir, a)
        if b == "top":
            destination = destination_path
        else:
            destination = os.path.join(destination_path,b)
            print " - Checking if destination", destination, "exists"
            if (not os.path.exists(destination)):
                print "Creating directory ", destination
                os.makedirs(destination)
        print " - Performing copy: ", source, "-->", destination
        if (os.path.isdir(source)):
            shutil.copytree(source, os.path.join(destination,os.path.basename(source)), ignore=ignore_list)
        else:
            shutil.copy2(source, destination)

def zip_project(projectName):
    print "Zipping up project", projectName
    seen_list = list()

    destination_zip = os.path.join(Output_Dir, SPL[projectName]['out'],(projectName+".zip"))
    if (not os.path.exists(os.path.dirname(destination_zip))):
        print " - Creating directory", os.path.dirname(destination_zip)
        os.makedirs(os.path.dirname(destination_zip))

    with zipfile.ZipFile(destination_zip, 'w', compression=zipfile.ZIP_DEFLATED) as dest_zip:
        for a,b in SPL[projectName]["copyList"]:
            source = os.path.join(Repository_Dir, a)
            platform_suffix = ""
            if (re.search("SPECIALIZE-win64",b)):
                b = b.replace("SPECIALIZE-win64", r"")
                platform_suffix = "-win64"
            if (re.search("SPECIALIZE-linux64",b)):
                b = b.replace("SPECIALIZE-linux64", r"")
                platform_suffix = "-linux64"
            if (re.search("SPECIALIZE-mac64",b)):
                b = b.replace("SPECIALIZE-mac64", r"")
                platform_suffix = "-mac64"
            if b == "top":
                destination = os.path.join(projectName)
            else:
                destination = os.path.join(projectName,b)
            if (os.path.isdir(source)):
                for root, dirs, files in os.walk(source):
                    if (".svn" in root or ".git" in root):
                        print " - Ignoring version control directory", root
                        continue
                    for f in files:
                        f = f + platform_suffix
                        fname = os.path.join(root, f)
                        dname = os.path.join(destination, os.path.relpath(fname, source))
                        if (dname in seen_list):
                            print " - Skipping already added file from directory:", dname
                        else:
#                             print " - Adding file from directory to zip:", fname, "\n                                     ", dname
                            print " - Adding file from directory to zip:", fname
                            dest_zip.write(fname, dname , zipfile.ZIP_DEFLATED)
                            seen_list.append(str(dname))
                    if not files and not dirs:
                        dname = os.path.join(destination, os.path.relpath(root, source)) + "/"
                        if (dname in seen_list):
                            print " - Skipping already added empty directory:", dname
                        else:
                            print " - Adding empty directory to zip:", fname, "\n                                     ", dname
                            zipInfo = zipfile.ZipInfo(dname + "/")
                            #Some web sites suggest using 48 or 64.  Don't know if this line is necessary at all.
                            zipInfo.external_attr = 16
                            dest_zip.writestr(zipInfo, "")
                            seen_list.append(str(dname))
            else:
                dname = os.path.join(destination, os.path.basename(source) + platform_suffix)
                if (dname in seen_list):
                    print " - Skipping already added file:", dname
                else:
                    print " - Adding single file to zip:", dname
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

def multiplatformize_project(projectName):
    print "Creating multi-platform project", projectName
    SPL_New = dict()
    SPL_New['type']='zip'
    SPL_New['out']=SPL[projectName]['out']
    SPL_New['copyList']=list()
    
    print " - Specializing files for Windows..."
    for a,b in SPL[projectName]["copyList"]:
        a = re.sub("RELEASE_DIR", "win", a)
        a = re.sub("\.LAUNCH_EXTENSION", ".bat", a)
        a = re.sub("\.EXECUTABLE", ".exe", a)
        a = re.sub("COMPILE_DIR", "windows64", a)
        b = b.replace("^", r"")
        b = b.replace("PLATFORM_DIR", "win64")
        if (re.search("\.DLL_EXTENSION",a)):
            if (re.search("_Python_sml_ClientInterface",a)):
                a = re.sub("\.DLL_EXTENSION", ".pyd", a)
            else:
                a = re.sub("\.DLL_EXTENSION", ".dll", a)
                d,f = os.path.split(a)
                a = os.path.join(d,f[3:])
        SPL_New['copyList'].append((a,b))
        print "   - Adding zip operation:", a, "--> ", b
    
    print " - Specializing files for Linux..."
    for a,b in SPL[projectName]["copyList"]:
        if (b.find("^") == -1):
            a = re.sub("\.DLL_EXTENSION", ".so", a)
            a = re.sub("\.EXECUTABLE", "", a)
            a = re.sub("RELEASE_DIR", "linux", a)
            a = re.sub("\.LAUNCH_EXTENSION", ".sh", a)
            a = re.sub("COMPILE_DIR", "linux64", a)
            b = b.replace("PLATFORM_DIR", "linux64")
            SPL_New['copyList'].append((a,b))
            print "   - Adding zip operation:", a, "--> ", b
    
    print " - Specializing files for OSX..."
    for a,b in SPL[projectName]["copyList"]:
        if (b.find("^") == -1):
            a = re.sub("COMPILE_DIR", "mac64", a)
            a = re.sub("RELEASE_DIR", "osx", a)
            a = re.sub("\.LAUNCH_EXTENSION", ".sh", a)
            a = re.sub("\.EXECUTABLE", "", a)
            if (re.search("libJava_sml_ClientInterface",a)):
                a = re.sub("\.DLL_EXTENSION", ".jnilib", a)
            elif (re.search("_Python_sml_ClientInterface",a)):
                a = re.sub("\.DLL_EXTENSION", ".so", a)
            else:
                a = re.sub("\.DLL_EXTENSION", ".dylib", a)
            b = b.replace("PLATFORM_DIR", "mac64")
            SPL_New['copyList'].append((a,b))
            print "   - Adding zip operation:", a, "--> ", b
    return SPL_New

def print_attr(fileName):
    with zipfile.ZipFile(fileName, 'r') as dest_zip:
        for zinfo in dest_zip.filelist:
            print zinfo.filename, zinfo.internal_attr, zinfo.external_attr, zinfo.create_system

def doit():
    clean_output_dir()
    load_project_list()
    SPL_New = dict()
    for p, i in SPL.iteritems():
        if SPL[p]["type"] == "multiplatform-zip":
            SPL_New[p + "-Multiplatform_64bit"] = multiplatformize_project(p)
    for p, i in SPL_New.iteritems():
        SPL[p] = i
    for p, i in SPL.iteritems():
        if SPL[p]["type"] == "zip":
            zip_project(p)
        elif SPL[p]["type"] == "copy":
            copy_project(p)
