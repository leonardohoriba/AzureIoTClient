import os


def signal_handler(signal, frame):
    print("SIGTERM received.")
    os._exit(0)
