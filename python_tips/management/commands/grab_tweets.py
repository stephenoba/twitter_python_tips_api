# -*- coding: utf-8 -*-
import sys

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from core.exceptions import MissingAuthKey
from python_tips.utils import PythonTipFetcher


class Command(BaseCommand):
    help = "Populates the database with tweets."

    def add_arguments(self, parser):
        parser.add_argument(
            "-c",
            "--count",
            type=int,
            default=settings.DEFAULT_REQUEST_COUNT,
            help="Number of tweets to pull. Should be less than 200",
        )
        parser.add_argument(
            "-t",
            "--twitter_id",
            default=settings.DEFAULT_TWITTER_USER_ID,
            dest="twitter_id",
            help="twitter id to pull Tweets from"
        )

    def handle(self, *args, **options):
        count = options.get("count", settings.DEFAULT_REQUEST_COUNT)
        twitter_id = options.get("twitter_id", settings.DEFAULT_TWITTER_USER_ID)

        try:
            fetcher = PythonTipFetcher(user_id=twitter_id, count=count)
        except MissingAuthKey as e:
            raise CommandError(e)

        try:
            self.stdout.write(f"Fetching tweet(s) from @{fetcher.user_id}")
            tweets = fetcher.fetch_tweets()
            self.stdout.write(f"Fetched {len(tweets)} tweet(s) from twitter")
            if len(tweets):
                self.stdout.write("Creating Tips......")
                fetcher.create_tips(tweets)
                self.stdout.write(f"Successfully updated database with {len(tweets)} tips")
                sys.exit(0)
        except Exception as e:
            raise CommandError(e)

        self.stdout.write("Database is up to date.")
        sys.exit(0)
