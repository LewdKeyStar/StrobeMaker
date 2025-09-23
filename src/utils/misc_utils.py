# Circumvent FilePicker not enforcing its provided extensions
# In an ideal world, I would just override FilePicke.save_file(),
# However, while that function is, obviously, asynchronous in opening of the file explorer dialog,
# It provides no async interface with which to properly wait for that dialog to close.
# In other words : an override completes before the dialog is actually closed,
# And there's no way to wait for it.

def add_extension_if_missing(path, ext):
    true_ext = '.' + ext
    return path if path.endswith(true_ext) else path + true_ext

def has_method(instance, method_name):
    return hasattr(instance, method_name) \
    and callable(getattr(instance, method_name))

# Taken from https://github.com/kkroening/ffmpeg-python/blob/master/examples/show_progress.py#L8

from contextlib import contextmanager
from tempfile import mkdtemp
from shutil import rmtree

@contextmanager
def _tmpdir_scope():
    tmpdir = mkdtemp()
    try:
        yield tmpdir
    finally:
        rmtree(tmpdir)
