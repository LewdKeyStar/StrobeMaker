from dataclasses import dataclass

from Resolution import Resolution

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
    output_path = "output.mp4"
