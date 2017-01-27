#! /usr/bin/python
"""Create the distribution files for Artistic Style Wx.
   Windows distribution is created on Windows.
   Linux distribution is created on Linux.
"""

# to disable the print statement and use the print() function (version 3 format)
from __future__ import print_function

import glob
import os
import shutil
import stat
import subprocess
import time
# local libraries
import libastylewx

# global variables ------------------------------------------------------------

# release number for distribution file
AS_RELEASE = "2.06"

# extract all platforms for testing (Windows, Linux, Mac)
EXTRACT_ALL = False
#EXTRACT_ALL = True

# inut from AStyleWx directory
__astylewx_dir = libastylewx.get_astylewx_directory()
# inut from AStyleWxTest directory
__astylewxtest_dir = libastylewx.get_astylewxtest_directory()
# inut from AStyle directory
__astyle_dir = libastylewx.get_astyle_directory()
# output to Project directory
__base_dir = libastylewx.get_project_directory()

# -----------------------------------------------------------------------------

def main():
    """Main processing function.
    """
    libastylewx.set_text_color("yellow")
    print(libastylewx.get_python_version())
    os.chdir(libastylewx.get_file_py_directory())
    remove_dist_directories()
    if EXTRACT_ALL:
        build_windows_distribution()
        build_linux_distribution()
        build_mac_distribution()
    elif os.name == "nt":
        build_windows_distribution()
    else:
        build_linux_distribution()
        build_mac_distribution()

# -----------------------------------------------------------------------------

def build_linux_distribution():
    """Copy astylewx files to the linux directory.
    """
    print()
    print("* * * * * * * * * * * * * * * * * * * * * * * * * * * * *")
    print("*         Creating AStyleWx Linux Distribution          *")
    print("* * * * * * * * * * * * * * * * * * * * * * * * * * * * *")
    print("Building astyle", AS_RELEASE)
    dist_base = get_distribution_folder_linux()
    dist_astylewx = dist_base + "/astylewx_{0}_linux".format(AS_RELEASE) + "/astylewx"
    os.makedirs(dist_astylewx)

    # top directory
    dist_top = dist_astylewx + "/"
    copy_astylewx_top(dist_top)

    # build directory
    dist_build = dist_astylewx + "/build"
    os.mkdir(dist_build)
    copy_linux_build_directories(dist_build)

    # doc directory
    dist_doc = dist_astylewx + "/doc/"
    os.mkdir(dist_doc)
    copy_astylewx_doc(dist_doc)

    # dialog directory
    dist_dialog = dist_astylewx + "/dialog/"
    os.mkdir(dist_dialog)
    copy_astylewx_dialog(dist_dialog)

    # file-py directory
    dist_python = dist_astylewx + "/file-py/"
    os.mkdir(dist_python)
    copy_astylewx_python_files(dist_python)

    # image directory
    dist_image = dist_astylewx + "/image/"
    os.mkdir(dist_image)
    copy_astylewx_image(dist_image)

    # src directory
    dist_src = dist_astylewx + "/src/"
    os.mkdir(dist_src)
    copy_astylewx_src(dist_src)

    # astyle project
    extract_linux_astyle()

    # create tar.bz2
    print()
    tarname = "astylewx_{0}_linux.tar".format(AS_RELEASE)
    call_7zip(dist_base, tarname)
    bz2name = tarname + ".gz"
    call_7zip(dist_base, bz2name)

# -----------------------------------------------------------------------------

