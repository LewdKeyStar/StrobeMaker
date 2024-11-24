import flet as ft
from flet_contrib.color_picker import ColorPicker

def hex_to_tuple(rgb_hex):
    h = rgb_hex.lstrip('#')
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def tuple_to_hex(rgb_tuple):
    return '#%02x%02x%02x' % rgb_tuple

class DualColorPicker(ft.Row):
    def __init__(self, page, options):

        self.page = page
        self.options = options

        self.main_color_picker = ColorPicker(
            color = "#FFFFFF"
        )

        self.main_color_picker_dialog = ft.AlertDialog(
            title = ft.Text("Select main movie color"),
            content = self.main_color_picker,
            actions = [
                ft.FilledButton("Select", on_click = lambda _ : self.set_color("main")),
                ft.TextButton("Cancel", on_click = lambda _ : self.close_dialog("main"))
            ],
            actions_alignment = ft.MainAxisAlignment.END,
        )

        self.main_color_trigger = ft.IconButton(
            icon = ft.icons.COLORIZE,
            icon_color = tuple_to_hex(self.options.main_color),
            bgcolor = tuple_to_hex(self.options.main_color),

            on_click = lambda _ : self.page.open(self.main_color_picker_dialog)
        )
        self.main_color_label = ft.Text("Main color")

        self.main_color_area = ft.Row(
            [
                self.main_color_trigger,
                self.main_color_label
            ]
        )

        self.inverse_color_picker = ColorPicker(
            color = "#000000"
        )

        self.inverse_color_picker_dialog = ft.AlertDialog(
            title = ft.Text("Select inverse movie color"),
            content = self.inverse_color_picker,
            actions = [
                ft.FilledButton("Select", on_click = lambda _ : self.set_color("inverse")),
                ft.TextButton("Cancel", on_click = lambda _ : self.close_dialog("inverse"))
            ],
            actions_alignment = ft.MainAxisAlignment.END
        )

        self.inverse_color_trigger = ft.IconButton(
            icon = ft.icons.COLORIZE,
            icon_color = tuple_to_hex(self.options.inverse_color),
            bgcolor = tuple_to_hex(self.options.inverse_color),

            on_click = lambda _ : self.page.open(self.inverse_color_picker_dialog)
        )
        self.inverse_color_label = ft.Text("Inverse color")

        self.inverse_color_area = ft.Row(
            [
                self.inverse_color_trigger,
                self.inverse_color_label
            ]
        )

        super().__init__(
            [
                self.main_color_area,
                self.inverse_color_area
            ]
        )

    def close_dialog(self, which):
        self.page.close(
            getattr(self, f'{which}_color_picker_dialog')
        )

    def set_color(self, which):
        relevant_picker = getattr(self, f'{which}_color_picker')
        relevant_trigger = getattr(self, f'{which}_color_trigger')

        relevant_trigger.icon_color = relevant_picker.color
        relevant_trigger.bgcolor = relevant_picker.color

        self.page.update()

        setattr(self.options, f'{which}_color', hex_to_tuple(relevant_picker.color))

        self.close_dialog(which)
