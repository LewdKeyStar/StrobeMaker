import os.path as ospath

ROOT_PROJECT_DIR = ospath.dirname(ospath.dirname(__file__))

ASSETS_PATH = ospath.join(ROOT_PROJECT_DIR, "assets")
TEMP_OUTPUT_PATH = ospath.join(ROOT_PROJECT_DIR, ".tmp")
DEFAULT_OUTPUT_PATH = ospath.join(ROOT_PROJECT_DIR, "output")
PREVIEW_PATH = ospath.join(ROOT_PROJECT_DIR, '.preview', 'preview.mp4')
