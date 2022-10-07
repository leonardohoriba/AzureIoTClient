from decouple import config

# --  Socket Configuration

# Server port
PORT = 2323
# Server address
SERVER = config("SERVER", default="127.0.0.1")
# Message format
FORMAT = "utf-8"
# Length of message
HEADER = 64
# ffmpeg command
FFMPEG_COMMAND = [
        "ffmpeg",
        "-thread_queue_size",
        "1",
        "-re",
        "-f",
        "rawvideo",
        "-pix_fmt",
        "bgr24",
        "-r",
        "25",
        "-s",
        "640x480",
        "-i",
        "-",
        "-ar",
        "44100",
        "-ac",
        "2",
        "-acodec",
        "pcm_s16le",
        "-f",
        "s16le",
        "-ac",
        "2",
        "-i",
        "/dev/zero",
        "-acodec",
        "aac",
        "-ab",
        "64k",
        "-strict",
        "experimental",
        "-vcodec",
        "h264",
        "-pix_fmt",
        "yuv420p",
        "-g",
        "50",
        "-vb",
        "1024k",
        "-profile:v",
        "baseline",
        "-preset",
        "ultrafast",
        "-r",
        "25",
        "-f",
        "flv",
        "rtmp://x.rtmp.youtube.com/live2/ect7-wqu9-tpce-qp22-d81u",
    ]