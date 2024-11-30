from dataclasses import dataclass
from typing import Tuple

from business.Resolution import Resolution

from constants import DEFAULT_OUTPUT_PATH
from os import path as ospath

@dataclass
class MovieOptions:

    main_color: Tuple[float, float, float] = (255, 255, 255)
    inverse_color: Tuple[float, float, float] = (0, 0, 0)

    resolution = Resolution(1920, 1080)

    flash_duration: int = 2 # an even number of frames ; flash_duration / 2 main, flash_duration / 2 inverse
    phrase_duration: int = 15 # counted in flashes, one flash = one main + one inverse

    font = "HelveticaNeue"
    text_size = 150
    text_border = True
    capitalize_all = True

    images_path = ""
    image_per_flash = 1

    sound = False
    sound_binaural_freq_high = 120
    sound_binaural_freq_lo = 121

    output_framerate = 30
    output_path = ospath.join(DEFAULT_OUTPUT_PATH, "output.mp4")

    def calculate_movie_length_ms(self, script):
        frame_length = self.flash_duration * self.phrase_duration * len(script)
        return 1000 * frame_length / self.output_framerate
