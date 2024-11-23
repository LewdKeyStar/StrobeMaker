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

        self.update_script_field_capitalize()

        # Yes, Flet doesn't support clear icons built-in on text fields.
        # They are only available on search bars.
        # Why ?!

        self.clear_button = ft.IconButton(
            icon = ft.icons.CLEAR,
            tooltip = "Clear script text",
            on_click = lambda _ : self.clear()
        )

        self.capitalize_cb = ft.Checkbox(
            label = "Capitalize script",
            value = True,
            on_change = lambda _ : self.update_capitalize()
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
                ft.Column(
                    [
                        ft.Row(
                            [
                                self.script_field,
                                self.clear_button,
                                self.upload_button
                            ],

                            alignment = ft.MainAxisAlignment.START
                        ),
                        ft.Row(
                            [
                                self.capitalize_cb
                            ],

                            alignment = ft.MainAxisAlignment.START
                        )
                    ]
                )
            ],

            alignment = ft.MainAxisAlignment.CENTER
        )

    def clear(self, update_enabled = True):
        self.script_field.value = ""
        self.page.update()

        if update_enabled:
            self.generate_area.update_enabled()

    def update_script_field_capitalize(self):
        self.script_field.capitalization = \
            ft.TextCapitalization.CHARACTERS if self.options.capitalize_all \
            else None # The .NONE value of the enum doesn't work for some reason

    def update_capitalize(self):
        self.options.capitalize_all = self.capitalize_cb.value
        self.update_script_field_capitalize()

        # Update text field content from new capitalization value.
        # Yes, I have to do this manually.
        # This framework doesn't even handle this.
        # I swear to God.

        old_val = self.script_field.value
        self.clear(update_enabled = False)
        self.script_field.value = \
            old_val.upper() if self.script_field.capitalization \
            else "\n".join([line[0].upper() + line[1:].lower() for line in old_val.split('\n')])

        self.page.update()

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
