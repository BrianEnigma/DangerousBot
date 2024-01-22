#!/usr/bin/env python3

import json
import urllib
import urllib.request


class BingImageSearch:
    API_ENDPOINT = 'https://api.bing.microsoft.com/v7.0/images/search'

    def __init__(self, api_key):
        self._api_key = api_key
        self._debug = False

    def set_debug(self, debug):
        self._debug = debug

    def get_image_url(self, search_term, min_height=0, only_transparent=False):
        result = ''
        url = BingImageSearch.API_ENDPOINT + '?'
        url += 'count=1&'
        if min_height != 0:
            url += "minHeight=%d&" % min_height
        if only_transparent:
            url += 'imageType=Transparent&'
        url += 'q=' + urllib.parse.quote(search_term, safe='')
        if self._debug:
            print(url)

        req = urllib.request.Request(url=url, headers={'Ocp-Apim-Subscription-Key': self._api_key})
        try:
            resp = urllib.request.urlopen(req)
        except urllib.error.HTTPError as err:
            if 401 != err.code:
                raise err
            return ''

        content = resp.read()
        try:
            j = json.loads(content)
            result = j['value'][0]['contentUrl']
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

