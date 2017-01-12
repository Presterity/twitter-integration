import boto3
from tweet_type import TweetType


class WriteToDynamoHandler:
    def __init__(self):
        _dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
        self.table = _dynamodb.Table('Tweets')

    def handle(self, tweet: dict):
        user = tweet['user']
        self.table.put_item(
            Item={
                'user': user['id_str'],
                'id': tweet['id_str'],
                'text': tweet['text'],
                'created_at': self.__parse_datetime(tweet['created_at']),
                'in_reply_to_screen_name': tweet.get('in_reply_to_screen_name'),
                'in_reply_to_status_id': tweet.get('in_reply_to_status_id_str'),
                'user_info': {
                    'screen_name': user.get('screen_name'),
                    'profile_image_url': user.get('profile_image_url'),
                    'presterity_user_flags': tweet.get('presterity_user_flags')
                },
                'presterity_actions': tweet.get('presterity_actions')
            }
        )

    @staticmethod
    def __parse_datetime(datetime):
        _datetime = TweetType.translate_datetime(datetime)
        return _datetime.strftime('%Y-%m-%d %H:%M:%S %Z')
