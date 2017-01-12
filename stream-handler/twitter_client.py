import logging
import twitter
from typing import List

DEFAULT_CONFIG_FILE = './config.py'


class TwitterClient:

    def __init__(self, config=None):
        self.log = logging.getLogger()
        if config is None:
            config = DEFAULT_CONFIG_FILE

        self.log.info("Loading config.py from %s", config)
        _config = self.__load_config(config)
        self.log.info("Config loaded")

        self.log.info("Initializing client")
        try:
            self.client = self.__init_client(_config)
            self.log.info("Twitter account verified")
        except twitter.TwitterError as ex:
            self.log.error("Error initializing client: %s", ex)

    @staticmethod
    def __load_config(cfg_filename: str) -> dict:
        """"Load our API credentials."""
        config = {}
        exec(open(cfg_filename).read(), config)
        return config

    @staticmethod
    def __init_client(config: dict) -> twitter.Api:
        _client = twitter.Api(
            consumer_key=config['consumer_key'],
            consumer_secret=config['consumer_secret'],
            access_token_key=config['access_key'],
            access_token_secret=config['access_secret'])

        _client.VerifyCredentials(include_entities=False, skip_status=True)

        return _client

    def get_stream(self, handles: List[str]):
        _user_ids = self.__handles_to_ids(handles)
        _query_args = {
            'languages': ['en'],
            'follow': [str(uid) for uid in _user_ids]
        }
        return self.client.GetStreamFilter(**_query_args)

    def __handles_to_ids(self, handles: List[str]) -> List[int]:
        num_handles = len(handles)
        if num_handles > 100:
            raise ValueError("Cannot lookup ids for more than 100 twitter handles.")
        handles = [hndl[1:] if hndl.startswith('@') else hndl for hndl in handles]
        self.log.info("Getting ids for handles: %s", handles)
        user_objs = self.client.UsersLookup(screen_name=handles)
        ids = [user_obj.id for user_obj in user_objs]
        self.log.info("Ids: %s", ids)
        return ids

