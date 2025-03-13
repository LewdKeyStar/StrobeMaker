import flet as ft

from business.Movie import Movie

from utils.misc_utils import add_extension_if_missing

from os import path as ospath

# Due to how add_extension_if_missing works, we're going to force the MP4 container.
# It's definitely an acceptable state of affairs for now.
# (The alternative would be to look through EVERY common video container extension,
# on every change event.)
VIDEO_EXTENSION = "mp4"

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
        if self.confirm_dialog is not None:
            self.page.close(self.confirm_dialog)
            self.confirm_dialog = None

    def generate(self):
        generate_dialog = ft.AlertDialog(
            modal = True,
            content = ft.Container(
                content = ft.Row(
                    [
                        # TODO : replace with ffmpeg-derived progress bar
                        # (see https://github.com/kkroening/ffmpeg-python/blob/master/examples/show_progress.py)
                        ft.ProgressRing(),
                        ft.Text("Generating movie...")
                    ],

                    alignment = ft.MainAxisAlignment.CENTER
                ),

                # The arbitrary values, they never end
                padding = ft.padding.only(top = 30)
            )
        )

        self.page.open(generate_dialog)
        Movie(self.script_field.value.split('\n'), self.options).create_movie()
        self.page.close(generate_dialog)

        self.close_confirm_dialog()
