from dataclasses import dataclass

from Resolution import Resolution

@dataclass
class MovieOptions:

    resolution = Resolution(1920, 1080)
    phrase_duration = 6

    font = "Helvetica"
    text_size = 60
    capitalize_all = True

    images_path = ""
    image_per_flash = 1

    sound = False
    sound_binaural_freq_high = 120
    sound_binaural_freq_lo = 121
