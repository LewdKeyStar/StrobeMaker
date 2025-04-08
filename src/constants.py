import os.path as ospath

from matplotlib import font_manager

ROOT_PROJECT_DIR = ospath.dirname(ospath.dirname(__file__))

ASSETS_PATH = ospath.join(ROOT_PROJECT_DIR, "assets")
DEFAULT_OUTPUT_PATH = ospath.join(ROOT_PROJECT_DIR, "output")
PREVIEW_PATH = ospath.join(ROOT_PROJECT_DIR, '.preview', 'preview.mp4')

DEFAULT_FONT_LABEL = "Default (Helvetica Neue)"
DEFAULT_FONT_NAME = "HelveticaNeue"
FONT_LIST = sorted(font_manager.findSystemFonts(fontext = 'ttf'))

APP_TITLE = "StrobeMaker"
