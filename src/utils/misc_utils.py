def add_extension_if_missing(path, ext):
    true_ext = '.' + ext
    return path if path.endswith(true_ext) else path + true_ext
