import celery
from celery.utils.log import get_task_logger

from core.exceptions import PythonTipError
from .utils import PythonTipFetcher

logger = get_task_logger(__name__)


@celery.task
def update_db():
    """
    Update the db with the latest tweets fro @python_tip
    """
    fetcher = PythonTipFetcher(count=199)
    try:
        logger.info(f"Fetching tweet(s) from @{fetcher.user_id}")
        tweets = fetcher.fetch_tweets()
        logger.info(f"Fetched {len(tweets)} tweet(s) from twitter")
        if len(tweets):
            logger.info(f"Creating Tips......")
            fetcher.create_tips(tweets)
    except Exception as e:
        logger.error(e)
        raise PythonTipError(e)
