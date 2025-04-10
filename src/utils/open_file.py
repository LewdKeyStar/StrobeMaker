import os, sys, subprocess

# Workaround for the fact that os.startfile is only available on Windows.
# Lifted from : https://stackoverflow.com/questions/17317219/is-there-an-platform-independent-equivalent-of-os-startfile

def open_file(filename):
    if sys.platform == "win32":
        os.startfile(filename)
    else:
        opener = "open" if sys.platform == "darwin" else "xdg-open"
        subprocess.Popen([opener, filename]) # the OG snippet used call() but we want to detach the subprocess
