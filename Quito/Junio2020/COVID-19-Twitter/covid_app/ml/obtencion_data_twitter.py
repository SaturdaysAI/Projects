#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Obtencion de datos de Twitter

from datetime import datetime as dt
from datetime import timedelta
from time import sleep
from re import sub
import json
import tweepy
import time
import csv
import string
import os
from unidecode import unidecode
import configparser

consumer_key = "*********"
consumer_secret = "*********"
access_token = "*********"
access_token_secret = "***********"

folder_path = os.path.dirname(os.path.abspath(__file__)) + os.path.sep

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

query = 'covid19 OR covid-19 OR pandemia OR depresion OR tristeza OR ansiedad OR suicidio'


# Cuenca
geo = '-2.892183,-79.0243995,8km'

# Guayaquil
#geo = '-2.151122,-79.9321841,8km'

# QuitoSur
#geo = '-0.2774566,-78.5333677,8km'
# QuitoCentro
#geo = '-0.191419,-78.4884011,8km'
# QuitoNorte
#geo = '-0.113248,-78.4810111,8km'



#file_name = folder_path + query.lower().replace(' ', '_') + '.csv'
file_name = folder_path + 'covid_.csv'
writer = csv.writer(open(file_name, 'a+'), delimiter='|', quotechar='"')

config = configparser.ConfigParser()

config_file = '{}config.ini'.format(folder_path)

config.read(config_file)

number_of_runs = int(config['DEFAULT']['number_of_runs'])

run_count = int(config['DEFAULT']['run_count'])

max_id = int(config['DEFAULT']['max_id']
             ) if config['DEFAULT']['max_id'] != 'None' else None

until = dt.strptime(config['DEFAULT']['until_date'], '%Y-%m-%d %H:%M:%S'
                    ) if config['DEFAULT']['until_date'] != 'None' else dt.now()


print('number_of_runs ::: {}'.format(number_of_runs))
print('run_count ::: {}'.format(run_count))
print('max_id ::: {}'.format(max_id))
print('until_date ::: {}'.format(until))


def clean_tweet(text):
    '''
    - Limpieza de tuits con expresiones regulares para eliminar caracteres especiales
    '''
    punctuation = string.punctuation.replace(
        ',', '').replace(';', '').replace('.', '')
    return sub('[{}]*|(\w+:\/\/\S+)'.format(string.punctuation), '', unidecode(text)).strip()


def get_tweets(api, query, max_id, until):
    tweets = 0
    cursor = tweepy.Cursor(api.search,
                    q=query+' -filter:retweets',
                    count=100,
                    max_id=max_id,
                    until=dt.strftime(until, '%Y-%m-%d'),
                    tweet_mode='extended',
                    geocode=geo,
                    include_entities=False,
                    monitor_rate_limit=True,
                    wait_on_rate_limit=True,
                    lang="es").items()

    for tweet in cursor:
        tweets = tweets + 1
        print(tweet.id)

        tweet_geo_coordinates = tweet.geo['coordinates'] if tweet.geo else ''
        tweet_coordinates_coordinates = tweet.coordinates['coordinates'] if tweet.coordinates else ''
        tweet_place_place_type = tweet.place.place_type if tweet.place else ''
        tweet_place_name = tweet.place.name if tweet.place else ''
        tweet_place_full_name = tweet.place.full_name if tweet.place else ''
        tweet_full_text = clean_tweet(tweet.full_text)
        tweet_user_id_str = str(tweet.user.id_str)
        tweet_user_id = str(tweet.user.id)
        tweet_id = str(tweet.id)

        line = [
            tweet_id,
            tweet.created_at,
            tweet_geo_coordinates,
            tweet_coordinates_coordinates,
            tweet_user_id,
            tweet_user_id_str,
            tweet.user.name,
            tweet.user.screen_name,
            tweet.user.location,
            tweet.user.created_at,
            tweet.user.geo_enabled,
            tweet_place_place_type, tweet_place_name, tweet_place_full_name,
            tweet.lang, tweet.source,
            tweet_full_text,
            ]

        writer.writerow(line)

        max_id = tweet.id - 1
        until = tweet.created_at

    return max_id, until, tweets


while(True):
    run_count = run_count + 1

    max_id, until, tweets = get_tweets(api, query, max_id, until)

    config['DEFAULT']['max_id'] = str(max_id)
    config['DEFAULT']['until_date'] = dt.strftime(until, '%Y-%m-%d %H:%M:%S')

    with open(config_file, 'w') as configfile:
        config.write(configfile)

    if tweets <= 0:
        break

    if run_count >= number_of_runs:
        break
