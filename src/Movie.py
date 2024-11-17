import ffmpeg

from dataclasses import dataclass

from PIL import ImageOps
from os import makedirs, path as ospath
from shutil import rmtree

from MovieOptions import MovieOptions
from MovieFrame import MovieFrame
from BWColor import BWColor

from constants import ASSETS_PATH, TEMP_OUTPUT_PATH

@dataclass
class Movie:

    script: list[str]
    options: MovieOptions = MovieOptions()

    @staticmethod
    def flash_pair(image):
        return [image, ImageOps.invert(image)]

    @staticmethod
    def get_font_path(font_name):
        return ospath.join(ASSETS_PATH, f"{font_name}.ttf")

    def create_movie(self):
        frames = []

        for line in self.script:

            for i in range(self.options.phrase_duration):
                frames.extend(
                    Movie.flash_pair(
                        MovieFrame(
                            self.options.resolution,
                            BWColor("WHITE"),
                            text = line.upper() if self.options.capitalize_all else line,
                            text_size = self.options.text_size,
                            font_path = Movie.get_font_path(self.options.font)
                        ).create_image()
                    )
                )

        makedirs(TEMP_OUTPUT_PATH)

        for i, frame in enumerate(frames):
            frame.save(ospath.join(TEMP_OUTPUT_PATH, f"{'%04d' % i}.png"))

        ffmpeg.input(
            ospath.join(TEMP_OUTPUT_PATH, '%04d.png'),
            framerate = self.options.output_framerate
        ).output(
            self.options.output_path
        ).run()

        rmtree(TEMP_OUTPUT_PATH)
