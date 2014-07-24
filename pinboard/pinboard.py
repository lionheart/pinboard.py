import operator
import requests
import urllib2
from dateutil import parser as date_parser

PINBOARD_API_ENDPOINT = "https://api.pinboard.in/v1/"

class Bookmark(object):
    def __init__(self, payload, token):
        self.title = payload['description']
        self.description = payload['extended']
        self.url = payload['href']
        self.meta = payload['meta']
        self.hash = payload['hash']
        self.shared = payload['shared'] == "yes"
        self.toread = payload['toread'] == "yes"
        self.tags = payload['tags'].split(' ')
        self.time = date_parser.parse(payload['time'])
        self.token = token

    @property
    def pinboard(self):
        return Pinboard(self.token)

    @property
    def dt(self):
        return self.time.strftime("%Y-%m-%dT%H:%M:%SZ")

    def __repr__(self):
        parse_result = urllib2.urlparse.urlparse(self.url)
        return "<Bookmark title=\"{}\" url=\"{}\">".format(self.title.encode("utf-8"), parse_result.netloc)

    def save(self, update_time=False):
        params = {
            'url': self.url,
            'description': self.title,
            'extended': self.description,
            'tags': self.tags,
            'shared': "yes" if self.shared else "no",
            'toread': "yes" if self.toread else "no",
        }

        if update_time:
            params['dt'] = self.dt

        return self.pinboard.posts.add(**params)

    def delete(self):
        return self.pinboard.posts.delete(url=self.url)


class Tag(object):
    def __init__(self, key, value):
        self.name = key
        self.count = int(value)

    def __repr__(self):
        return "<Tag name=\"{}\" count={}>".format(self.name, self.count)


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

            if self.components == ["posts", "all"]:
                return map(lambda k: Bookmark(k, self.token), json_response)
            elif self.components in [["posts", "get"], ["posts", "recent"]]:
                json_response['posts'] = map(lambda k: Bookmark(k, self.token), json_response['posts'])
            elif self.components == ["tags", "get"]:
                tags = [Tag(k, v) for k, v in json_response.iteritems()]
                tags.sort(key=operator.attrgetter('name'))
                return tags

            return json_response
        else:
            return response