def build_mac_distribution():
    """Copy astylewx files to the mac directory.
    """
    print()
    print("* * * * * * * * * * * * * * * * * * * * * * * * * * * * *")
    print("*          Creating AStyleWx Mac Distribution           *")
    print("* * * * * * * * * * * * * * * * * * * * * * * * * * * * *")
    print("Building astyle", AS_RELEASE)
    dist_base = get_distribution_folder_mac()
    dist_astylewx = dist_base + "/astylewx_{0}_macos".format(AS_RELEASE) + "/astylewx"
    os.makedirs(dist_astylewx)

    # top directory
    dist_top = dist_astylewx + "/"
    copy_astylewx_top(dist_top)

    # build directory
    dist_build = dist_astylewx + "/build"
    os.mkdir(dist_build)
    copy_mac_build_directories(dist_build)

    # doc directory
    dist_doc = dist_astylewx + "/doc/"
    os.mkdir(dist_doc)
    copy_astylewx_doc(dist_doc)

    # dialog directory
    dist_dialog = dist_astylewx + "/dialog/"
    os.mkdir(dist_dialog)
    copy_astylewx_dialog(dist_dialog)

    # file-py directory
    dist_python = dist_astylewx + "/file-py/"
    os.mkdir(dist_python)
    copy_astylewx_python_files(dist_python)

    # image directory
    dist_image = dist_astylewx + "/image/"
    os.mkdir(dist_image)
    copy_astylewx_image(dist_image)

    # src directory
    dist_src = dist_astylewx + "/src/"
    os.mkdir(dist_src)
    copy_astylewx_src(dist_src)

    # astyle project
    extract_mac_astyle()

    # create tar.gz
    print()
    tarname = "astylewx_{0}_macos.tar".format(AS_RELEASE)
    call_7zip(dist_base, tarname)
    gzname = tarname + ".gz"
    call_7zip(dist_base, gzname)

# -----------------------------------------------------------------------------

def build_windows_distribution():
    """Copy astylewx files to the windows directory.
    """
    print()
    print("* * * * * * * * * * * * * * * * * * * * * * * * * * * * *")
    print("*       Creating AStyleWx XP Windows Distribution       *")
    print("* * * * * * * * * * * * * * * * * * * * * * * * * * * * *")
    # the following variables may be modified except vscfg=libastyle.STATIC_XP
    vsdir = libastylewx.VS_RELEASE
    wxrel = libastylewx.WX_RELEASE
    vscfg = libastylewx.STATIC_XP

    print("Compiling with {0} XP wxWidgets {1}".format(vsdir, wxrel))
    print("Building AStyleWx release", AS_RELEASE)
    dist_base = get_distribution_folder_windows()
    dist_astylewx = dist_base + "/AStyleWx_{0}_windows".format(AS_RELEASE) + "/AStyleWx"
    os.makedirs(dist_astylewx)
    libastylewx.build_astylewx_executable(vscfg)

    # Windows includes an executable in the bin directory
    print("copying exe")
    dist_astylewx_bin = dist_astylewx + "/bin/"
    os.mkdir(dist_astylewx_bin)
    astylewx_build_directory = libastylewx.get_astylewx_build_directory(vscfg)
    if vscfg == libastylewx.STATIC_XP:
        shutil.copy(astylewx_build_directory + "/binstatic/AStyleWx.exe", dist_astylewx_bin)
    else:
        libastylewx.system_exit("Invalid compile configuration: " + vscfg)

    # top directory
    dist_top = dist_astylewx + "/"
    copy_astylewx_top(dist_top, True)

    # build directory
    dist_build = dist_astylewx + "/build"
    os.mkdir(dist_build)
    copy_windows_build_directories(dist_build)

    # doc directory
    dist_doc = dist_astylewx + "/doc/"
    os.mkdir(dist_doc)
    copy_astylewx_doc(dist_doc, True)

    # dialog directory
    dist_dialog = dist_astylewx + "/dialog/"
    os.mkdir(dist_dialog)
    copy_astylewx_dialog(dist_dialog, True)

    # file-py directory
    dist_python = dist_astylewx + "/file-py/"
    os.mkdir(dist_python)
    copy_astylewx_python_files(dist_python)

    # image directory
    dist_image = dist_astylewx + "/image/"
    os.mkdir(dist_image)
    copy_astylewx_image(dist_image)

    # src directory
    dist_src = dist_astylewx + "/src/"
    os.mkdir(dist_src)
    copy_astylewx_src(dist_src, True)

    # astyle project
    extract_windows_astyle()

    # create zip
    print()
    zipfile = "AStyleWx_{0}_windows.zip".format(AS_RELEASE)
    call_7zip(dist_base, zipfile)

# -----------------------------------------------------------------------------

