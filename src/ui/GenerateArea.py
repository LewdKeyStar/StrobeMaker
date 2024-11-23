import flet as ft

from business.Movie import Movie

from os import path as ospath

class GenerateArea(ft.Row):
    def __init__(self, page, options):

        self.page = page
        self.options = options

        self.output_path_field = ft.TextField(
            label = "Save as...",
            value = self.options.output_path,
            max_lines = 1,
            text_align = ft.TextAlign.LEFT,

            on_change = self.update_output_path
        )

        self.output_path_picker = ft.FilePicker(
            on_result = self.pick_output_path
        )

        self.page.overlay.append(self.output_path_picker)

        self.pick_path_button = ft.IconButton(
            icon = ft.icons.FOLDER_OPEN,
            on_click = lambda _ : self.output_path_picker.save_file(
                dialog_title = "Select path for output file",
                file_name = "output.mp4",
                file_type = ft.FilePickerFileType.VIDEO
            )
        )

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
            on_click = lambda _ : self.generate()
        )

        super().__init__(
            [
                self.output_path_field,
                self.pick_path_button,
                self.generate_button
            ],
            alignment = ft.MainAxisAlignment.CENTER
        )

    def update_enabled(self):
        self.generate_button.disabled = self.script_field.value.strip() == ""
        self.page.update()

    def update_output_path(self):
        self.options.output_path = self.output_path_field.value
        self.page.update()

    def pick_output_path(self, picker_result_event):
        if picker_result_event.path is None:
            return

        self.output_path_field.value = picker_result_event.path
        self.update_output_path()

    def generate(self):
        Movie(self.script_field.value.split('\n'), self.options).create_movie()
