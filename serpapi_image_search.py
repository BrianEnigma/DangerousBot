#!/usr/bin/env python3

import json
import serpapi
import urllib
import urllib.request


class SerpApiImageSearch:
    def __init__(self, api_key):
        self._api_key = api_key
        self._debug = False

    def set_debug(self, debug):
        self._debug = debug

    def get_image_url(self, search_term):
        result = ''
        params = {
            "engine": "bing_images",
            "q": search_term,
            "count": 1,
            "imagesize": "medium",
            "photo": "transparent",
            "api_key": self._api_key
        }
        client = serpapi.Client(api_key=self._api_key)
        results = client.search(params)
        images_results = results["images_results"]
        try:
            result = images_results[0]['original']
        except IndexError:
            pass
        except:
            pass
        return result

    @staticmethod
    def get_image_bytes_for_url(image_url):
        try:
            req = urllib.request.Request(url=image_url)
            resp = urllib.request.urlopen(req)
            content = resp.read()
            #image_mime_type = resp.info().get_content_type()
            #print("mime_type is " + image_mime_type)
            return content
        except:
            return []

