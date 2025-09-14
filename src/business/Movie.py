import ffmpeg
import threading

from dataclasses import dataclass

from PIL import ImageOps, ImageFont
from os import makedirs, symlink, path as ospath
from shutil import rmtree

from business.MovieOptions import MovieOptions
from business.MovieFrame import MovieFrame
from business.ReversibleColor import ReversibleColor

from constants import ASSETS_PATH, DEFAULT_FONT_LABEL
from utils.misc_utils import _tmpdir_scope
from utils.ffmpeg_progress import track_ffmpeg_progress

from time import perf_counter

# TODO : Ugly orphan constants, do something about this please
OPTIMAL_TEXT_PERCENT_H = 0.75
OPTIMAL_TEXT_PERCENT_W = 0.9

@dataclass
class Movie:

    script: list[str]
    options: MovieOptions = MovieOptions()

    def flash_group(self, image, provided_invert = None):
        inverted_image = ~image if provided_invert is None else provided_invert
        return [
            *[image for i in range(self.options.flash_duration // 2)],
            *[inverted_image for i in range(self.options.flash_duration // 2)]
        ]

    # Should be fired when auto font size is enabled whenever the script, border, resolution or font changes
    # FIXME : uses the border size instead of zeroeing out if border is disabled !!
    def get_auto_font_size(self):

        # First, establish an upper limit : the percentage times the frame height.
        # This is a constant for all lines of the script.

        max_size_borderless = int(
            OPTIMAL_TEXT_PERCENT_H * self.options.resolution_height
        )

        # In testing, it doesn't seem to make a difference whether the border size is calculated
        # with the default size or max_size_borderless.
        # However, for correctness purposes, we do it anyway.

        calc_options = self.options.clone({'text_size': max_size_borderless})

        # Now, we can establish a slightly lower limit, taking the potential text border into consideration.

        max_size = \
            max_size_borderless - 2 * calc_options.text_border_size

        # However, the real size is determined by the longest line of the script,
        # As it must still fit entirely within the frame.

        longest_line = sorted(self.script, key = lambda line : len(line))[-1]

        # We need a PIL ImageFont object to calculate the line size in pixels.

        font = ImageFont.truetype(calc_options.font_path, max_size)

        size = max_size
        calc_options.text_size = size

        # And now, until the longest line fits comfortably in the frame, we lower the size.

        while font.getlength(longest_line) > OPTIMAL_TEXT_PERCENT_W * calc_options.resolution_width - 2 * calc_options.text_border_size:
            size -= 1
            calc_options.text_size = size
            font = ImageFont.truetype(self.options.font_path, size)

        return size

    def create_movie(self, *, fast = False, pubsub = None):

        start_time = perf_counter()

        frames = []
        unique_frames = {}

        for frame_index, line in enumerate(self.script):

            frame_id = (line, tuple(self.options.main_color))
            inverse_frame_id = (line, tuple(self.options.inverse_color))
            is_new_frame = frame_id not in unique_frames

            flash_group = self.flash_group(
                MovieFrame(
                    self.options.resolution,
                    ReversibleColor(self.options.main_color, self.options.inverse_color),
                    text = line.upper() if self.options.capitalize_all else line,
                    text_size = self.options.text_size,
                    text_border_size = self.options.text_border_size,
                    font_path = self.options.font_path
                )

                if is_new_frame

                else unique_frames[frame_id],

                None if is_new_frame else unique_frames[inverse_frame_id]
            )

            for i in range(self.options.phrase_duration):
                frames.extend(frame for frame in flash_group)

            if is_new_frame:
                unique_frames[frame_id] = flash_group[0]
                unique_frames[inverse_frame_id] = flash_group[self.options.flash_duration // 2]

        dt_movie_frames_objects = perf_counter() - start_time
        print("Created movie frame objects in", dt_movie_frames_objects, "seconds")
        start_time = perf_counter()

        makedirs(ospath.dirname(self.options.output_path), exist_ok = True)

        with _tmpdir_scope() as tmpdir:

            file_paths = {}

            for i, frame in enumerate(frames):
                file_path = ospath.join(tmpdir, f"{'%04d' % i}.png")

                if frame not in file_paths:
                    frame.create_image().save(file_path, compress_level = 1)
                    file_paths[frame] = file_path
                else:
                    symlink(file_paths[frame], file_path)

            # I am unable to properly test the increase in perf from using RAM-based tmpdir,
            # Because it is negligible against an SSD.

            dt_movie_frames_write = perf_counter() - start_time
            print("Wrote movie frames to RAM in", dt_movie_frames_write, "seconds")
            start_time = perf_counter()

            socket_filename = ospath.join(tmpdir, "progress_socket")

            def render():
                ffmpeg.input(
                    ospath.join(tmpdir, '%04d.png'),
                    framerate = self.options.output_framerate
                ).output(
                    self.options.output_path,
                    crf = 28 if fast else 23,
                    preset = "ultrafast" if fast else "medium"
                ).global_args(
                    "-hide_banner", # suppress startup print (version, etc.)
                    "-loglevel", "error",
                    "-progress", f"unix://{socket_filename}", # unix:// prefix makes this a valid resource URL !
                    "-y", # use -y, not overwrite_output, because the latter is ignored when global_args() is used
                ).run_async().wait() # run_async() is necessary when piping output

            t1 = threading.Thread(target = render)
            t2 = threading.Thread(target = track_ffmpeg_progress, args = (socket_filename, pubsub))

            t1.start()
            t2.start()

            t1.join()
            t2.join()

            dt_movie_render = perf_counter() - start_time
            print("Wrote final movie to disk in", dt_movie_render, "seconds")

            print(
                "Total render time :",
                dt_movie_frames_objects + dt_movie_frames_write + dt_movie_render,
                "seconds"
            )
