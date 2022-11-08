from decouple import config

# Robot parameters
ROBOT_NAME = config("ROBOT_NAME", default="stingray")

# --  Socket Configuration

# Server port
PORT = 2323
# Server address
SERVER = config("SERVER", default="127.0.0.1")
# Message format
FORMAT = "utf-8"
# Length of message
HEADER = 64
# Sonar parameters
SONAR_MAX_ECHO_PULSE_WIDTH = 30000  #microseconds
# Camera resolution
CAMERA_RESOLUTION_WIDTH = 640   #pixels
CAMERA_RESOLUTION_HEIGHT = 480  #pixels
# Neural network parameters
NEURAL_NETWORK_MINIMUM_CONFIDENCE = 0.5  # must be between 0 and 1
# Streaming parameters
STREAM_BITRATE = 1024  # kilobits per second
STREAM_FFMPEG_COMMAND = ["ffmpeg",
    "-thread_queue_size", "1",
    "-re",
    "-f", "rawvideo",
    "-pix_fmt", "bgr24",
    "-r", "25",
    "-s", f"{CAMERA_RESOLUTION_WIDTH}x{CAMERA_RESOLUTION_HEIGHT}",
    "-i", "-",
    "-ar", "44100",
    "-ac", "2",
    "-acodec", "pcm_s16le",
    "-f", "s16le",
    "-ac", "2",
    "-i", "/dev/zero",
    "-acodec", "aac",
    "-ab", "64k",
    "-strict", "experimental",
    "-vcodec", "h264",
    "-pix_fmt", "yuv420p",
    "-g", "50",
    "-vb", f"{STREAM_BITRATE}k",
    "-profile:v", "baseline",
    "-preset", "ultrafast",
    "-r", "25",
    "-f", "flv",
    config("STREAM_LINK"),
]
# STREAM_LINK must be in .env because it contains the streaming key
