import boto3


dynamodb = boto3.resource('dynamodb', region_name='us-west-2')

table = dynamodb.create_table(
    TableName='Tweets',
    KeySchema=[
        {
            'AttributeName': 'user',
            'KeyType': 'HASH'  # Partition key
        },
        {
            'AttributeName': 'id',
            'KeyType': 'RANGE'  # Sort key
        }
    ],
    AttributeDefinitions=[
        {
            'AttributeName': 'user',
            'AttributeType': 'S'
        },
        {
            'AttributeName': 'id',
            'AttributeType': 'S'
        }
    ],
    ProvisionedThroughput={
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    }
)

print("Table status:", table.table_status)