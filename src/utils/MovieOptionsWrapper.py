import flet as ft

from dataclasses import dataclass

from business.MovieOptions import MovieOptions

from utils.debounce import debounce

DEBOUNCE_TIME = 0.1

# This class is used to trigger video preview updates on option changes.
# However, due to the Video control apparently not working on my system
# (see #10),
# it goes unused so far.

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
        cloned_dict = self.__dict__

        del cloned_dict['page']

        cloned_dict.update(new_vals)

        return MovieOptions(**cloned_dict)

    @debounce(DEBOUNCE_TIME)
    def send_message_debounced(self):
        self.page.pubsub.send_all("Update preview")
