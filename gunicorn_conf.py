import os
from multiprocessing import cpu_count

# current directory path
dir_path = os.path.dirname(os.path.realpath(__name__))

# Socket path
bind = 'unix:/run/txt2video/gunicorn.sock'

# Worker Options
# workers = cpu_count() + 1
workers = 1
worker_class = 'uvicorn.workers.UvicornWorker'

# Logging Options
loglevel = 'debug'
accesslog = '/var/log/txt2video/access.log'
errorlog = '/var/log/txt2video/error.log'
