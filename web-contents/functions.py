import os
import shlex
import subprocess


def escape_os_path(path):
    tmp = r""
    for s in path:
        if s in r' \%$':
            tmp += r'\%c' % s
        else:
            tmp += s
    return tmp


def exec_oe(cmd):
    process = subprocess.Popen(
        shlex.split(cmd), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = process.communicate()
    return (process.returncode, out, err)


def get_real_svn_location(path):
    if path.startswith("/svn-us"):
        return "http://web-repository/%s" % path[8:]
    elif path.startswith("/svn-eu"):
        return "http://svn.eu/%s" % path[8:]
    elif path.startswith("/svn-cn"):
        return "http://webcn-repo/%s" % path[8:]
    elif path.startswith("/svn-kr"):
        return "http://kr-repository/%s" % path[8:]
    elif path.startswith("/billing"):
        return "http://billing-repository/%s" % path[9:]
    else:
        # fallback to the us one
        return "http://web-repository/%s" % path[8:]
    return None


def export_var(name, value):
    os.environ[name] = value
