import ffmpeg

from dataclasses import dataclass

from PIL import ImageOps
from os import makedirs, path as ospath
from shutil import rmtree

from business.MovieOptions import MovieOptions
from business.MovieFrame import MovieFrame
from business.ReversibleColor import ReversibleColor

from constants import ASSETS_PATH, TEMP_OUTPUT_PATH

from time import perf_counter

@dataclass
class Movie:

    script: list[str]
    options: MovieOptions = MovieOptions()

    @staticmethod
    def get_font_path(font_name):
        return ospath.join(ASSETS_PATH, f"{font_name}.ttf")

    def flash_group(self, image):
        return [
            *[image for i in range(self.options.flash_duration // 2)],
            *[~image for i in range(self.options.flash_duration // 2)]
        ]

    def create_movie(self, fast = False):

        start_time = perf_counter()

        frames = []

        for line in self.script:

            for i in range(self.options.phrase_duration):
                frames.extend(
                    frame.create_image()

                    for frame in

                    self.flash_group(
                        MovieFrame(
                            self.options.resolution,
                            ReversibleColor(self.options.main_color, self.options.inverse_color),
                            text = line.upper() if self.options.capitalize_all else line,
                            text_size = self.options.text_size,
                            text_border = self.options.text_border,
                            font_path = Movie.get_font_path(self.options.font)
                        )
                    )
                )

        print("Wrote movie frames to RAM in", perf_counter() - start_time, "seconds")
        start_time = perf_counter()

        rmtree(TEMP_OUTPUT_PATH, ignore_errors = True)
        makedirs(TEMP_OUTPUT_PATH)
        makedirs(ospath.dirname(self.options.output_path), exist_ok = True)

        for i, frame in enumerate(frames):
            frame.save(ospath.join(TEMP_OUTPUT_PATH, f"{'%04d' % i}.png"))

        print("Wrote movie frames to disk in", perf_counter() - start_time, "seconds")
        start_time = perf_counter()

        ffmpeg.input(
            ospath.join(TEMP_OUTPUT_PATH, '%04d.png'),
            framerate = self.options.output_framerate
        ).output(
            self.options.output_path,
            crf = 28 if fast else 23,
            preset = "ultrafast" if fast else "medium"
        ).run(
            overwrite_output = True
        )

        print("Wrote final movie to disk in", perf_counter() - start_time, "seconds")

        rmtree(TEMP_OUTPUT_PATH)
