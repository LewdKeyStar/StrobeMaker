from dataclasses import dataclass
from typing import ClassVar, Tuple

from business.ReversibleColor import ReversibleColor
from business.Resolution import Resolution

from PIL import Image, ImageDraw, ImageFont

BG_COLOR_INDEX = 0
TEXT_COLOR_INDEX = 1

@dataclass
class MovieFrame:
    resolution: Resolution
    bg_color: ReversibleColor
    text: str
    text_size: int
    text_border_size: int
    font_path: str

    UPLEFT_CORNER: ClassVar[Tuple[int, int]] = (0, 0)

    @property
    def palette(self):
        return [
            *tuple(self.bg_color), *tuple(~self.bg_color)
        ]

    @property
    def stroke_width(self):
        return self.text_border_size

    def __invert__(self):
        return MovieFrame(
            resolution = self.resolution,
            bg_color = ~self.bg_color,
            text = self.text,
            text_size = self.text_size,
            text_border_size = self.text_border_size,
            font_path = self.font_path
        )

    # TODO : we'll have to add font size to this,
    # if we want to manage variable font size in movie
    def __hash__(self):
        return hash((self.text, tuple(self.bg_color)))

    def create_image(self):

        frame_canvas = Image.new("P", tuple(self.resolution), BG_COLOR_INDEX)

        drawer = ImageDraw.Draw(frame_canvas)

        font = ImageFont.truetype(
            self.font_path,
            self.text_size
        )

        _, _, text_right, text_bottom = drawer.textbbox(
            MovieFrame.UPLEFT_CORNER,
            self.text,
            font = font,
            stroke_width = self.stroke_width
        )

        drawer.text(
            (
                int(frame_canvas.width / 2 - text_right / 2),
                int(frame_canvas.height / 2 - text_bottom / 2)
            ),
            self.text,
            font = font,
            # This used to be a bool carried by the MovieFrame instance, but for auto-font logic it's in MovieOptions instead.
            fill = BG_COLOR_INDEX if self.text_border_size > 0 else TEXT_COLOR_INDEX,
            stroke_fill = TEXT_COLOR_INDEX,
            stroke_width = self.stroke_width
        )

        frame_canvas.putpalette(self.palette)

        return frame_canvas
