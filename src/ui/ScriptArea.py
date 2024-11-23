import flet as ft

MAX_LINES = 10
# SCRIPT_WIDTH = 300

class ScriptArea(ft.Row):
    def __init__(self, page, options):

        self.page = page
        self.options = options

        self.script_field = ft.TextField(
            label = "Video script",
            hint_text = "Enter words to flash or upload a file",
            value = "",
            multiline = True,
            max_lines = MAX_LINES,
            text_align = ft.TextAlign.JUSTIFY
        )

        # Yes, Flet doesn't support clear icons built-in on text fields.
        # They are only available on search bars.
        # Why ?!

        self.clear_button = ft.IconButton(
            icon = ft.icons.CLEAR,
            tooltip = "Clear script text",
            on_click = lambda _ : self.clear()
        )

        self.script_picker = ft.FilePicker(
            on_result = self.upload_script
        )

        self.page.overlay.append(self.script_picker)

        self.upload_button = ft.FilledTonalButton(
            "Upload text file",
            icon=ft.icons.UPLOAD_FILE,
            on_click = lambda _ : self.script_picker.pick_files(
                dialog_title = "Select script file",
                file_type=ft.FilePickerFileType.CUSTOM,
                allowed_extensions = ['txt']
            )
        )

        super().__init__(
            [
                self.script_field,
                self.clear_button,
                self.upload_button
            ],
            alignment = ft.MainAxisAlignment.CENTER
        )

    def clear(self):
        self.script_field.value = ""
        self.page.update()
        self.generate_area.update_enabled()

    def upload_script(self, picker_result_event):
        if picker_result_event.files is None:
            return

        with open(picker_result_event.files[0].path) as script_file:
            self.script_field.value = \
                (script_file.read().upper() if self.options.capitalize_all \
                else script_file.read()).strip()

        self.page.update()
        # Yes, in that order.
        self.generate_area.update_enabled()
