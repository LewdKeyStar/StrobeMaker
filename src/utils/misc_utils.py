# Circumvent FilePicker not enforcing its provided extensions
# In an ideal world, I would just override FilePicke.save_file(),
# However, while that function is, obviously, asynchronous in opening of the file explorer dialog,
# It provides no async interface with which to properly wait for that dialog to close.
# In other words : an override completes before the dialog is actually closed,
# And there's no way to wait for it.

def add_extension_if_missing(path, ext):
    true_ext = '.' + ext
    return path if path.endswith(true_ext) else path + true_ext
