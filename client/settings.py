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
