import flet as ft

from os import makedirs
from os.path import dirname

from utils.misc_utils import add_extension_if_missing

MIN_LINES = MAX_LINES = 5
MIN_LINES_LARGE = MAX_LINES_LARGE = 20

SCRIPT_WIDTH = 400
SCRIPT_WIDTH_LARGE = 1000
SCRIPT_HEIGHT_LARGE = 500

SCRIPT_FIELD_ICONS_PADDING_LEFT = -20
SCRIPT_FIELD_ICONS_PADDING_TOP = -8

SCRIPT_FIELD_CONTENT_PADDING_LEFT = SCRIPT_FIELD_CONTENT_PADDING_BOTTOM = 20
SCRIPT_FIELD_CONTENT_PADDING_TOP = -5
SCRIPT_FIELD_CONTENT_PADDING_TOP_LARGE = 10

TOGGLE_PADDING = -5 # the toggle has baked-in left-hand padding for some goddamn reason

SCRIPT_FILE_EXTENSION = "txt"

class ScriptArea(ft.Row):
    def __init__(self, page, options):

        self.page = page
        self.options = options

        self.script_field = ft.TextField(

            # FIXME : this used to work, but no longer does
            # since the introduction of the prefix and suffix icons.
            # autofocus = True,

            prefix = ft.Container(
                content = ft.IconButton(
                    icon = ft.icons.FULLSCREEN,
                    tooltip = "Expand to script window",
                    on_click = lambda _ : self.page.open(
                        self.script_window
                    )
                ),

                padding = ft.padding.only(
                    left = SCRIPT_FIELD_ICONS_PADDING_LEFT,
                    top = SCRIPT_FIELD_ICONS_PADDING_TOP)
            ),

            width = SCRIPT_WIDTH,
            content_padding = ft.padding.only(
                left = SCRIPT_FIELD_CONTENT_PADDING_LEFT,
                bottom = SCRIPT_FIELD_CONTENT_PADDING_BOTTOM,
                top = SCRIPT_FIELD_CONTENT_PADDING_TOP
            ),

            label = "Video script",
            hint_text = "Enter words to flash or upload a file",
            value = "",
            multiline = True,
            min_lines = MIN_LINES,
            max_lines = MAX_LINES,
            text_align = ft.TextAlign.JUSTIFY,

            suffix = ft.Container(
                ft.IconButton(
                    icon = ft.icons.CLEAR,
                    tooltip = "Clear script text",
                    on_click = lambda _ : self.clear()
                ),

                padding = ft.padding.only(top = SCRIPT_FIELD_ICONS_PADDING_TOP)
            )
        )

        self.capitalize_toggle = ft.Switch(
            label = "  Capitalize script", # Yes, this is intentional leading whitespace you're seeing
            # No, this framework does not allow for control labels to define padding
            # Please save me from this hell
            value = True,
            on_change = lambda _ : self.update_capitalize()
        )

        self.capitalize_toggle_container = ft.Container(
            self.capitalize_toggle,
            padding = ft.padding.only(left = TOGGLE_PADDING)
        )

        self.script_window = ft.AlertDialog(
            title = ft.Text("Edit video script", text_align = ft.TextAlign.CENTER),

            content = ft.Column(
                [
                    ft.TextField(
                        autofocus = True,

                        expand = True,
                        width = SCRIPT_WIDTH_LARGE,
                        height = SCRIPT_HEIGHT_LARGE,
                        content_padding = ft.padding.only(
                            left = SCRIPT_FIELD_CONTENT_PADDING_LEFT,
                            bottom = SCRIPT_FIELD_CONTENT_PADDING_BOTTOM,
                            top = SCRIPT_FIELD_CONTENT_PADDING_TOP_LARGE
                        ),

                        hint_text = "Enter words to flash or upload a file",

                        value = "",
                        multiline = True,
                        min_lines = MIN_LINES_LARGE,
                        max_lines = MAX_LINES_LARGE,

                        on_change = lambda _ : self.update_script_field_value_from_script_window(),

                        suffix = ft.Container(
                            ft.IconButton(
                                icon = ft.icons.CLEAR,
                                tooltip = "Clear script text",
                                on_click = lambda _ : self.clear()
                            ),

                            padding = ft.padding.only(top = SCRIPT_FIELD_ICONS_PADDING_TOP)
                        )
                    ),

                    self.capitalize_toggle_container
                ]
            ),

            actions = [
                ft.FilledButton("OK", on_click = lambda _ : self.page.close(self.script_window)),
            ],

            actions_alignment = ft.MainAxisAlignment.END,
        )

        # For SOME fucking reason, setting this on_change at control declaration does nothing.
        # it works everywhere else, including in the very script window right above,
        # but not here.
        self.script_field.on_change = self.update_script_window_value

        self.update_script_field_capitalize()

        self.script_importer = ft.FilePicker(
            on_result = self.import_script
        )

        self.page.overlay.append(self.script_importer)

        self.import_button = ft.FilledTonalButton(
            "Import script",
            icon = ft.icons.DOWNLOAD,
            on_click = lambda _ : self.script_importer.pick_files(
                dialog_title = "Select script file",
                file_type=ft.FilePickerFileType.CUSTOM,
                allowed_extensions = [SCRIPT_FILE_EXTENSION]
            )
        )

        self.script_exporter = ft.FilePicker(
            on_result = self.export_script
        )

        self.page.overlay.append(self.script_exporter)

        self.export_button = ft.FilledTonalButton(
            "Export script",
            icon = ft.icons.UPLOAD,
            on_click = lambda _ : self.script_exporter.save_file(
                dialog_title = "Save script",
                file_type = ft.FilePickerFileType.CUSTOM,
                allowed_extensions = [SCRIPT_FILE_EXTENSION]
            )
        )

        super().__init__(
            [
                ft.Column(
                    [
                        ft.Row(
                            [
                                self.script_field,
                                ft.Column(
                                    [
                                        self.import_button,
                                        self.export_button
                                    ]
                                )
                            ],

                            # FIXME : the two buttons are slightly too much to the left
                            # but this is the only alignment that WORKS
                            # space_between and space_evenly just STICK the two children together
                            # with zero spacing
                            # fuck. this. framework.
                            alignment = ft.MainAxisAlignment.START
                        ),
                        self.capitalize_toggle_container
                    ]
                )
            ],

            alignment = ft.MainAxisAlignment.START
        )

    def clear(self):
        if self.script_field.value == "":
            return

        else:

            def effective_clear():
                self.script_field.value = ""
                self.page.update()
                self.script_field.on_change(None)
                # The magic of interpreted code : pre-declaration lexical reference
                self.page.close(clear_confirm_dialog)

            clear_confirm_dialog = ft.AlertDialog(
                title = ft.Text("Clear video script ?"),

                content = ft.Text("Do you really want to delete this video's script ?"),

                actions = [
                    ft.FilledButton("Yes", on_click = lambda _ : effective_clear()),
                    ft.TextButton("No", on_click = lambda _ : self.page.close(clear_confirm_dialog))
                ],
                actions_alignment = ft.MainAxisAlignment.END
            )

            self.page.open(clear_confirm_dialog)

    def update_script_field_value_from_script_window(self):
        self.script_field.value = self.script_window.content.controls[0].value
        self.script_field.on_change(None)
        self.page.update()

    def update_script_window_value(self):
        self.script_window.content.controls[0].value = self.script_field.value

    def update_script_field_capitalize(self):
        self.script_field.capitalization = \
        self.script_window.content.controls[0].capitalization = \
            ft.TextCapitalization.CHARACTERS if self.options.capitalize_all \
            else None # The .NONE value of the enum doesn't work for some reason

    def update_capitalize(self):
        self.options.capitalize_all = self.capitalize_toggle.value
        self.update_script_field_capitalize()

        # Update text field content from new capitalization value.
        # Yes, I have to do this manually.
        # This framework doesn't even handle this.
        # I swear to God.

        old_val = self.script_field.value

        self.script_field.value = \
        self.script_window.content.controls[0].value = \
            old_val.upper() if self.script_field.capitalization \
            else "\n".join([
                line[0].upper() + \
                line[1:].lower() if len(line) > 1 else "" \
                for line in old_val.split('\n')
            ])

        self.page.update()

    def import_script(self, picker_result_event):
        if picker_result_event.files is None:
            return

        with open(picker_result_event.files[0].path) as script_file:
            self.script_field.value = \
                (script_file.read().upper() if self.options.capitalize_all \
                else script_file.read()).strip()

        self.script_field.focus()

        self.page.update()
        # Yes, in that order.
        self.script_field.on_change(None)

    def export_script(self, picker_result_event):
        if picker_result_event.path is None:
            return

        path = add_extension_if_missing(
            picker_result_event.path,
            SCRIPT_FILE_EXTENSION
        )

        makedirs(
            dirname(path),
            exist_ok=True
        )

        with open(path, mode="w", encoding="utf-8-sig") as writer:
            writer.write(self.script_field.value)
