import flet as ft

from business.Movie import Movie

from constants import PREVIEW_PATH

class VideoPreview(ft.Video):

    def __init__(self, script_field, options):
        self.script_field = script_field # it's so clunky having to carry the control around...
        # how about refs to non-UI objects, like in any modern framework ??
        self.options = options

        super().__init__(playlist = [])

    def update_preview(self):
        if len(self.playlist) == 0:
            return

        self.playlist_remove(0)
        Movie(self.script_field.value, self.options.clone({output_path: PREVIEW_PATH})).create_movie()
        self.playlist_add(ft.VideoMedia(PREVIEW_PATH))
