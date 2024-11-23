from dataclasses import dataclass

from business.Resolution import Resolution

from constants import DEFAULT_OUTPUT_PATH
from os import path as ospath

@dataclass
class MovieOptions:

    resolution = Resolution(1920, 1080)
    phrase_duration = 3 # counted in flashes, one flash = one white + one black

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
