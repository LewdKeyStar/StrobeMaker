import flet as ft

from ui.atoms.NumberInput import NumberInput
from ui.atoms.CustomSlider import CustomSlider
from ui.atoms.CustomSwitch import CustomSwitch

CONTENT_PADDING = 25

EDIT_WINDOW_WIDTH = 1000
EDIT_WINDOW_HEIGHT = 500

SECTION_TEXT_SIZE = 18

BLURB_COLOR = ft.colors.GREY_300
HINT_COLOR = ft.colors.GREY_400
HIGHLIGHT_COLOR = ft.colors.with_opacity(0.45, ft.colors.GREY_700)

class VideoSection(ft.GestureDetector):

    def __init__(self, page, options):

        self.page = page
        self.options = options

        self.card_container = ft.Card(
            ft.Container(
                # no content, purposeful
                expand = True,
                padding = ft.padding.only(
                    right = CONTENT_PADDING,
                    left = CONTENT_PADDING
                )
            )
        )

        self.fps_input = NumberInput(
            self.page,
            self.options,
            "output_framerate",

            min = 15,
            max = 120,

            user_on_change = lambda _ : self.update_display(True),
        )

        # Placeholder until we can choose fonts
        self.font_family_input = ft.TextField(
            value = "Helvetica Neue",
            disabled = True
        )

        self.font_size_input = NumberInput(
            self.page,
            self.options,
            "text_size",

            min = 60,
            max = 300,

            user_on_change = lambda _ : self.update_display()
        )

        self.font_border_switch = CustomSwitch(
            options = self.options,
            label = "Draw border around text",
            property = "text_border",

            user_on_change = lambda _ : self.update_display()
        )

        self.flash_duration_slider = CustomSlider(
            self.page,
            self.options,
            "flash_duration",

            min = 2,
            max = 20,
            increment = 2,

            user_on_change = lambda _ : self.update_display(True)
        )

        self.flash_duration_seconds = ft.Text(
            italic = True,
            color = HINT_COLOR
        )

        self.phrase_duration_slider = CustomSlider(
            self.page,
            self.options,
            "phrase_duration",

            min = 1,
            max = 100,
            increment = 1,

            user_on_change = lambda _ : self.update_display(True)
        )

        self.phrase_duration_seconds = ft.Text(
            italic = True,
            color = HINT_COLOR
        )

        self.edit_window = ft.AlertDialog(
            title = ft.Text("Edit video settings", text_align = ft.TextAlign.CENTER),

            content = ft.Container(
                ft.Column(
                    [
                        ft.Text("Framerate", size = SECTION_TEXT_SIZE),
                        self.fps_input,

                        ft.Text("Text settings", size = SECTION_TEXT_SIZE),
                        ft.Row(
                            [
                                self.font_family_input, self.font_size_input, self.font_border_switch
                            ],
                            alignment = ft.MainAxisAlignment.CENTER
                        ),

                        ft.Text("Frames per flash", size = SECTION_TEXT_SIZE),
                        ft.Row(
                            [
                                self.flash_duration_slider,
                                self.flash_duration_seconds
                            ],

                            alignment = ft.MainAxisAlignment.SPACE_EVENLY
                        ),

                        ft.Text("Flashes per phrase", size = SECTION_TEXT_SIZE),
                        ft.Row(
                            [
                                self.phrase_duration_slider,
                                self.phrase_duration_seconds
                            ],

                            alignment = ft.MainAxisAlignment.SPACE_EVENLY
                        )
                    ],
                    alignment = ft.MainAxisAlignment.SPACE_BETWEEN
                ),

                width = EDIT_WINDOW_WIDTH,
                height = EDIT_WINDOW_HEIGHT
            )
        )

        super().__init__(
            self.card_container,

            mouse_cursor = ft.MouseCursor.CLICK,

            on_enter = lambda _ : self.update_bgcolor("enter"),
            on_exit = lambda _ : self.update_bgcolor("exit"),
            on_tap = lambda _ : self.page.open(self.edit_window)
        )

        self.update_display(True)

    def update_bgcolor(self, which):
        self.card_container.color = \
            HIGHLIGHT_COLOR if which == "enter" \
            else None # Yes. This works. There is no default color value for cards, so None acts as one.
        self.page.update()

    def update_blurb(self):
        self.card_container.content.content = ft.Text(
            self.options.get_video_section_blurb(),
            color = BLURB_COLOR
        )

    def update_display(self, update_second_durations = False):
        self.update_blurb()

        if update_second_durations:
            flash_duration_seconds = self.options.flash_duration / self.options.output_framerate

            self.flash_duration_seconds.value = \
                f"({flash_duration_seconds:.2f} seconds)"
            self.phrase_duration_seconds.value = \
                f"({(self.options.phrase_duration * flash_duration_seconds):.2f} seconds)"

        if self.page is not None:
            self.page.update()
