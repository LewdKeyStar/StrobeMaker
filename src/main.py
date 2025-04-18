import flet as ft
import asyncio

from business.MovieOptions import MovieOptions
from business.Movie import Movie
from utils.MovieOptionsWrapper import MovieOptionsWrapper

from ui.GenerateArea import GenerateArea
from ui.ScriptArea import ScriptArea
from ui.DualColorPicker import DualColorPicker
from ui.VideoPreview import VideoPreview

from ui.subsections.VideoSection import VideoSection

from constants import APP_TITLE

async def main(page: ft.Page):
    options = MovieOptionsWrapper(page)

    page.title = APP_TITLE
    page.vertical_alignment = ft.MainAxisAlignment.SPACE_BETWEEN
    page.dark_theme = ft.Theme(primary_color = ft.colors.BLUE) # color_scheme_seed won't work ; WHY ?
    page.theme_mode = ft.ThemeMode.DARK

    page.update()

    script_area = ScriptArea(page, options)
    generate_area = GenerateArea(page, options, script_area.script_field)

    def progress_message_handler(t, render_progress):
        generate_area.update_progress(render_progress)

    page.pubsub.subscribe_topic("progress", progress_message_handler)

    video_preview = VideoPreview(script_area.script_field, page, options)
    await video_preview.update_preview('') # Generate original blank preview

    def vp_async_wrapper(t, _):
        page.run_task(video_preview.update_preview)

    page.pubsub.subscribe_topic("preview", vp_async_wrapper)

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

                                width = 550, # otherwise the column is the full width of the app,
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

                    margin = ft.margin.only(top = 10)
                ),

                ft.Container(
                    content = video_preview,
                    width = 480,
                    height = 270,
                    padding= ft.padding.only(top = 10)
                )
            ],

            alignment = ft.MainAxisAlignment.CENTER
        ),

        ft.Row(
            [
                VideoSection(page, options)
            ],
            alignment = ft.MainAxisAlignment.CENTER
        ),

        generate_area
    )

    video_preview.is_added = True

    # FIXME : I don't know why this is needed.
    # TextField has an autofocus property,
    # And it used to work before the introduction of its prefix and suffix icons.
    # This seems like a framework bug.
    script_area.script_field.focus()


if __name__ == '__main__':
    ft.app(main)
