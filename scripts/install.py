import os
import tarfile
import tempfile
from urllib.request import urlopen
from labutil.utils import err, run_cmd


# Define list of available things to install

available = {
    'keyd': {
        'version': "2.4.3",
        'url': "https://github.com/rvaiya/keyd/archive/refs/tags/v{0}.tar.gz",
        'build_cmds': [
            ['make'],
            ['sudo', 'make', 'install'],
            ['sudo', 'systemctl', 'enable', 'keyd.service'],
            ['sudo', 'systemctl', 'start', 'keyd.service'],
        ]
    },
}


# Define some utility functions

def fetch_source(liburl):
    """Downloads and decompresses the source code for a given library.
    """
    # Download tarfile to temporary folder
    srctar = urlopen(liburl)
    srcfile = liburl.split("/")[-1]
    tmpdir = tempfile.mkdtemp(suffix="labutil")
    outpath = os.path.join(tmpdir, srcfile)
    with open(outpath, 'wb') as out:
        out.write(srctar.read())

    # Extract source from archive
    with tarfile.open(outpath, 'r:gz') as z:
        z.extractall(path=tmpdir)

    return os.path.join(tmpdir, srcfile.replace(".tar.gz", ""))


def install_from_source(name, silent=False):
    # Download and extract source code
    info = available[name]
    if not silent:
        print("\n=== Downloading {0} {1} ===".format(name, info['version']))
    srcdir = fetch_source(info['url'].format(info['version']))

    # Enter source directory and build/install the library
    os.chdir(srcdir)
    if not silent:
        print("\n=== Building {0} {1} from source ===\n".format(name, info['version']))
    for cmd in info['build_cmds']:
        p = sub.Popen(cmd, stdout=sys.stdout, stderr=sys.stderr)
        p.communicate()
        if p.returncode != 0:
            success = False
            break


# Actually run build script

def labutil_install(libname):
    if not libname in available.keys():
        e = "install.py is not configured to install '{0}'"
        raise RuntimeError(e.format(libname))

    # Download and extract source code
    info = available[libname]
    srcdir = fetch_source(info['url'].format(info['version']))

    # Enter source directory and build/install the library
    os.chdir(srcdir)
    print("\n=== Building {0} {1} from source ===\n".format(libname, info['version']))
    for cmd in info['build_cmds']:
        p = sub.Popen(cmd, stdout=sys.stdout, stderr=sys.stderr)
        p.communicate()
        if p.returncode != 0:
            success = False
            break


if __name__ == "__main__":
    libname = sys.argv[1]
    labutil_install(libname)
