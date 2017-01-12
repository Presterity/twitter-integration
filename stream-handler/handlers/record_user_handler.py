import boto3
from tweet_type import TweetType
import logging


class RecordUserHandler:
    def __init__(self):
        _dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
        self.table = _dynamodb.Table('Users')
        self.log = logging.getLogger()

    def handle(self, tweet: dict):
        user = tweet.get('user')

        response = self.table.update_item(
            Key={
                'id': user.get('id_str')
            },
            UpdateExpression=
            'set '
            'screen_name = :s, '
            'profile_image_url = :p, '
            'created_at = :c',
            ExpressionAttributeValues={
                ':s': user.get('screen_name'),
                ':p': user.get('profile_image_url'),
                ':c': self.__parse_datetime(user.get('created_at'))
            },
            ReturnValues='ALL_NEW'
        )

        # Take advantage of the fact that dynamo returns the record's attributes
        # Removes need to read record from database in ApplyUserFilterHandler
        record = response['Attributes']
        user_flags = record['user_flags'] or {}
        tweet['presterity_user_flags'] = user_flags

    @staticmethod
    def __parse_datetime(datetime):
        datetime = TweetType.translate_datetime(datetime)
        return datetime.strftime('%Y-%m-%d %H:%M:%S %Z')