def call_7zip(dist_base, compressed_file):
    """Call 7zip to create an archive.
       arg 1- the directory to compress.
       arg 2- name of the compressed file.
    """
    exepath = libastylewx.get_7zip_path()
    compress = [exepath, "a", compressed_file]
    # check file ending to see if it is a tarball
    if compressed_file.endswith((".gz", ".bz2")):
        compress.append("*.tar")
    # stdout file must have full path since 'cwd' is used in call
    filename = libastylewx.get_file_py_directory(True) + "compress.txt"
    outfile = open(filename, 'w')
    try:
        subprocess.check_call(compress, cwd=dist_base, stdout=outfile)
    except subprocess.CalledProcessError as err:
        libastylewx.system_exit("Bad 7zip return: " + str(err.returncode))
    except OSError:
        libastylewx.system_exit("Cannot find executable: " + compress[0])
    outfile.close()
    os.remove(filename)
    print(compressed_file + " created")

# -----------------------------------------------------------------------------

def convert_line_ends(dist_dir, to_dos):
    """Convert line ends to dos (CRLF) or linux (LF).
       Needs tofrodos package.
       All files in a directory are converted.
    """
    files = glob.glob(dist_dir + "*.*")
    if os.name == "nt":
        exedir = "C:/Programs/tofrodos/"
        if to_dos:
            call_list = [exedir + "todos"] + files
        else:
            call_list = [exedir + "fromdos"] + files
    else:
        if to_dos:
            call_list = ["todos"] + files
        else:
            call_list = ["fromdos"] + files

    # call the conversion program
    try:
        subprocess.check_call(call_list)
    except subprocess.CalledProcessError as err:
        libastylewx.system_exit("Bad tofro return: " + str(err.returncode))
    except OSError:
        libastylewx.system_exit("Cannot find executable: " + call_list[0])

# -----------------------------------------------------------------------------

def copy_astylewx_doc(dist_doc, to_dos=False):
    """Copy astylewx doc directory to a distribution directory.
    """
    print("copying doc")
    deleted = 0
    docfiles = glob.glob(__astylewx_dir + "/doc/*")
    for filepath in docfiles:
        sep = filepath.rfind(os.sep)
        filename = filepath[sep + 1:]
        if (filename == "index.html"
                or filename == "install.html"
                or filename == "static.html"
                or filename == "styles.css"):
            shutil.copy(filepath, dist_doc)
            print("    " + filename)
        else:
            deleted += 1
    convert_line_ends(dist_doc, to_dos)
    # verify copy - had a problem with bad filenames
    distfiles = (glob.glob(dist_doc + "/*.html")
                 + glob.glob(dist_doc + "/*.css"))
    if len(distfiles) != len(docfiles) - deleted:
        libastylewx.system_exit("Error copying doc: " + str(len(distfiles)))
    # change file permissions
    for srcfile in distfiles:
        # read/write by the owner and read only by everyone else (-rw-r--r--)
        mode = (stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IROTH)
        os.chmod(srcfile, mode)

# -----------------------------------------------------------------------------

def copy_astylewx_dialog(dist_dialog, to_dos=False):
    """Copy astylewx dialog directory to a distribution directory.
    """
    print("copying dialog")
    dialogfiles = glob.glob(__astylewx_dir + "/dialog/*")
    for dialogpath in dialogfiles:
        shutil.copy(dialogpath, dist_dialog)
    convert_line_ends(dist_dialog, to_dos)
    # verify copy - had a problem with bad filenames
    distfiles = (glob.glob(dist_dialog + "/*.*"))
    if len(distfiles) != len(dialogfiles):
        libastylewx.system_exit("Error copying dialog: " + str(len(distfiles)))
    # change file permissions
    for dialogfile in distfiles:
        # read/write by the owner and read only by everyone else (-rw-r--r--)
        mode = (stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IROTH)
        os.chmod(dialogfile, mode)

# -----------------------------------------------------------------------------

def copy_astylewx_python_files(dist_file):
    """Copy astylewxtest python files to a distribution directory.
       Copied from astylewxtest, not astylewx.
    """
    print("copying file-py")
    pythonfiles = glob.glob(__astylewxtest_dir + "/file-py/*")
    files_copied = 0
    for pythonpath in pythonfiles:
        if not os.path.isfile(pythonpath):
            continue
        sep = pythonpath.rfind(os.sep)
        filename = pythonpath[sep + 1:]
        if (pythonpath.endswith("change_static_wx30.py")
                or pythonpath.endswith("change_static_wx31.py")
                or pythonpath.endswith("libastylewx.py")
                or pythonpath.endswith("to_xxbook.py")
                or pythonpath.endswith("xpm_fix.py")):
            files_copied += 1
            shutil.copy(pythonpath, dist_file)
            print("    " + filename)
    # verify number of files copied (from AStyleWxTest)
    if files_copied != 5:
        libastylewx.system_exit("Error in number of python files copied: " + str(files_copied))
    # verify copy - had a problem with bad filenames
    distfiles = (glob.glob(dist_file + "/*"))
    if len(distfiles) != files_copied:
        libastylewx.system_exit("Error copying python files: " + str(len(distfiles)))
    # change file permissions
    for pythonfile in distfiles:
        # read/write by the owner and read only by everyone else (-rw-r--r--)
        mode = (stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IROTH)
        os.chmod(pythonfile, mode)

