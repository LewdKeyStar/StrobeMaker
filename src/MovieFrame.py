from dataclasses import dataclass
from typing import ClassVar, Tuple

from BWColor import BWColor
from Resolution import Resolution

from PIL import Image, ImageDraw, ImageFont

@dataclass
class MovieFrame:
    resolution: Resolution
    bg_color: BWColor
    text: str
    text_size: int
    text_border: bool
    font_path: str

    UPLEFT_CORNER: ClassVar[Tuple[int, int]] = (0, 0)

    def create_image(self):

        frame_canvas = Image.new("1", self.resolution.to_tuple(), int(self.bg_color))

        drawer = ImageDraw.Draw(frame_canvas)

        font = ImageFont.truetype(
            self.font_path,
            self.text_size
        )

        _, _, text_right, text_bottom = drawer.textbbox(
            MovieFrame.UPLEFT_CORNER,
            self.text,
            font = font,
            stroke_width = self.stroke_width()
        )

        drawer.text(
            (
                int(frame_canvas.width / 2 - text_right / 2),
                int(frame_canvas.height / 2 - text_bottom / 2)
            ),
            self.text,
            font = font,
            fill = int(self.bg_color) if self.text_border else int(~self.bg_color),
            stroke_fill = int(~self.bg_color),
            stroke_width = self.stroke_width()
        )

        return frame_canvas

    def stroke_width(self):
        return int(0.1 * self.text_size) if self.text_border else 0
