# twitter-integration
Offline tools for collecting, archiving, and organizing tweets.
Uses https://python-twitter.readthedocs.io/en/latest/


## Python development environment requirements
* Python 3: http://docs.python-guide.org/en/latest/dev/virtualenvs/
* virtualenv: http://docs.python-guide.org/en/latest/dev/virtualenvs/


## presterity/twitter-integration development

1. go to preferred workspace directory
2. `virtualenv -p python3 venvs/presterity`
3. `source venvs/presterity/bin/activate`
4. `git clone git@github.com:/presterity/twitter-integration`
5. `pip install -r twitter-integration/requirements.txt`


## Using the Twitter APIs

1. Follow the instructions at https://python-twitter.readthedocs.io/en/latest/getting_started.html to register a Twitter app.
2. Under "Keys and Access Tokens," generate Consumer Key and Secret
3. Copy your consumer key/secret and access key/secret into your own version of the config.py file
4. Execute the following command from the root of the repo (to avoid accidentaly checking in your changes to the file) `git update-index --assume-unchanged ./config.py`


## Running stream-listener

1. CD to root of repo
2. `python stream-listener/twitter-stream-listen.py --handle @presterity --verbose`

Notes about the above command:

1. Run `python stream-listener/twitter-stream-listen.py -h` for a help page
2. `python` - If you didn't run `-p python3` option when create the virtualenv workspace, you need to specify `python3` instead `python`. Otherwise, you will get errors immeditately after running.
3. If you don't start the command from the root of the repo, you'll need to specify `--config {path/to/config}`. If your error message is related to accessing `config.py`, this is likely your problem.
4. Pick a different handle than @presterity to listen to something more active. Specify multiple like follows: `--handle @presterity --handle @SenWarren --handle @PramiliaJayapal --handle @BarackObama` ('@' is optional. Leave it off if you want.)
5. I recommend `--verbose` the first time you run it because otherwise you might think the application is hanging (when it's just waiting for someone being watched to tweet). Remove this flag after you know it works for your own sanity.

## Using the AWS APIs

1. Log-in to the AWS Console (You can create an account with your Amazon information if you haven't already. A lot of things are free for the first year. Setting up the Dynamo databases like I do below costs approximately $5 per month if you are not still on the free level)
2. In the IAM section, create a user with programatic access and AmazonDynamoDBFullAccess permissions
3. Create a file in ~/.aws/config and paste in your access key and secret access key in the following format

```
[default]
aws_access_key_id = xxxxxxxxxxxxxxxxxxxxxx
aws_secret_access_key = xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

4. You're all set up. All AWS API calls will find this file automatically and grant permissions accordingly
5. If you have any difficulty, reach out on slack to kyle.parker.robinson

## Creating DynamoDB Tables

The application in stream-handler requires access to two DynamoDB tables. Run the scripts in ./dynamo-tables/ to create them

`python dynamo-tables/create_tweet_table.py`
`python dynamo-tables/create_users_table.py`

If your AWS account is not on the free tier, these tables will accrue charges of around $5 per month for both as long as they exist. You can delete them and recreate them when needed to save costs.

## Running stream-handler

`python3 stream-handler/main.py --handle @BarackObama`

Using BarackObama for testing has been useful because there is a steady stream of people tweeting to him
