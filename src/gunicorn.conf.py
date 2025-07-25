"""
A gunicorn conf file, so that the app can be launched by running
$ gunicorn
"""

import multiprocessing
import socket


def _get_local_private_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ret = s.getsockname()[0]
    s.close()
    return ret


# bind to both local host and local network
bind = ["127.0.0.1", _get_local_private_ip()]
wsgi_app = "app:app"

# use many workers to handle requests concurrently
workers = multiprocessing.cpu_count() * 2 + 1

accesslog = "-"  # write to stdout

timeout = 0
