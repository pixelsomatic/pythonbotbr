# Python Bot 

Python Bot is an automated content aggregator that gathers all content related to the Python programming language within the Portuguese-speaking developer community on Twitter.

This project was created during free time available at the time. Please do not expect anything highly documented or a super complex project, it's just a hobby, where you are welcome to contribute :)

## Installation

Use the [pip](https://pip.pypa.io/en/stable/) package manager to install the project dependencies.

```
pip install -r requirements.txt
```

## Usage

This project use [Tweepy](https://docs.tweepy.org/en/stable/) to connect with 
To use the bot, you'll need to follow these steps:

1. Create a [Twitter](https://developer.twitter.com/apply-for-access) account for the bot and generate Twitter API credentials.
2. Clone this repository and install the dependencies.

```
git clone https://github.com/pixelsomatic/pythonbotbr.git
```

3. Open the `config.py` file and add your API credentials.

```python
def create_api():
    consumer_key = "[your_consumer_key]"
    consumer_secret = "[your_consumer_secret]"
    access_token = "[your_access_token]"
    access_token_secret = "[access_token_secret]"

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True,
        wait_on_rate_limit_notify=True)
    try:
        api.verify_credentials()
    except Exception as e:
        logger.error("Erro criando a API", exc_info=True)
        raise e
    logger.info("API criada")
    return api
```

4. Edit the `python_bot.py` file with the desired keywords.
5. Next, you have to activate your virtual environment and run the bot’s main file, bot/pythonbot.py:

```bash
$ source ./venv/bin/activate
$ python bot/pythonbot.py
```

## Examples

Below are some examples that you can build using the same Tweepy library and Python programming language.

```python
#!/usr/bin/env python
# tweepy-bots/bots/favretweet.py

import tweepy
import logging
from config import create_api
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

class FavRetweetListener(tweepy.StreamListener):
    def __init__(self, api):
        self.api = api
        self.me = api.me()

    def on_status(self, tweet):
        logger.info(f"Processing tweet id {tweet.id}")
        if tweet.in_reply_to_status_id is not None or \
            tweet.user.id == self.me.id:
            # This tweet is a reply or I'm its author so, ignore it
            return
        if not tweet.favorited:
            # Mark it as Liked, since we have not done it yet
            try:
                tweet.favorite()
            except Exception as e:
                logger.error("Error on fav", exc_info=True)
        if not tweet.retweeted:
            # Retweet, since we have not retweeted it yet
            try:
                tweet.retweet()
            except Exception as e:
                logger.error("Error on fav and retweet", exc_info=True)

    def on_error(self, status):
        logger.error(status)

def main(keywords):
    api = create_api()
    tweets_listener = FavRetweetListener(api)
    stream = tweepy.Stream(api.auth, tweets_listener)
    stream.filter(track=keywords, languages=["en"])

if __name__ == "__main__":
    main(["Python", "Tweepy"])
```

In the Python Bot, a Tweepy stream is created to filter tweets that are in Portuguese and include the keyword "Python". The on_status() of the stream listener processes the tweets from the stream. This method receives a tweet object and uses the favorite() method to mark the tweet as liked, since the bot has not done it yet. The bot also retweets the tweet using the retweet() method, since it has not retweeted it yet.

To avoid retweeting and liking tweets that are replies to other tweets, on_status() checks if in_reply_to_status_id is not None. Additionally, the bot does not retweet and like its own content by checking if tweet.user.id is not equal to the bot's own user id.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## Licença
[MIT](https://choosealicense.com/licenses/mit/)
