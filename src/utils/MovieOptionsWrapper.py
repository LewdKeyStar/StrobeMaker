import flet as ft

from dataclasses import dataclass
from copy import copy # replace() is not available in Python 3.10

from business.MovieOptions import MovieOptions

from utils.debounce import debounce

DEBOUNCE_TIME = 0.5

@dataclass
class MovieOptionsWrapper(MovieOptions):

    page: ft.Page = None

    auto_font_size: bool = True

    preview_no_update_keys = [
        "output_path"
    ]

    preview_no_update_keys_if_true = [
        "auto_font_size"
    ]

    font_size_update_keys = [ # Can't use list type annotation in dataclass, fuck's sake
        'auto_font_size', # Technically this means we set the auto font size again upon disabling it, but it's basically undetectable
        'font',
        'resolution_width',
        'resolution_height',
        'text_border',
        'capitalize_all'
    ]


    def __init__(self, page):
        self.page = page
        super().__init__()

    def __setattr__(self, name, value):
        super().__setattr__(name, value)

        if name in self.font_size_update_keys:
            self.send_font_size_message()

        # More concise way to do this ?
        if name not in self.preview_no_update_keys \
            and (name not in self.preview_no_update_keys_if_true or getattr(self, name) is True):
            self.send_preview_message()

    def wrap(self, func, *args):
        if self.auto_font_size:
            self.send_font_size_message()

        self.send_preview_message()

        return func(*args)

    def clone(self, new_vals):
        # replace() is not available in Python 3.10
        copied = copy(self)
        for key in new_vals:
            setattr(copied, key, new_vals[key])
        return copied

    @debounce(DEBOUNCE_TIME)
    def send_preview_message(self):
        self.page.pubsub.send_all_on_topic("preview", "Update preview")

    @debounce(DEBOUNCE_TIME)
    def send_font_size_message(self):
        self.page.pubsub.send_all_on_topic("font_size", "Update font size")
