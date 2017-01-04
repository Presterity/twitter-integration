"""
Example program for using Twitter Stream API. Prints messages for particular user ids
or for 'social' track as fast as possible. Use -h for help.

From:
https://github.com/ideoforms/python-twitter-examples/blob/master/twitter-stream-extract-links.py
https://github.com/sixohsix/twitter/blob/master/twitter/stream_example.py
"""

import argparse
import logging
import sys
from typing import List

import twitter 

from tweet_type import TweetType


log = None

DEFAULT_CONFIG_FILE = './config.py'
TWITTER_API = None

def ensure_api(config: dict=None) -> twitter.Api:
    """Return authenticated Twitter API instance, instantiating if necessary."""
    global TWITTER_API
    if TWITTER_API is None:
        log.debug("Initializing API")
        TWITTER_API = twitter.Api(
            consumer_key=config['consumer_key'],
            consumer_secret=config['consumer_secret'],
            access_token_key=config['access_key'],
            access_token_secret=config['access_secret'])
        try:
            TWITTER_API.VerifyCredentials(include_entities=False, skip_status=True)
            log.debug("Twitter account verified")
        except twitter.TwitterError as ex:
            log.error("Twitter account verification failed for provided credentials: %s", ex)
            sys.exit(1)
    return TWITTER_API

def handle_tweet(tweet) -> None:
    """Print out type of tweet and, if text tweet, the contents."""
    if not tweet:
        print('-- None -- ')
    elif TweetType.is_timeout(tweet):
        print('-- Timeout --')
    elif TweetType.is_heartbeat_timeout(tweet):
        print('-- Heartbeat Timeout --')
    elif TweetType.is_hangup(tweet):
        print('-- Hangup --')
    else:
        print(TweetType.get_text(tweet))

def handles_to_ids(handles: List[str]) -> List[int]:
    """Convert up to 100 Twitter user names to ids.

    :param handles: list of strings that are twitter handles (do not include '@'
    :return: list of integers that are twitter ids for provided handles
    :raise: ValueError if more than 100 handles are provided

    The limit of 100 is an API limit. If necessary, this function
    can be updated to make requests in batches, but for now, it
    complains if more than 100 handles are provided.
    """
    num_handles = len(handles)
    if num_handles > 100:
        raise ValueError("Cannot lookup ids for more than 100 twitter handles.")
    handles = [hndl[1:] if hndl.startswith('@') else hndl for hndl in handles]
    log.debug("Getting ids for handles: %s", handles)
    user_objs = ensure_api().UsersLookup(screen_name=handles)
    ids = [user_obj.id for user_obj in user_objs]
    log.debug("Ids: %s", ids)
    return ids

def listen(user_ids: List[int]=None) -> None:
    """Connect to Twitter Stream API and listen for tweets from specified users.
    
    :param user_ids: optional list of ints or strings that are twitter user ids
    """
    query_args = {'languages': ['en']}
    if user_ids:
        log.debug("Listening for tweets from user_ids %s", user_ids)
        query_args['follow'] = [str(uid) for uid in user_ids]
    else:
        log.debug("Listening for tweets in 'social' track'")
        query_args['track'] = 'social'
    for tweet in ensure_api().GetStreamFilter(**query_args):
        handle_tweet(tweet)

def load_config(cfg_filename: str) -> dict:
    """"Load our API credentials."""
    log.info("Loading config from %s", cfg_filename)
    config = {}
    exec(open(cfg_filename).read(), config)
    return config

def build_parser() -> argparse.ArgumentParser:
    """Construct argument parser for script.

    :return: ArgumentParser
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--config', default=DEFAULT_CONFIG_FILE,
                        help='Location of config file with auth tokens; default is {0}'.format(
            DEFAULT_CONFIG_FILE))
    parser.add_argument('--handle', action='append', 
                        help='Twitter handle to listen for; may appear multiple times')
    parser.add_argument('--id', action='append', 
                        help='Twitter user id to listen for; may appear multiple times')
    parser.add_argument('--verbose', '-v', action='store_true', help='log level DEBUG')
    return parser


if __name__ == '__main__':
    parser = build_parser()
    args = parser.parse_args()

    # Log at WARN overall; DEBUG is very verbose for python-twitter code
    logging.basicConfig(level=logging.WARN)
    log_level = logging.INFO
    if args.verbose:
        log_level = logging.DEBUG
    log = logging.getLogger(__name__)
    log.setLevel(log_level)

    config = load_config(args.config)
    ensure_api(config=config)

    ids = args.id or []
    if args.handle:
        ids.extend(handles_to_ids(args.handle))

    listen(user_ids=ids)
    sys.exit(0)
