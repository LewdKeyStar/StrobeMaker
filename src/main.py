import flet as ft

from business.MovieOptions import MovieOptions
from business.Movie import Movie
from utils.MovieOptionsWrapper import MovieOptionsWrapper

from ui.GenerateArea import GenerateArea
from ui.ScriptArea import ScriptArea
from ui.DualColorPicker import DualColorPicker
from ui.VideoPreview import VideoPreview

def main(page: ft.Page):
    options = MovieOptions() # with the video preview, this should be MovieOptionsWrapper(page)

    page.title = "StrobeMaker"
    page.vertical_alignment = ft.MainAxisAlignment.SPACE_BETWEEN
    page.dark_theme = ft.Theme(primary_color = ft.colors.BLUE) # color_scheme_seed won't work ; WHY ?
    page.theme_mode = ft.ThemeMode.DARK

    page.update()

    script_area = ScriptArea(page, options)
    generate_area = GenerateArea(page, options, script_area.script_field)



    # FIXME : The video preview is unfeasible. See below.
    # video_preview = VideoPreview(script_area.script_field, options)
    # page.pubsub.subscribe(lambda _ : video_preview.update_preview())

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

                                # Actually, the alignment does fuck-all as is :
                                # It's supposed to be center, but the children are aligned left.
                                # Even CSS works better than this.
                                horizontal_alignment = ft.CrossAxisAlignment.CENTER,
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

                    # Original values : top and left 60, left -45
                    # This was with the video preview standin, which has been removed
                    # Now that the feature appears unusable.
                    margin = ft.margin.only(top = 10)
                )
            ],

            # FIXME : it appears impossible to add the VideoPreview control.
            # The Video controls seems to simply not work on the system ; see #10 for more details.

            alignment = ft.MainAxisAlignment.CENTER
        ),
        generate_area
    )


if __name__ == '__main__':
    ft.app(main)
