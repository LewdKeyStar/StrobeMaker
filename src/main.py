import flet as ft

from business.MovieOptions import MovieOptions
from business.Movie import Movie

from ui.GenerateArea import GenerateArea
from ui.ScriptArea import ScriptArea

def main(page: ft.Page):
    options = MovieOptions()

    page.title = "StrobeMaker"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.dark_theme = ft.Theme(primary_color = ft.colors.BLUE) # color_scheme_seed won't work ; WHY ?
    page.theme_mode = ft.ThemeMode.DARK

    page.update()

    script_area = ScriptArea(page, options)
    generate_area = GenerateArea(page, options)

    # I don't really know how to handle this circular dependency.
    # One can have the other in its constructor, but not both,
    # So it makes the most sense to setup both here.
    # But that just can't scale.

    generate_area.script_field = script_area.script_field
    script_area.script_field.on_change = lambda _ : generate_area.update_enabled()
    script_area.generate_area = generate_area

    page.add(
        ft.Container(
            content = script_area,
            margin = ft.margin.only(bottom = 20)
        ),
        generate_area
    )


if __name__ == '__main__':
    ft.app(main)
