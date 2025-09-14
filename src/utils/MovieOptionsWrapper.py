import flet as ft

from dataclasses import dataclass
from copy import copy # replace() is not available in Python 3.10

from business.MovieOptions import MovieOptions

from utils.debounce import debounce

DEBOUNCE_TIME = 0.5

@dataclass
class MovieOptionsWrapper(MovieOptions):

    page: ft.Page = None

    def __init__(self, page):
        self.page = page
        super().__init__()

    def __setattr__(self, name, value):
        super().__setattr__(name, value)

        if name != "output_path": # TODO : maybe have a list of non-update-worthy properties
            self.send_message_debounced()

    def wrap(self, func, *args):
        self.send_message_debounced()
        return func(*args)

    def clone(self, new_vals):
        # replace() is not available in Python 3.10
        copied = copy(self)
        for key in new_vals:
            setattr(copied, key, new_vals[key])
        return copied

    @debounce(DEBOUNCE_TIME)
    def send_message_debounced(self):
        self.page.pubsub.send_all_on_topic("preview", "Update preview")
