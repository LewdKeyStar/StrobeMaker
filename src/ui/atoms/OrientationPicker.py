import flet as ft

orientations = ["landscape", "portrait", "square"]

DEFAULT_ASPECT_RATIO_MULT = 0.5625

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
            icon_color = ft.colors.GREY_600,
            selected_icon = ft.icons.CROP_LANDSCAPE,
            selected_icon_color = ft.colors.BLUE_200,

            selected = True,

            on_click = lambda _ : self.set_orientation("landscape")
        )

        self.portrait_button = ft.IconButton(
            icon = ft.icons.CROP_PORTRAIT,
            icon_color = ft.colors.GREY_600,
            selected_icon = ft.icons.CROP_PORTRAIT,
            selected_icon_color = ft.colors.BLUE_200,

            selected = False,

            on_click = lambda _ : self.set_orientation("portrait")
        )

        self.square_button = ft.IconButton(
            icon = ft.icons.CROP_SQUARE,
            icon_color = ft.colors.GREY_600,
            selected_icon = ft.icons.CROP_SQUARE,
            selected_icon_color = ft.colors.BLUE_200,

            selected = False,

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

        getattr(self, f"{orientation}_button").selected = True

        for other_orientation in [ \
            other_orientation for other_orientation in orientations if other_orientation != orientation \
        ] :
            getattr(self, f"{other_orientation}_button").selected = False

        larger_dimension = max(self.options.resolution_width, self.options.resolution_height)
        smaller_dimension = min(self.options.resolution_width, self.options.resolution_height)

        if smaller_dimension == larger_dimension:
            smaller_dimension = int(DEFAULT_ASPECT_RATIO_MULT * larger_dimension)

        if orientation == "landscape":
            self.options.resolution_width = larger_dimension
            self.options.resolution_height = smaller_dimension

        elif orientation == "portrait":
            self.options.resolution_width = smaller_dimension
            self.options.resolution_height = larger_dimension

        else:
            self.options.resolution_width = larger_dimension
            self.options.resolution_height = larger_dimension

        self.user_on_change(None)
