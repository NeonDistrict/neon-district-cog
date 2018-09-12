import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import tweepy

from collections import deque

from cakechat.utils.logger import WithLogger
from cakechat.api.response import get_response
from cakechat.config import INPUT_CONTEXT_SIZE, DEFAULT_CONDITION

class TwitterBot(WithLogger):
    """
    Interface for Twitter bot API
    """
    since_id = 0
    user = None

    def __init__(self, consumer_key, consumer_secret, access_token, access_token_secret):
        """
        :param token: consumer_key
        :param token: consumer_secret
        :param token: access_token
        :param token: access_token_secret
        """
        # Configure the API
        self.auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        self.auth.set_access_token(access_token, access_token_secret)
        self.api = tweepy.API(self.auth)

        # Store the user credentials
        self.user = self.api.me()
        self.screen_name = self.user.screen_name

    """
    Get the next tweet
    """
    def findNextTweet(self):
        for tweet in tweepy.Cursor(self.api.search, "to:COG1347", since_id=self.since_id).items():
            try:
                self.since_id = tweet.id
                return tweet
            except tweepy.TweepError as e:
                self._logger.info('Twitter Bot TweepError: {}'.format(e.reason))
                return None
            except StopIteration:
                return None
        return None

    """
    From the messages sent from this bot, get the ID of the last tweet sent
    """
    def determineSinceId(self):
        # Not good enough - assumes that only the bot responds, doesn't account for custom / user posts
        self.since_id = self.api.user_timeline(count = 1)[0]

    def collectResponse(self, tweet_text):
        msg = self.parseMessage(tweet_text)
        context = deque(maxlen=INPUT_CONTEXT_SIZE)
        context.append(msg)
        response = get_response(context, DEFAULT_CONDITION)
        return response
        #context.append(response)
        #self._send_text(response)

    def parseMessage(self, msg_text):
        """
        Parse message text as <@screen_name> [message]
        """
        if not msg_text.startswith('@' + self.screen_name):
            raise ValueError('The command must start with @')

        message = msg_text[len('@' + self.screen_name):].strip()
        return message

    def run(self):
        """
        :param session_class: subclass of AbstractTelegramChat
        """
        self._logger.info('Started Twitter chat bot: @{}'.format(self.screen_name))

        self.determineSinceId()

        while True:
            # Find the next tweet directed at the bot
            tweet = self.findNextTweet()
            if tweet is not None:
                print "Found tweet: " + tweet.text
                response = self.collectResponse(tweet.text)
                print response
                #self.respond(tweet.id, response)
                self.since_id = tweet.id

            # Sleep for five seconds
            time.sleep(5)
