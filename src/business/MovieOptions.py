from dataclasses import dataclass
from typing import Tuple
from textwrap import dedent
from pathlib import Path


from business.Resolution import Resolution

from constants import (
    ASSETS_PATH,
    DEFAULT_OUTPUT_PATH,
    DEFAULT_FONT_LABEL,
    DEFAULT_FONT_NAME
)
from os import path as ospath

@dataclass
class MovieOptions:

    main_color: Tuple[float, float, float] = (255, 255, 255)
    inverse_color: Tuple[float, float, float] = (0, 0, 0)

    resolution_width = 1920
    resolution_height = 1080

    flash_duration: int = 2 # an even number of frames ; flash_duration / 2 main, flash_duration / 2 inverse
    phrase_duration: int = 15 # counted in flashes, one flash = one main + one inverse

    font = DEFAULT_FONT_LABEL
    text_size = 150
    text_border = True
    capitalize_all = True

    images_path = ""
    images_per_flash = 1

    sound = False
    sound_binaural_freq_high = 120
    sound_binaural_freq_lo = 121

    output_framerate = 30
    output_path = ospath.join(DEFAULT_OUTPUT_PATH, "output.mp4")

    def calculate_movie_length_frames(self, script):
        frame_length = self.flash_duration * self.phrase_duration * len(script)
        return frame_length

    def calculate_movie_length_ms(self, script):
        return 1000 * self.calculate_movie_length_frames(script) / self.output_framerate

    @property
    def resolution(self):
        return Resolution(self.resolution_width, self.resolution_height)

    @property
    def font_path(self):
        return ospath.join(ASSETS_PATH, f"{DEFAULT_FONT_NAME}.ttf") \
            if self.font == DEFAULT_FONT_LABEL \
            else self.font

    @property
    def font_name(self):
        return Path(self.font).stem

    def get_video_section_blurb(self):
        return dedent(f"""
        - Resolution : {self.resolution.to_user_format()}px
        - Framerate : {self.output_framerate}fps
        - Flash duration : {self.flash_duration} frames
        - Phrase duration : {self.phrase_duration} flashes
        - Font family : {self.font_name}
        - Font size : {self.text_size}pt
        - With border : {'Yes' if self.text_border else 'No'}
        """)
