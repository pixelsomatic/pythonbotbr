# -*- coding: utf-8 -*-

import tweepy
import logging
from config import create_api


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

class RetweetListener(tweepy.StreamListener):
    def __init__(self, api):
        self.api = api
        self.me = api.me()

    def on_status(self, tweet):
        processing = 'Processando tweet - {}'.format(tweet.text)
        msg = logger.info(processing)
        print(msg)

        if tweet.in_reply_to_status_id is not None or tweet.user.id == self.me.id:
            # Se o tweet é um retweet ou eu sou o autor então ignora
            return
        if tweet.user.id == 1342883800213299202:
            # Teste para bloquear usuário
            return
        keywords = ['cobra','píton','monty','mounty','colt', 'hollywood', 'simpsons', 'serpente','mounty','valadão','serpentes','cobras','monte','tênis','nature','hotmart','crocodile', 'austrália']
        if any(keyword in tweet.text.lower() for keyword in keywords):
            msg = 'Palavra bloqueada de usuário: {} - {}'.format(tweet.user.name, tweet.text)
            warning = logger.info(msg)
            print(warning)
            return
        blocked_id = ['1342883800213299202', '1354378215955943430']
        if any(id in tweet.user.id_str for id in blocked_id):
            msg = 'Spam bloqueado pelo id: {} - {}'.format(tweet.user.name, tweet.text)
            warning = logger.info(msg)
            print(warning)
            return
        blocked_users = ['analytics', 'netcarreiras']
        if any(name in tweet.user.name.lower() for name in blocked_users):
            msg = 'Spam bloqueado pelo nome: {} - {}'.format(tweet.user.name, tweet.text)
            warning = logger.info(msg)
            print(warning)
            return
        if tweet.is_quote_status:
            msg = 'Tweet é um retweet com comentário: {} - {}'.format(tweet.user.name, tweet.text)
            warning = logger.info(msg)
            print(warning)
            return
        if not tweet.favorited:
            try:
                tweet.favorite()
            except:
                logger.error('Erro ao favoritar', exc_info=True)
        if not tweet.retweeted:
            try:
                tweet.retweet()
            except:
                logger.error('Erro ao favoritar e retweetar', exc_info=True)

    def on_error(self, status):
        print(status.text)
        logger.error(status)
        if status == 420:
            return False

api = create_api()
tweets_listener = RetweetListener(api)
stream = tweepy.Stream(auth=api.auth, listener=tweets_listener)
stream.filter(track=['python'], languages=["pt"])
