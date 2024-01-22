#!/usr/bin/env python3

# System imports
import json
import os
import random
import string
import sys
import time
import urllib

# Downloaded imports
# https://github.com/bear/python-twitter
import twitter
from mastodon import Mastodon

# Local imports
from local_settings import *
from dangerous_generator import *


def do_post_twitter(tweet_text, image_file, image_mime_type):
    if not DO_TWITTER:
        return ''
    api = twitter.Api(consumer_key=MY_CONSUMER_KEY,
        consumer_secret=MY_CONSUMER_SECRET,
        access_token_key=MY_ACCESS_TOKEN_KEY,
        access_token_secret=MY_ACCESS_TOKEN_SECRET
    )
    status = api.PostUpdate(status=tweet_text, media=image_file)
    return "Tweeted: \"{0}\"\n".format(tweet_text)


def do_post_mastodon(tweet_text, image_file, image_mime_type):
    if not DO_MASTODON:
        return ''
    api = Mastodon(
        client_secret = CLIENT_SECRET,
        access_token = ACCESS_TOKEN,
        api_base_url = 'https://botsin.space'
    )
    with open(image_file, 'rb') as f:
        content = f.read(-1)
    media_id = 0
    post_result = api.media_post(
            media_file = content,
            mime_type = image_mime_type,
            description = tweet_text)
    media_id = int(post_result['id'])

    if media_id != 0:
        status = api.status_post(status = tweet_text, media_ids = media_id)
    else:
        status = api.status_post(status = tweet_text)
    return "Tooted: \"{0}\"\n".format(tweet_text)


def lambda_handler(event, context):
    result = ''
    if not DEBUG:
        guess = random.choice(range(ODDS))
    else:
        guess = 0

    if guess == 0:
        generator = DangerousGenerator(BING_API_KEY)
        generator.set_debug(DEBUG)
        if generator.generate_random():
            tweet_text = "It's dangerous to go alone! Take this %s." % generator.get_noun().lower()
            result = "%s // file path %s" % (tweet_text, generator.get_image_path())

            if not DEBUG:
                if DO_TWITTER:
                    try:
                        do_post_twitter(tweet_text, generator.get_image_path(), generator.get_image_mime_type())
                    except:
                        result += "Error posting to Twitter\n"
                if DO_MASTODON:
                    try:
                        do_post_mastodon(tweet_text, generator.get_image_path(), generator.get_image_mime_type())
                    except:
                        result += "Error posting to Mastodon\n"
        else:
            result = "Unable to generate random image: {0}".format(generator.get_error())
    else:
        result += str(guess) + " No, sorry, not this time.\n" #message if the random number fails.

    return {'message': result}


