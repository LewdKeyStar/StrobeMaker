from dataclasses import dataclass
from typing import ClassVar, Tuple

from business.ReversibleColor import ReversibleColor
from business.Resolution import Resolution

from PIL import Image, ImageDraw, ImageFont

@dataclass
class MovieFrame:
    resolution: Resolution
    bg_color: ReversibleColor
    text: str
    text_size: int
    text_border: bool
    font_path: str

    UPLEFT_CORNER: ClassVar[Tuple[int, int]] = (0, 0)

    def __invert__(self):
        return MovieFrame(
            resolution = self.resolution,
            bg_color = ~self.bg_color,
            text = self.text,
            text_size = self.text_size,
            text_border = self.text_border,
            font_path = self.font_path
        )

    def create_image(self):

        frame_canvas = Image.new("RGB", tuple(self.resolution), tuple(self.bg_color))

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
            fill = tuple(self.bg_color) if self.text_border else tuple(~self.bg_color),
            stroke_fill = tuple(~self.bg_color),
            stroke_width = self.stroke_width
        )

        return frame_canvas

    @property
    def stroke_width(self):
        return int(0.1 * self.text_size) if self.text_border else 0

    def __hash__(self):
        return hash((self.text, tuple(self.bg_color)))