# -----------------------------------------------------------------------------

def copy_astylewx_image(dist_image):
    """Copy astylewx image directory to a distribution directory.
    """
    print("copying image")
    imagefiles = glob.glob(__astylewx_dir + "/image/*")
    for imagepath in imagefiles:
        shutil.copy(imagepath, dist_image)
    # verify copy - had a problem with bad filenames
    distfiles = (glob.glob(dist_image + "/*.*"))
    if len(distfiles) != len(imagefiles):
        libastylewx.system_exit("Error copying image: " + str(len(distfiles)))
    # change file permissions
    for imagefile in distfiles:
        # read/write by the owner and read only by everyone else (-rw-r--r--)
        mode = (stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IROTH)
        os.chmod(imagefile, mode)

# -----------------------------------------------------------------------------

def copy_astylewx_src(dist_src, to_dos=False):
    """Copy astylewx src directory to a distribution directory.
    """
    print("copying src")
    srcfiles = glob.glob(__astylewx_dir + "/src/*")
    for srcpath in srcfiles:
        shutil.copy(srcpath, dist_src)
    convert_line_ends(dist_src, to_dos)
    # verify copy - had a problem with bad filenames
    distfiles = (glob.glob(dist_src + "/*.cpp")
                 + glob.glob(dist_src + "/*.h")
                 + glob.glob(dist_src + "/*.rc"))
    if len(distfiles) != len(srcfiles):
        libastylewx.system_exit("Error copying src: " + str(len(distfiles)))
    # change file permissions
    for srcfile in distfiles:
        # read/write by the owner and read only by everyone else (-rw-r--r--)
        mode = (stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IROTH)
        os.chmod(srcfile, mode)

# -----------------------------------------------------------------------------

def copy_astylewx_top(dist_top, to_dos=False):
    """Copy astylewx top directory to a distribution directory.
    """
    print("copying top")
    deleted = 0
    docfiles = glob.glob(__astylewx_dir + "/*")
    for filepath in docfiles:
        sep = filepath.rfind(os.sep)
        filename = filepath[sep + 1:]
        if (filename == "LICENSE.txt"
                or filename == "README.txt"):
            shutil.copy(filepath, dist_top)
            print("    " + filename)
        else:
            deleted += 1
    convert_line_ends(dist_top, to_dos)
    # verify copy - had a problem with bad filenames
    distfiles = (glob.glob(dist_top + "/*.txt"))
    if len(distfiles) != len(docfiles) - deleted:
        libastylewx.system_exit("Error copying top: " + str(len(distfiles)))
    # change file permissions
    for srcfile in distfiles:
        # read/write by the owner and read only by everyone else (-rw-r--r--)
        mode = (stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IROTH)
        os.chmod(srcfile, mode)

# -----------------------------------------------------------------------------

