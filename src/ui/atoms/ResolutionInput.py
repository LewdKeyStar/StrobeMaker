import flet as ft

from ui.atoms.NumberInput import NumberInput

INPUT_WIDTH = 150

LOWRES_WIDTH = 256
LOWRES_HEIGHT = 144
HIGHRES_WIDTH = 3840
HIGHRES_HEIGHT = 2160

UNIT_TEXT_SIZE = 16 # ugly duplication from VideoSection

class ResolutionInput(ft.Column):

    def __init__(
        self,
        page,
        options,

        *,

        user_on_change
    ):

        self.page = page
        self.options = options

        self.resolution_width_input = NumberInput(
            self.page,
            self.options,
            "resolution_width",

            min = LOWRES_WIDTH,
            max = HIGHRES_WIDTH,

            width = INPUT_WIDTH,

            user_on_change = lambda e : self.update_resolution(e)
        )

        self.resolution_height_input = NumberInput(
            self.page,
            self.options,
            "resolution_height",

            min = LOWRES_HEIGHT,
            max = HIGHRES_HEIGHT,

            width = INPUT_WIDTH,

            user_on_change = lambda e : self.update_resolution(e)
        )

        self.save_video_aspect_ratio()

        self.aspect_ratio_lock_toggle = ft.IconButton(
            icon = ft.icons.LINK_OFF,
            icon_color = ft.colors.GREY_600,

            selected_icon = ft.icons.LINK,
            selected_icon_color = ft.colors.BLUE_200,

            selected = True,

            on_click = lambda _ : self.toggle_aspect_ratio_lock()
        )

        self.line_canvas_paint_enabled = ft.Paint(
            stroke_width = 2,
            color = ft.colors.BLUE_100,
            style = ft.PaintingStyle.STROKE
        )

        self.line_canvas_paint_disabled = ft.Paint(
            stroke_width = 1,
            color = ft.colors.GREY_800,
            style = ft.PaintingStyle.STROKE
        )

        self.decorative_canvas_left = ft.canvas.Canvas(
            [
                ft.canvas.Path(
                    [
                        ft.canvas.Path.MoveTo(10, 0),
                        ft.canvas.Path.LineTo(-50, 0),
                        ft.canvas.Path.LineTo(-50, -15)
                    ],

                    paint = self.line_canvas_paint_enabled,
                )
            ]
        )

        self.decorative_canvas_right = ft.canvas.Canvas(
            [
                ft.canvas.Path(
                    [
                        ft.canvas.Path.MoveTo(-10, 0),
                        ft.canvas.Path.LineTo(50, 0),
                        ft.canvas.Path.LineTo(50, -15)
                    ],

                    paint = self.line_canvas_paint_enabled
                )
            ]
        )

        self.aspect_ratio_locked = True

        super().__init__(
            [
                ft.Container(
                    content = ft.Row(
                        [
                            self.resolution_width_input,
                            ft.Text("x", size = UNIT_TEXT_SIZE),
                            self.resolution_height_input,
                            ft.Text("px", size = UNIT_TEXT_SIZE)
                        ]
                    ),

                    padding = ft.padding.only(left = 26) # align with link button and OrientationPicker
                ),

                ft.Row(
                    [
                        self.decorative_canvas_left,
                        self.aspect_ratio_lock_toggle,
                        self.decorative_canvas_right
                    ]
                )
            ],

            horizontal_alignment = ft.CrossAxisAlignment.CENTER,
            spacing = 5
        )

        self.user_on_change = user_on_change

    @property
    def canvas_paint(self):
        return self.line_canvas_paint_enabled if self.aspect_ratio_locked else self.line_canvas_paint_disabled

    def save_video_aspect_ratio(self):
        self.video_aspect_ratio = self.options.resolution_width / self.options.resolution_height

    def toggle_aspect_ratio_lock(self):
        self.aspect_ratio_locked = not self.aspect_ratio_locked

        if self.aspect_ratio_locked:
            self.save_video_aspect_ratio()

        self.aspect_ratio_lock_toggle.selected = self.aspect_ratio_locked
        self.aspect_ratio_lock_toggle.update()

        self.decorative_canvas_left.shapes[0].paint = self.canvas_paint
        self.decorative_canvas_left.update()

        self.decorative_canvas_right.shapes[0].paint = self.canvas_paint
        self.decorative_canvas_right.update()


    def update_resolution(self, e):

        if self.aspect_ratio_locked:

            control_to_update = \
                self.resolution_width_input if e.control == self.resolution_height_input \
                else self.resolution_height_input

            mult = \
                self.video_aspect_ratio if control_to_update == self.resolution_width_input \
                else 1 / self.video_aspect_ratio

            setattr(self.options, control_to_update.property, int(mult * e.control.value))

            control_to_update.value = getattr(self.options, control_to_update.property)

        self.user_on_change(None)

    # Called when the OrientationPicker is used.
    # Blindly set resolution without care for the aspect ratio
    # (Because the point of OrientationPicker is to change it)

    def update_orientation(self):
        self.resolution_width_input.value = self.options.resolution_width
        self.resolution_height_input.value = self.options.resolution_height
        self.save_video_aspect_ratio()
