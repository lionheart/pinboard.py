import requests
import urllib2
from dateutil import parser as date_parser

PINBOARD_API_ENDPOINT = "https://api.pinboard.in/v1/"

class Bookmark(object):
    def __init__(self, payload):
        self.title = payload['description']
        self.description = payload['extended']
        self.url = payload['href']
        self.time = payload['time']
        self.meta = payload['meta']
        self.hash = payload['hash']
        self.shared = payload['shared'] == "yes"
        self.toread = payload['toread'] == "yes"
        self.tags = payload['tags'].split(' ')

    def __repr__(self):
        parse_result = urllib2.urlparse.urlparse(self.url)
        return "<Bookmark title='{}' url='{}'>".format(self.title.encode("utf-8"), parse_result.netloc)


class Pinboard(object):
    BOOLEAN_FIELDS = ["meta", "replace", "shared", "toread"]
    SPACE_DELIMITED_FIELDS = ["tag", "tags"]

    def __init__(self, token):
        self.token = token

    def __getattr__(self, k):
        return PinboardCall(self.token, k)


class PinboardCall(object):
    def __init__(self, token, path):
        self.token = token
        self.components = [path]

    def __getattr__(self, k):
        self.components.append(k)
        return self

    def __call__(self, *args, **kwargs):
        url = "{}{}".format(PINBOARD_API_ENDPOINT, "/".join(self.components))

        parse_json = kwargs.get('parse_json', True)

        params = kwargs.copy()

        if 'parse_json' in params:
            del params['parse_json']

        for field in Pinboard.BOOLEAN_FIELDS:
            if field in kwargs:
                params[field] = kwargs[field] == "yes"

        for field in Pinboard.SPACE_DELIMITED_FIELDS:
            if field in kwargs:
                params[field] = ' '.join(kwargs[field])

        params['format'] = "json"
        params['auth_token'] = self.token

        response = requests.get(url, params=params)

        if parse_json:
            json_response = response.json()

            if 'date' in json_response:
                json_response['date'] = date_parser.parse(json_response['date'])

            if isinstance(json_response, list):
                return map(lambda k: Bookmark(k), json_response)
            elif 'posts' in json_response:
                json_response['posts'] = map(lambda k: Bookmark(k), json_response['posts'])

            return json_response
        else:
            return response

