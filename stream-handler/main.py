import logging
import argparse
from twitter_client import TwitterClient
from twitter_stream_listener import TwitterStreamListener

from handlers.write_to_dynamo_handler import WriteToDynamoHandler
from handlers.record_user_handler import RecordUserHandler
from handlers.apply_user_filter_handler import ApplyUserFilterHandler


def build_parser() -> argparse.ArgumentParser:
    """Construct argument parser for script.

    :return: ArgumentParser
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--handle', action='append',
                        help='Twitter handle to listen for; may appear multiple times')
    parser.add_argument('--id', action='append',
                        help='Twitter user id to listen for; may appear multiple times')
    parser.add_argument('--verbose', '-v', action='store_true', help='log level DEBUG')
    return parser

if __name__ != '__main__':
    raise Exception('main.py can only be run as main')

parser = build_parser()
args = parser.parse_args()

# Log at WARN overall; DEBUG is very verbose for python-twitter code
logging.basicConfig(level=logging.WARN)
log_level = logging.INFO
if args.verbose:
    log_level = logging.DEBUG
log = logging.getLogger()
log.setLevel(log_level)

client = TwitterClient()
listener = TwitterStreamListener(client.get_stream(args.handle))

listener.register_handler(RecordUserHandler())
listener.register_handler(ApplyUserFilterHandler())
listener.register_handler(WriteToDynamoHandler())

listener.start()

input('Press Enter to quit')

listener.stop()