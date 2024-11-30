import flet as ft

from asyncio import Lock
from shutil import rmtree
from os.path import dirname

from business.Movie import Movie

from constants import PREVIEW_PATH

class VideoPreview(ft.Video):

    def __init__(self, script_field, page, options):
        self.script_field = script_field # it's so clunky having to carry the control around...
        # how about refs to non-UI objects, like in any modern framework ??
        self.page = page
        self.options = options

        self.lock = Lock() # Avoid overstepping on successive preview updates

        self.is_added = False # Necessary because the jump_to hack only works after add

        super().__init__(
            autoplay = False,
            playlist = [ft.VideoMedia(PREVIEW_PATH)],
            aspect_ratio = 16/9
        )

    async def update_preview(self, override_script_val = None):

        script = \
            self.script_field.value.split('\n')[0] if override_script_val is None \
            else override_script_val

        async with self.lock:
            Movie(
                [script],
                self.options.clone({'output_path': PREVIEW_PATH})
            ).create_movie(fast = True)

        if self.is_added:
            # We can't just update the playlist, because for some reason, playlist_add() is busted.
            # So instead, we do this :

            self.jump_to(0) # This forces the component to actually update its video content
            self.pause() # Prevent autoplay on jump, which does still happen despite autoplay = False
            # (But the play icon still changes...)

        if self.page is not None:
            self.page.update()