def copy_linux_build_directories(dist_build):
    """Copy the Linux build directories to the distribution directory.
    """
    print("copying build")
    # permissions = read/write by the owner and read only by everyone else
    mode = (stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IROTH)

    # build/clang directory
    print("    clang")
    astylewx_build_clang = __astylewx_dir + "/build/clang/"
    dist_build_clang = dist_build + "/clang/"
    os.makedirs(dist_build_clang)
    files_copied = 0
    for buildfile in ["Makefile", "deps.mak"]:
        files_copied += 1
        make_path_clang = astylewx_build_clang + buildfile
        shutil.copy(make_path_clang, dist_build_clang)
        os.chmod(make_path_clang, mode)
    # verify number of files copied
    if files_copied != 2:
        libastylewx.system_exit("Error in number of clang build files copied: " + str(files_copied))

    # build/gcc directory
    print("    gcc")
    astylewx_build_gcc = __astylewx_dir + "/build/gcc/"
    dist_build_gcc = dist_build + "/gcc/"
    os.makedirs(dist_build_gcc)
    files_copied = 0
    for buildfile in ["Makefile", "deps.mak"]:
        files_copied += 1
        make_path_gcc = astylewx_build_gcc + buildfile
        shutil.copy(make_path_gcc, dist_build_gcc)
        os.chmod(make_path_gcc, mode)
    # verify number of files copied
    if files_copied != 2:
        libastylewx.system_exit("Error in number of gcc build files copied: " + str(files_copied))

    # build/intel directory
    print("    intel")
    astylewx_build_intel = __astylewx_dir + "/build/intel/"
    dist_build_intel = dist_build + "/intel/"
    os.makedirs(dist_build_intel)
    files_copied = 0
    for buildfile in ["Makefile", "deps.mak"]:
        files_copied += 1
        make_path_intel = astylewx_build_intel + buildfile
        shutil.copy(make_path_intel, dist_build_intel)
        os.chmod(make_path_intel, mode)
    # verify number of files copied
    if files_copied != 2:
        libastylewx.system_exit("Error in number of intel build files copied: " + str(files_copied))

# -----------------------------------------------------------------------------

def copy_mac_build_directories(dist_build):
    """Copy the Mac build directories to the distribution directory.
    """
    print("copying build")
    # permissions = read/write by the owner and read only by everyone else
    mode = (stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IROTH)

    # build/mac directory
    print("    mac")
    astylewx_build_mac = __astylewx_dir + "/build/mac/"
    dist_build_mac = dist_build + "/mac/"
    os.makedirs(dist_build_mac)
    for buildfile in ["Makefile", "deps.mak"]:
        make_path_mac = astylewx_build_mac + buildfile
        shutil.copy(make_path_mac, dist_build_mac)
        os.chmod(make_path_mac, mode)

    # build/xcode directory
    print("    xcode")
    astylewx_build_xcode = __astylewx_dir + "/build/xcode/"
    dist_build_xcode = dist_build + "/xcode/"
    shutil.copytree(astylewx_build_xcode, dist_build_xcode)
    # permissions = read/write by the owner and read only by everyone else
    mode = (stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IROTH)
    for file_in in ("/AStyleWx.xcodeproj/project.pbxproj",
                    "/AStyleWxDy.xcodeproj/project.pbxproj"):
        os.chmod(dist_build_xcode + file_in, mode)

#	for file_in in ("/install.sh",
#			        "/uninstall.sh"):
#		os.chmod(dist_build_xcode + file_in, mode)

# -----------------------------------------------------------------------------

def copy_windows_build_directories(dist_build):
    """Copy the build/vs20xx directories to the distribution directory.
    """
    print("copying build")
    buildfiles = __astylewx_dir + "/build"
    # get a list of build/vs20xx directories
    build_dir_list = os.listdir(buildfiles)
    build_dir_list.sort()
    for unused, build_dir in enumerate(build_dir_list):
        if (build_dir[:4] == "vs20"
            and not build_dir.endswith("-clang")):
            print("    " + build_dir)

            # copy solution and properties files
            vsdir = '/' + build_dir + '/'
            dist_astylewx_vs20xx = dist_build + vsdir
            os.mkdir(dist_astylewx_vs20xx)
            slnfiles = glob.glob(buildfiles + vsdir + "*.sln")
            for sln in slnfiles:
                shutil.copy(sln, dist_astylewx_vs20xx)
            propsfiles = glob.glob(buildfiles + vsdir + "*.props")
            for props in propsfiles:
                shutil.copy(props, dist_astylewx_vs20xx)

            # build project directories
            for projdir in ("/AStyle Dll/",
                            "/AStyle Lib/",
                            "/AStyleWx/",
                            "/AStyleWxDll/"):
                dist_astylewx_proj = dist_astylewx_vs20xx[:-1] + projdir
                os.mkdir(dist_astylewx_proj)

                # copy project files
                projfiles = glob.glob(buildfiles + vsdir[:-1] + projdir + "*.*proj")
                files_copied = 0
                for proj in projfiles:
                    files_copied += 1
                    shutil.copy(proj, dist_astylewx_proj)
                filtfiles = glob.glob(buildfiles + vsdir[:-1] + projdir + "*.*.filters")
                for filter_in in filtfiles:
                    files_copied += 1
                    shutil.copy(filter_in, dist_astylewx_proj)
                # verify number of files copied
                if files_copied != 2:
                    libastylewx.system_exit("Error in number of build files copied: " + str(files_copied))

