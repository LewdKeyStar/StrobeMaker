import flet as ft

WIDTHS = {"landscape": 1920, "portrait": 1080, "square": 1080}
HEIGHTS = {"landscape": 1080, "portrait": 1920, "square": 1080}

class OrientationPicker(ft.Row):
    def __init__(
        self, page, options,

        *,

        user_on_change
    ):

        self.page = page
        self.options = options

        self.landscape_button = ft.IconButton(
            icon = ft.icons.CROP_LANDSCAPE,

            on_click = lambda _ : self.set_orientation("landscape")
        )

        self.portrait_button = ft.IconButton(
            icon = ft.icons.CROP_PORTRAIT,

            on_click = lambda _ : self.set_orientation("portrait")
        )

        self.square_button = ft.IconButton(
            icon = ft.icons.CROP_SQUARE,

            on_click = lambda _ : self.set_orientation("square")
        )

        self.user_on_change = user_on_change

        super().__init__(
            [
                self.landscape_button,
                self.portrait_button,
                self.square_button
            ]
        )

    def set_orientation(self, orientation):
        self.options.resolution_width = WIDTHS[orientation]
        self.options.resolution_height = HEIGHTS[orientation]
        self.user_on_change(None)
