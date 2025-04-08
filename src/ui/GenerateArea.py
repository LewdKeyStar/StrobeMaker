import flet as ft

from business.Movie import Movie

from utils.misc_utils import add_extension_if_missing

from os import path as ospath
from datetime import timedelta

from constants import APP_TITLE

# Due to how add_extension_if_missing works, we're going to force the MP4 container.
# It's definitely an acceptable state of affairs for now.
# (The alternative would be to look through EVERY common video container extension,
# on every change event.)
VIDEO_EXTENSION = "mp4"
GENERATING_MESSAGE = "Rendering video..."

# TODO : factorize with VideoSection into some sort of style file?
HINT_COLOR = ft.colors.GREY_400

class GenerateArea(ft.Row):
    def __init__(self, page, options, script_field):

        self.page = page
        self.options = options
        self.script_field = script_field

        former_on_change = self.script_field.on_change
        self.script_field.on_change = lambda _ : options.wrap(self.update_enabled, former_on_change)

        self.confirm_dialog = None

        self.output_path_field = ft.TextField(
            label = "Save as...",
            value = self.options.output_path,
            max_lines = 1,
            text_align = ft.TextAlign.LEFT,
            width = 1100, # I hate arbitrary units
            # Isn't %-based sizing a thing in this framework ?!,

            suffix = ft.IconButton(
                icon = ft.icons.FOLDER_OPEN,
                on_click = lambda _ : self.output_path_picker.save_file(
                    dialog_title = "Select path for output file",
                    file_name = "output.mp4",
                    file_type = ft.FilePickerFileType.VIDEO
                )
            ),

            on_change = lambda _ : self.update_output_path()
        )

        self.output_path_picker = ft.FilePicker(
            on_result = self.pick_output_path
        )

        self.page.overlay.append(self.output_path_picker)

        self.generate_button = ft.FilledButton(
            "Generate",
            disabled = True,
            style = ft.ButtonStyle(
                bgcolor =  {
                    "": page.dark_theme.primary_color,
                    ft.ControlState.DISABLED: ft.colors.with_opacity(0.4, page.dark_theme.primary_color)
                },
                color = {
                    "": ft.colors.WHITE,
                    ft.ControlState.DISABLED: ft.colors.WHITE10
                }
            ),
            on_click = lambda _ : self.generate_wrapper()
        )

        # The generate dialog *has* to be preloaded,
        # Because it's necessarily referenced in the pubsub handler.

        self.generate_dialog = ft.AlertDialog(
            modal = True,
            content = ft.Container(
                content = ft.Column(
                    [
                        ft.Text(GENERATING_MESSAGE, text_align = ft.TextAlign.CENTER),
                        ft.ProgressBar(0),
                        ft.Text(text_align = ft.TextAlign.CENTER),
                        ft.Text(text_align = ft.TextAlign.CENTER, color = HINT_COLOR)
                    ],

                    alignment = ft.MainAxisAlignment.CENTER,
                    horizontal_alignment = ft.CrossAxisAlignment.CENTER,
                    height = 80
                ),

                # The arbitrary values, they never end
                padding = ft.padding.only(top = 10)
            )
        )

        super().__init__(
            [
                self.output_path_field,
                self.generate_button
            ],
            alignment = ft.MainAxisAlignment.CENTER
        )

    def update_enabled(self, former_on_change):
        former_on_change()
        self.generate_button.disabled = self.script_field.value.strip() == ""
        self.page.update()

    def update_output_path(self):
        self.options.output_path = add_extension_if_missing(
            self.output_path_field.value,
            VIDEO_EXTENSION
        )
        self.page.update()

    def pick_output_path(self, picker_result_event):
        if picker_result_event.path is None:
            return

        path = add_extension_if_missing(picker_result_event.path, VIDEO_EXTENSION)

        self.output_path_field.value = path
        self.update_output_path()

    def generate_wrapper(self):

        if ospath.exists(self.options.output_path):

            self.confirm_dialog = ft.AlertDialog(
                title = ft.Text("File already exists"),
                content = ft.Text(f'Do you wish to overwrite the existing file by the name of \"{ ospath.basename(self.options.output_path) }\" ?'),
                actions = [
                    ft.FilledButton("Yes", on_click = lambda _ : self.generate()),
                    ft.TextButton("No", on_click = lambda _ : self.close_confirm_dialog())
                ],
                actions_alignment = ft.MainAxisAlignment.END,
            )

            self.page.open(self.confirm_dialog)

        else:
            self.generate()

    def close_confirm_dialog(self):
        # TODO : why exactly am I keeping it None ?
        # What's the point ?
        # Keeping random dialogs in memory and not shown is just part of this framework, embrace it :)

        if self.confirm_dialog is not None:
            self.page.close(self.confirm_dialog)
            self.confirm_dialog = None

    def generate(self):

        self.page.open(self.generate_dialog)
        Movie(self.script_field.value.split('\n'), self.options).create_movie(pubsub = self.page.pubsub)
        self.page.close(self.generate_dialog)

        self.page.title = APP_TITLE

        # Ugly as fuck, but where else could we put it ?
        self.close_confirm_dialog()

    def update_progress(self, render_progress):

        movie_length = self.options.calculate_movie_length_frames(self.script_field.value.split('\n'))

        # Update detailed frame by frame progress info
        self.generate_dialog.content.content.controls[3].value = \
            f"Frame {render_progress.frame_number} of {movie_length} @ {render_progress.fps} fps"

        render_percent = render_progress.frame_number / movie_length

        # Set progress bar value
        self.generate_dialog.content.content.controls[1].value = render_percent

        render_percent_pretty_string = round(render_percent*100)

        # Update completion percentage text
        self.generate_dialog.content.content.controls[0].value = \
            f"{GENERATING_MESSAGE}{render_percent_pretty_string}% done"

        remaining_time_sec = \
            round(
                (movie_length - render_progress.frame_number) / render_progress.fps
            ) \
            if render_progress.fps > 0 \
            else 0 # Start with 00:00:00 remaining, no big deal

        # Update time remaining
        self.generate_dialog.content.content.controls[2].value = \
            f"{timedelta(seconds = remaining_time_sec)} remaining"

        # Finally, also display in app title for users who tabbed out
        self.page.title = f"Rendering ({render_percent_pretty_string}%) — {APP_TITLE}"

        self.page.update()