# -----------------------------------------------------------------------------

def extract_astyle_build_dirs_linux(dist_build):
    """Extract astyle Linux build directories to the distribution directory.
    """
    print("extracting build")
    # permissions = read/write by the owner and read only by everyone else
    mode = (stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IROTH)

    # build/clang directory
    print("    clang")
    astyle_build_clang = __astyle_dir + "/build/clang/"
    dist_build_clang = dist_build + "/clang/"
    os.makedirs(dist_build_clang)
    for buildfile in ["Makefile"]:
        make_path_clang = astyle_build_clang + buildfile
        shutil.copy(make_path_clang, dist_build_clang)
        os.chmod(make_path_clang, mode)

    # build/gcc directory
    print("    gcc")
    astylewx_build_gcc = __astyle_dir + "/build/gcc/"
    dist_build_gcc = dist_build + "/gcc/"
    os.makedirs(dist_build_gcc)
    for buildfile in ["Makefile"]:
        make_path_gcc = astylewx_build_gcc + buildfile
        shutil.copy(make_path_gcc, dist_build_gcc)
        os.chmod(make_path_gcc, mode)

    # build/intel directory
    print("    intel")
    astylewx_build_intel = __astyle_dir + "/build/intel/"
    dist_build_intel = dist_build + "/intel/"
    os.makedirs(dist_build_intel)
    for buildfile in ["Makefile"]:
        make_path_intel = astylewx_build_intel + buildfile
        shutil.copy(make_path_intel, dist_build_intel)
        os.chmod(make_path_intel, mode)

# -----------------------------------------------------------------------------

def extract_astyle_build_dirs_mac(dist_build):
    """Extract astyle Mac build directories to the distribution directory.
    """
    print("extracting build")
    # permissions = read/write by the owner and read only by everyone else
    mode = (stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IROTH)

    # build/clang directory
    print("    clang")
    astyle_build_clang = __astyle_dir + "/build/clang/"
    dist_build_clang = dist_build + "/clang/"
    os.makedirs(dist_build_clang)
    for buildfile in ["Makefile"]:
        make_path_clang = astyle_build_clang + buildfile
        shutil.copy(make_path_clang, dist_build_clang)
        os.chmod(make_path_clang, mode)

    # build/gcc directory
    print("    gcc")
    astylewx_build_gcc = __astyle_dir + "/build/gcc/"
    dist_build_gcc = dist_build + "/gcc/"
    os.makedirs(dist_build_gcc)
    for buildfile in ["Makefile"]:
        make_path_gcc = astylewx_build_gcc + buildfile
        shutil.copy(make_path_gcc, dist_build_gcc)
        os.chmod(make_path_gcc, mode)

    # build/intel directory
    print("    intel")
    astylewx_build_intel = __astyle_dir + "/build/intel/"
    dist_build_intel = dist_build + "/intel/"
    os.makedirs(dist_build_intel)
    for buildfile in ["Makefile"]:
        make_path_intel = astylewx_build_intel + buildfile
        shutil.copy(make_path_intel, dist_build_intel)
        os.chmod(make_path_intel, mode)

# -----------------------------------------------------------------------------

def extract_astyle_top(dist_top, to_dos=False):
    """Extract astyle top directory to a distribution directory.
    """
    print("extracting top")
    deleted = 0
    docfiles = glob.glob(__astylewx_dir + "/*")
    for filepath in docfiles:
        sep = filepath.rfind(os.sep)
        filename = filepath[sep + 1:]
        if filename == "LICENSE.txt":
            shutil.copy(filepath, dist_top)
            print("    " + filename)
        else:
            deleted += 1
    convert_line_ends(dist_top, to_dos)
    # verify copy - had a problem with bad filenames
    distfiles = (glob.glob(dist_top + "/*.txt"))
    if len(distfiles) != len(docfiles) - deleted:
        libastylewx.system_exit("Error copying top: " + str(len(distfiles)))
    # change file permissions
    for srcfile in distfiles:
        # read/write by the owner and read only by everyone else (-rw-r--r--)
        mode = (stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IROTH)
        os.chmod(srcfile, mode)

