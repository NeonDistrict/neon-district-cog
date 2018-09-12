import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import argparse

from cakechat.utils.env import init_theano_env

init_theano_env(is_dev=True)

from cakechat.utils.twitter_bot_client import TwitterBot

if __name__ == '__main__':
    argparser = argparse.ArgumentParser()
    argparser.add_argument('--consumer_key', required=True, help='Twitter Consumer Key')
    argparser.add_argument('--consumer_secret', required=True, help='Twitter Consumer Key Secret')
    argparser.add_argument('--access_token', required=True, help='Twitter Access Token')
    argparser.add_argument('--access_token_secret', required=True, help='Twitter Access Token Secret')

    args = argparser.parse_args()

    TwitterBot(consumer_key=args.consumer_key, 
        consumer_secret=args.consumer_secret, 
        access_token=args.access_token,
        access_token_secret=args.access_token_secret).run()
