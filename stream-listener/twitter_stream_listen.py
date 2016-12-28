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

import twitter
import twitter.api
from twitter.oauth import OAuth
from twitter.stream import TwitterStream, Timeout, HeartbeatTimeout, Hangup
from twitter.util import printNicely

log = None

DEFAULT_CONFIG_FILE = './config.py'
TWITTER_API = None

def ensure_api(auth=None):
    """Return authenticated Twitter API instance, instantiating if necessary."""
    global TWITTER_API
    if TWITTER_API is None:
        log.debug("Initializing API")
        TWITTER_API = twitter.Twitter(auth=auth)
        try:
            TWITTER_API.account.verify_credentials(include_entities=False, skip_status=True)
            log.debug("Twitter account verified")
        except twitter.api.TwitterHTTPError as ex:
            log.error("Twitter account verification failed for provided credentials: %s", ex)
            sys.exit(1)
    return TWITTER_API

def get_auth(config):
    return OAuth(
        config["access_key"], config["access_secret"], config["consumer_key"], config["consumer_secret"])

def handle_tweet(tweet):
    """Print out type of tweet and, if text tweet, the contents."""
    if tweet is None:
        printNicely("-- None --")
    elif tweet is Timeout:
        printNicely("-- Timeout --")
    elif tweet is HeartbeatTimeout:
        printNicely("-- Heartbeat Timeout --")
    elif tweet is Hangup:
        printNicely("-- Hangup --")
    elif tweet.get('text'):
        printNicely(tweet['text'])
    else:
        printNicely("-- Some data: " + str(tweet))

def handles_to_ids(handles):
    """Convert up to 100 Twitter user names to ids."""
    handle_arg = ','.join(handles[0:min(100,len(handles))])
    log.debug("Getting ids for handles: %s", handle_arg)
    user_objs = ensure_api().users.lookup(screen_name=handle_arg)
    ids = [user_obj['id'] for user_obj in user_objs]
    log.debug("Ids: %s", ids)
    return ids

def listen(user_ids=None, auth=None):
    """Connect to Twitter Stream API and listen for tweets from specified users.
    
    :param user_ids: optional list of ints or strings that are twitter user ids.
    """
    stream = TwitterStream(auth=auth, secure=True)
    query_args = {}
    if user_ids:
        log.debug("Listening for tweets from user ids %s", user_ids)
        query_args['follow'] = ','.join([str(uid) for uid in user_ids])
    else:
        log.debug("Listening for tweets in 'social' track'")
        query_args['track'] = 'social'

    tweet_iter = stream.statuses.filter(**query_args)
    for tweet in tweet_iter:
        handle_tweet(tweet)

def load_config(cfg_filename):
    """"Load our API credentials."""
    log.info("Loading config from %s", cfg_filename)
    config = {}
    exec(open(cfg_filename).read(), config)
    return config

def build_parser():
    """Construct argument parser for script."""
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

    log_level = logging.INFO
    if args.verbose:
        log_level = logging.DEBUG
    logging.basicConfig(level=log_level)
    log = logging.getLogger(__name__)

    config = load_config(args.config)
    auth = get_auth(config)
    ensure_api(auth)

    ids = args.id or []
    if args.handle:
        ids.extend(handles_to_ids(args.handle))

    listen(user_ids=ids, auth=auth)
    sys.exit(0)
