import os
import sys

# python tools/test_api.py -f 127.0.0.1 -p 8080 -c "Hi, Eddie, what's up?"

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cakechat.utils.env import init_theano_env

init_theano_env(is_dev=True)
#init_theano_env()

# All of the react stuff is in this folder
from cakechat.api.v1.server import app

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
