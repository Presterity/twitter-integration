import logging


class ApplyUserFilterHandler:

    def __init__(self):
        self.log = logging.getLogger()

    def handle(self, tweet: dict):
        if tweet.get('presterity_action') is None:
            tweet['presterity_action'] = {}

        user_flags = tweet.get('presterity_user_flags')
        if user_flags is None:
            return

        if 'user_blocked' in user_flags:
            self.log.info('Blocked user detected: %s', tweet['user'].get('screen_name'))
            tweet['presterity_action']['hidden'] = 'blocked_user'
        if 'user_promoted' in user_flags:
            self.log.info('Promoted user detected: %s', tweet['user'].get('screen_name'))
            tweet['presterity_action']['promoted'] = 'promoted_user'

