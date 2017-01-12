"""
Utility class to help understand data returned from Twitter API.
"""

from typing import Optional
from datetime import datetime


class TweetType(object):
    Timeout = {'timeout': True}
    Hangup = {'hangup': True}
    HeartbeatTimeout = {'hangup': True, 'heartbeat_timeout': True}

    @classmethod
    def is_hangup(cls, tweet_dict: dict) -> bool:
        """Return True if provided dict looks like any type of hangup.

        Note that a heartbeat timeout is a kind of hangup.
        """
        return tweet_dict and tweet_dict is cls.Hangup

    @classmethod
    def is_heartbeat_timeout(cls, tweet_dict: dict) -> bool:
        """Return True if provided dict looks like heartbeat timeout."""
        return tweet_dict and tweet_dict is cls.HeartbeatTimeout

    @classmethod
    def is_timeout(cls, tweet_dict: dict) -> bool:
        """Return True if provided dict looks like timeout."""
        return tweet_dict and tweet_dict is cls.Timeout

    @classmethod
    def is_hangup_or_timeout(cls, tweet_dict: dict) -> bool:
        return cls.is_hangup(tweet_dict) \
               or cls.is_heartbeat_timeout(tweet_dict) \
               or cls.is_timeout(tweet_dict)

    @classmethod
    def get_text(cls, tweet_dict: dict) -> Optional[str]:
        """Return text or None."""
        text = None
        if tweet_dict:
            text = tweet_dict.get('text')
        # Convert empty string to None for consistency
        return text or None

    @staticmethod
    def translate_datetime(tweet_datetime: str):
        _format = '%a %b %d %H:%M:%S %z %Y'
        return datetime.strptime(tweet_datetime, _format)