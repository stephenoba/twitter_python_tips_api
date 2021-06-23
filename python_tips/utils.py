import re
import logging
import html
import tweepy
from tweepy.error import TweepError

from django.conf import settings

from core.exceptions import MissingAuthKey, InvalidAuthKey
from .models import Tip

logger = logging.getLogger(__name__)


def get_most_recent_tip():
    """
    helper function to get most recent tweet id
    """
    tip = Tip.objects.first()
    if not tip:
        return None
    return tip.tweet_id


class PythonTipFetcher(object):
    """
    Used in fetching tips from a twitter account and
    updating Database with tips.
    """
    def __init__(self, user_id=settings.DEFAULT_TWITTER_USER_ID, count=None):
        # set since_id to ensure that the celery job gets only
        # the latest tweets
        self.since_id = get_most_recent_tip()
        self.user_id = user_id
        # count is used to specify the number of tweets to pull in a request
        self.count = count

        self.consumer_key = settings.CONSUMER_KEY
        self.consumer_secret = settings.CONSUMER_SECRET
        self.access_token = settings.ACCESS_TOKEN
        self.access_token_secret = settings.ACCESS_TOKEN_SECRET

        if not all([self.consumer_key, self.consumer_secret, self.access_token, self.access_token_secret]):
            raise MissingAuthKey(
                "One or more Auth Keys are missing.")

        try:
            auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
            auth.set_access_token(self.access_token, self.access_token_secret)
        except TweepError:
            logger.info("Unable to perform authentication")
            raise InvalidAuthKey("Error in authentication, please verify Auth keys from provider.")
        self.api = tweepy.API(auth)

    def fetch_tweets(self):
        if self.count and self.count >= 200:
            # maximum count per request is 200
            raise ValueError(f"Count can not be greater than 200")
        tweets = self.api.user_timeline(
            screen_name=self.user_id,
            count=self.count,
            since_id=self.since_id,
            include_rts=False,
            tweet_mode='extended'
        )
        return tweets

    def create_tips(self, tweets):
        for tweet in tweets:
            full_text = html.unescape(tweet.full_text)
            data = {
                "tweet_id": tweet.id,
                "full_text": self.clean_text(full_text),
                "num_retweets": tweet.retweet_count,
                "num_likes": tweet.favorite_count,
                "timestamp": tweet.created_at,
            }
            tip = Tip(**data)
            tip.save()
            self.create_links(tip, tweet.entities.get("urls", None), tweet.entities.get("media", None)),
        logger.info(f"DB updated with {Tip.objects.all().count()} Tips......")

    @staticmethod
    def create_links(tip, links, media_links):
        if links:
            for link in links:
                link.pop('expanded_url')
                link.pop('indices')
                tip.links.create(**link)
        if media_links:
            # since we are not displaying media fies, we get the
            # url to the tweet from the first media file instead of looping
            # through the list
            media = media_links[0]
            tip.links.create(
                url=media["url"],
                display_url=media['display_url'])

    @staticmethod
    def clean_text(text):
        """
        removes all links from tip

        :param text:
        :return:
        """
        cleaned_text = re.sub(r'http\S+', '<see link below>', text)
        return cleaned_text
