from threading import Thread
import logging
from tweet_type import TweetType


class TwitterStreamListener:

    def __init__(self, stream):
        self.stream = stream
        self.listener_thread = None
        self.handlers = []
        self.status = 'Stopped'
        self.stop_listener = False
        self.log = logging.getLogger()

    def register_handler(self, handler):
        self.handlers.append(handler)

    def get_status(self):
        return self.status

    def start(self):
        if self.status != 'Stopped':
            raise ValueError('Status=Stopped is required to Start. Instead Status=%s', self.status)
        if self.listener_thread is not None:
            raise ValueError('It appears that a listener is already running')
        if len(self.handlers) < 1:
            raise ValueError('No handlers are registered.')

        self.log.info('Starting listener')
        self.listener_thread = Thread(target=self.__listen__)
        self.listener_thread.start()
        self.log.info('Started')
        self.status = 'Running'

    def stop(self):
        if self.status != 'Running':
            raise ValueError('Status=Running is required to Stop. Instead Status=%s', self.status)
        if self.listener_thread is None:
            raise ValueError('It appears that there is no listener running')

        self.log.info('Stopping listener')
        self.status = 'Stopping'
        self.stop_listener = True
        self.listener_thread.join()
        self.listener_thread = None
        self.status = 'Stopped'
        self.log.info('Listener stopped')

    def __listen__(self):
        for tweet in self.stream:
            if TweetType.is_hangup_or_timeout(tweet):
                continue

            for handler in self.handlers:
                try:
                    handler.handle(tweet)
                except Exception as e:
                    self.log.error('Failure running handler %s on tweet %s. Exception message:%n%s',
                                   handler.__class__.__name__, tweet, e)

            if self.stop_listener:
                self.log.info('Stop detected in thread')
                break
