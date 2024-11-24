import flet as ft

from business.MovieOptions import MovieOptions
from business.Movie import Movie

from ui.GenerateArea import GenerateArea
from ui.ScriptArea import ScriptArea
from ui.DualColorPicker import DualColorPicker

def main(page: ft.Page):
    options = MovieOptions()

    page.title = "StrobeMaker"
    page.vertical_alignment = ft.MainAxisAlignment.SPACE_BETWEEN
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

    dual_color_picker = DualColorPicker(page, options)

    page.add(
        ft.Row(
            [
                ft.Container(
                    content = ft.Card(
                        content = ft.Container(
                            content = ft.Column(
                                [
                                    script_area,
                                    dual_color_picker
                                ],

                                width = 500, # otherwise the column is the full width of the app,
                                # and this, for some reason, fucks up the cross axis alignment
                                # (the color picker ends up left, but the script area is centered)
                                # I'm not even sure the alignment has any effect right now :
                                # It was STRETCH during testing and its appearance was identical
                                horizontal_alignment = ft.CrossAxisAlignment.START,
                            ),

                            # For some reason
                            # (Notice I'm saying this a lot)
                            # A padding of 20 is not sufficient for the right side ;
                            # The upload button clips out of the card ??
                            # Can't the card determine its content size and apply the padding in the proper place ?
                            # This is baffling !

                            padding = ft.padding.only(
                                left = 20,
                                top = 20,
                                bottom = 20,
                                right = 45
                            )
                        )
                    ),

                    # More arbitrary values, yay !
                    # The 60 is for left side alignment,
                    # The -45 is to compensate the stupid card padding
                    margin = ft.margin.only(left = 60, top = 60, right = -45)
                ),

                # Stand-in for the video preview (issue #10)

                ft.canvas.Canvas(
                    [
                        ft.canvas.Rect(
                            # TODO : these arbitrary values are at least temporary :
                            # Canvas elements are ALWAYS absolute positioned,
                            # so the Row alignment has no bearing on them.

                            # When this becomes a real video preview, we won't have to do this
                            # ... hopefully
                            x = 270, y = -50, width = 350, height = 200,
                            paint = ft.Paint(color = "#FFFFFF", style = ft.PaintingStyle.FILL)
                        )
                    ]
                )
            ],

            # TODO : add alignment when video preview is available
        ),
        generate_area
    )


if __name__ == '__main__':
    ft.app(main)
