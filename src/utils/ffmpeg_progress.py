from dataclasses import dataclass

@dataclass
class RenderProgress:
    frame_number: int
    fps: int

import socket

BUFSIZE = 16

# This logic is adapted from https://github.com/kkroening/ffmpeg-python/blob/df129c7ba30aaa9ffffb81a48f53aa7253b0b4e6/examples/show_progress.py#L42
# (but condensed into a single function because I'm not sure why they break it down so much)

def track_ffmpeg_progress(socket_filename, pubsub):

    # Create a stream socket :
    # Listening on it allows us to constantly take in new data
    # (via an ACTIVE recv() call rather than a reader object),
    # Unlike a pipe or file which wait for the write to end.
    # This way, we can track the progress output as it happens!

    # We use a Unix address so that it can simply be formatted as unix://
    # in the argument to the ffmpeg -progress option.
    # Despite the name, this *should* work on Windows platforms.

    sock = socket.socket(family = socket.AF_UNIX, type = socket.SOCK_STREAM)
    sock.bind(socket_filename)

    sock.listen(1) # Meaning : accept only one connection (ours)

    connection, addr = sock.accept()

    data = b''
    frame_number = 0
    fps = 0

    try:
        while True:
            new_data = connection.recv(BUFSIZE)

            if not new_data:
                break

            data += new_data
            lines = data.split(b'\n')

            # This handler code is taken straight from the example,
            # It simply focuses on completing one line before moving on to the next,
            # Such that the line can then be split between key and val.
            # For our purposes, we're only using the frame number,
            # But by doing this, we can fetch any information from the progress print.

            for line in lines[:-1]:

                line = line.decode()
                parts = line.split('=')

                key = parts[0] if len(parts) > 0 else None
                value = parts[1] if len(parts) > 1 else None

                if key == "frame":
                    new_frame_number = int(value)

                    if new_frame_number > frame_number:
                        frame_number = new_frame_number

                # Frame number alone is not enough,
                # So we wait for the fps field (which comes afterwards)
                # Before pushing the info.

                elif key == "fps":
                    fps = float(value)

                    # FIXME : This is extremely promiscuous.
                    # We shouldn't have to mix parsing functionality with sending to pubsub
                    # But as it stands, I see no better way of doing things.

                    # Also, if pubsub *is* none, we basically do all of this for nothing.
                    # But the alternative is specifying another outlet for the ffmpeg -progress output,
                    # And what could it be ?
                    # Better to just sink it here

                    if pubsub is not None:
                        pubsub.send_all_on_topic(
                            "progress",
                            RenderProgress(frame_number, fps)
                        )

            # Once a line is complete, discard the previously parsed one, and assemble the next.
            data = lines[-1]

    finally:
        connection.close()
        sock.close()