# -----------------------------------------------------------------------------

def extract_astyle_src(dist_src, to_dos=False):
    """Extract astyle src directory to a distribution directory.
    """
    print("extracting src")
    srcfiles = glob.glob(__astyle_dir + "/src/*")
    for srcpath in srcfiles:
        shutil.copy(srcpath, dist_src)
    convert_line_ends(dist_src, to_dos)
    # verify copy - had a problem with bad filenames
    distfiles = (glob.glob(dist_src + "/*.cpp")
                 + glob.glob(dist_src + "/*.h")
                 + glob.glob(dist_src + "/*.rc"))
    if len(distfiles) != len(srcfiles):
        libastylewx.system_exit("Error copying src: " + str(len(distfiles)))
    # change file permissions
    for srcfile in distfiles:
        # read/write by the owner and read only by everyone else (-rw-r--r--)
        mode = (stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IROTH)
        os.chmod(srcfile, mode)

# -----------------------------------------------------------------------------

def extract_linux_astyle():
    """Extract the required astyle files to the linux directory.
    """
    print("\nEXTRACTING ASTYLE")
    dist_base = get_distribution_folder_linux()
    dist_astyle = dist_base + "/astylewx_{0}_linux".format(AS_RELEASE) + "/astyle"
    os.makedirs(dist_astyle)

    # top directory
    dist_top = dist_astyle + "/"
    extract_astyle_top(dist_top)

    # src directory
    dist_src = dist_astyle + "/src/"
    os.mkdir(dist_src)
    extract_astyle_src(dist_src)

# -----------------------------------------------------------------------------

def extract_mac_astyle():
    """Extract the required astyle files to the mac directory.
    """
    print("\nEXTRACTING ASTYLE")
    dist_base = get_distribution_folder_mac()
    dist_astyle = dist_base + "/astylewx_{0}_macos".format(AS_RELEASE) + "/astyle"
    os.makedirs(dist_astyle)

    # top directory
    dist_top = dist_astyle + "/"
    extract_astyle_top(dist_top)

    # src directory
    dist_src = dist_astyle + "/src/"
    os.mkdir(dist_src)
    extract_astyle_src(dist_src)

# -----------------------------------------------------------------------------

def extract_windows_astyle():
    """Extract the required astyle files to the windows directory.
    """
    print("\nEXTRACTING ASTYLE")
    dist_base = get_distribution_folder_windows()
    dist_astyle = dist_base + "/AStyleWx_{0}_windows".format(AS_RELEASE) + "/AStyle"
    os.makedirs(dist_astyle)

    # top directory
    dist_top = dist_astyle + "/"
    extract_astyle_top(dist_top, True)

    # src directory
    dist_src = dist_astyle + "/src/"
    os.mkdir(dist_src)
    extract_astyle_src(dist_src, True)

# -----------------------------------------------------------------------------

def get_distribution_folder_linux():
    """Get the distribution folder name for linux
    """
    dist_base = __base_dir + "/DistLinuxWxXP"
    return dist_base

# -----------------------------------------------------------------------------

def get_distribution_folder_mac():
    """Get the distribution folder name for mac
    """
    dist_base = __base_dir + "/DistMacWxXP"
    return dist_base

# -----------------------------------------------------------------------------

def get_distribution_folder_windows():
    """Get the distribution folder name for windows
    """
    dist_base = __base_dir + "/DistWindowsWxXP"
    return dist_base

# -----------------------------------------------------------------------------

def remove_dist_directories():
    """Remove directories from a previous run.
    """
    dirs = glob.glob(__base_dir + "/[Dd]ist*/")
    dirs.sort()
    for directory in dirs:
        if not directory[:-1].lower().endswith("wxxp"):
            continue
        directory = directory.replace('\\', '/')
        print("remove " + directory)
        # remove the directory - this is a problem with Windows only
        imax = 5
        for i in range(0, imax):
            shutil.rmtree(directory, True)
            if not os.path.isdir(directory):
                break
            if i == imax - 1:
                libastylewx.system_exit("Directory not removed: " + directory)
            time.sleep(2)

# -----------------------------------------------------------------------------

# make the module executable
if __name__ == "__main__":
    main()
    libastylewx.system_exit()

# -----------------------------------------------------------------------------
