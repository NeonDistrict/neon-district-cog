import os
import sys
import time
import random

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import tweepy

from collections import deque

from cakechat.utils.logger import WithLogger
from cakechat.api.response import get_response
from cakechat.config import INPUT_CONTEXT_SIZE, DEFAULT_CONDITION

from cog.cog import find_match

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
        super(TwitterBot, self).__init__()

        # Configure the API
        self.auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        self.auth.set_access_token(access_token, access_token_secret)
        self.api = tweepy.API(self.auth)

        # Store the user credentials
        self.user = self.api.me()
        self.screen_name = self.user.screen_name
        self.since_id = 0

    """
    Get the next tweet
    """
    def findNextTweet(self):
        try:
            tweets = self.api.search("@COG1347 -filter:retweets", since_id=self.since_id)
            oldest_tweet = None
            for tweet in tweets:
                if oldest_tweet is None or oldest_tweet.id > tweet.id:
                    oldest_tweet = tweet
            self._logger.info('Next tweet id: {}'.format(str(oldest_tweet.id)))
            return oldest_tweet
        except:
            self._logger.info('No tweets found')

    """
    From the messages sent from this bot, get the ID of the last tweet sent
    """
    def determineSinceId(self):
        # Not good enough - assumes that only the bot responds, doesn't account for custom / user posts
        most_recent_timeline = self.api.user_timeline(count = 10)

        # Review all of the tweets, get the newest that received a response
        for tweet in most_recent_timeline:
            if tweet.in_reply_to_status_id is not None:
                status = self.api.get_status(tweet.in_reply_to_status_id)
                if status is not None and status.text.startswith('@' + self.screen_name):
                    if self.since_id < status.id:
                        self.since_id = status.id
        self._logger.info('Since id: {}'.format(str(self.since_id)))

    def collectResponse(self, tweet_text, tweeter):
        msg = self.parseMessage(tweet_text)
        context = deque(maxlen=INPUT_CONTEXT_SIZE)
        context.append(msg)

        # Need to collect responses from the lines as well
        # -- gifs need to be converted to usable format
        response, _, _ = find_match(msg.encode("utf8"), twitter = True)
        image_filename = None
        if response is None:
            condition = random.choice(['neutral', 'joy', 'anger'])
            response = get_response(context, condition)
            #response = get_response(context, DEFAULT_CONDITION)
            self._logger.info('Respond to tweet ({}) using AI: {}'.format(msg.encode("utf8"), response))

            # Format
            response = "@" + tweeter + " " + response
        else:
            if response.endswith('.gif') or response.endswith('.jpg') or response.endswith('.png'):
                image_filename = response
                
                # Direct to the tweeter
                response = "@" + tweeter
            else:
                # Format
                response = "@" + tweeter + " " + response
            
            self._logger.info('Respond to tweet ({}) using Cog logic: {}'.format(msg.encode("utf8"), response))

        return response, image_filename

    def parseMessage(self, msg_text):
        """
        Parse message text as <@screen_name> [message]
        """
        if not msg_text.startswith('@' + self.screen_name):
            message = msg_text.strip()
            #raise ValueError('The command must start with @')
        else:
            message = msg_text[len('@' + self.screen_name):].strip()

        return message

    def respond(self, tweet_id, response, image_filename = None):
        if image_filename is None:
            self.api.update_status(response, in_reply_to_status_id = tweet_id)
        else:
            filename = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
            image_filename = filename + "/images/" + image_filename
            self.api.update_with_media(image_filename, status = response, in_reply_to_status_id = tweet_id)

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
                try:
                    response, image_filename = self.collectResponse(tweet.text, tweet.author.screen_name)
                    self.respond(tweet.id, response, image_filename)
                    self.since_id = tweet.id
                except:
                    self._logger.info('Error trying to respond to tweet: {}'.format(str(tweet.id)))

            # Sleep for some time
            time.sleep(5)
