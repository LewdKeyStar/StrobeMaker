import flet as ft

from ui.atoms.NumberInput import NumberInput
from ui.atoms.CustomSlider import CustomSlider
from ui.atoms.CustomSwitch import CustomSwitch
from ui.atoms.CustomSearch import CustomSearch

from constants import FONT_LIST, DEFAULT_FONT_LABEL

from pathlib import Path

CONTENT_PADDING = 25

EDIT_WINDOW_WIDTH = 1000
EDIT_WINDOW_HEIGHT = 500

LARGE_NUMINPUT_WIDTH = 150

LOWRES_WIDTH = 256
LOWRES_HEIGHT = 144
HIGHRES_WIDTH = 3840
HIGHRES_HEIGHT = 2160

SECTION_TEXT_SIZE = 18
UNIT_TEXT_SIZE = 16

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

        self.resolution_width_input = NumberInput(
            self.page,
            self.options,
            "resolution_width",

            min = LOWRES_WIDTH,
            max = HIGHRES_WIDTH,

            width = LARGE_NUMINPUT_WIDTH,

            user_on_change = lambda _ : self.update_display()
        )

        self.resolution_height_input = NumberInput(
            self.page,
            self.options,
            "resolution_height",

            min = LOWRES_HEIGHT,
            max = HIGHRES_HEIGHT,

            width = LARGE_NUMINPUT_WIDTH,

            user_on_change = lambda _ : self.update_display()
        )

        self.fps_input = NumberInput(
            self.page,
            self.options,
            "output_framerate",

            min = 15,
            max = 120,

            user_on_change = lambda _ : self.update_display(update_second_durations = True),
        )

        self.font_family_input = CustomSearch(
            self.page,
            self.options,
            "font",

            items = [DEFAULT_FONT_LABEL] + FONT_LIST,
            transform = lambda x : Path(x).stem,

            user_on_change = lambda _ : self.update_display(move_focus = True)
        )

        self.font_size_input = NumberInput(
            self.page,
            self.options,
            "text_size",

            min = 10,
            max = 1000,

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

            user_on_change = lambda _ : self.update_display(update_second_durations = True)
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

            user_on_change = lambda _ : self.update_display(update_second_durations = True)
        )

        self.phrase_duration_seconds = ft.Text(
            italic = True,
            color = HINT_COLOR
        )

        self.dummy_child = ft.TextField(visible = False)

        self.edit_window = ft.AlertDialog(
            title = ft.Text("Edit video settings", text_align = ft.TextAlign.CENTER),

            content = ft.Container(
                ft.Column(
                    [
                        ft.Text("Video profile", size = SECTION_TEXT_SIZE),
                        ft.Row(
                            [
                                ft.Row(
                                    [
                                        self.resolution_width_input,
                                        ft.Text("x", size = UNIT_TEXT_SIZE),
                                        self.resolution_height_input,
                                        ft.Text("px", size = UNIT_TEXT_SIZE)
                                    ]
                                ),

                                ft.Row(
                                    [
                                        self.fps_input,
                                        ft.Text("fps", size = UNIT_TEXT_SIZE)
                                    ]
                                )
                            ],

                            alignment = ft.MainAxisAlignment.SPACE_EVENLY
                        ),

                        ft.Text("Text settings", size = SECTION_TEXT_SIZE),
                        ft.Row(
                            [
                                self.font_family_input,
                                self.font_size_input,
                                ft.Text("px", size = UNIT_TEXT_SIZE),
                                ft.Container(
                                    content = self.font_border_switch,

                                    margin = ft.margin.only(left = 20)
                                )
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
                        ),

                        self.dummy_child
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

        self.update_display(update_second_durations = True)

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

    def update_display(self, *, update_second_durations = False, move_focus = False):
        self.update_blurb()

        if update_second_durations:
            flash_duration_seconds = self.options.flash_duration / self.options.output_framerate

            self.flash_duration_seconds.value = \
                f"({flash_duration_seconds:.2f} seconds)"
            self.phrase_duration_seconds.value = \
                f"({(self.options.phrase_duration * flash_duration_seconds):.2f} seconds)"

        # It's not intuitive for the font selector to keep focus when the choice has been made.
        # Since we can't just blur it (there is no blur() method),
        # Move the focus to the font size input instead,
        # Since desired font size often changes between fonts.
        if move_focus:
            self.font_size_input.focus()

        if self.page is not None:
            self.page.update()
