from tweet_type import TweetType


class WriteToconsoleHandler:

    @classmethod
    def handle(cls, tweet: dict):
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
