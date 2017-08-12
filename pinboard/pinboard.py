# Copyright 2014-2017 Lionheart Software LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import datetime
import json
import operator
import urllib.request, urllib.parse, urllib.error
import urllib.request, urllib.error, urllib.parse
import logging

from . import exceptions

PINBOARD_API_ENDPOINT = "https://api.pinboard.in/v1/"
PINBOARD_DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%SZ"
PINBOARD_ALTERNATE_DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
PINBOARD_DATE_FORMAT = "%Y-%m-%d"

class Bookmark(object):
    def __init__(self, payload, token):
        self.description = payload['description']
        self.extended = payload['extended']
        self.url = payload['href']
        self.meta = payload['meta']
        self.hash = payload['hash']
        self.shared = payload['shared'] == "yes"
        self.toread = payload['toread'] == "yes"
        self.tags = payload['tags'].split(' ')
        self.time = Pinboard.datetime_from_string(payload['time'])
        self.token = token

    def __eq__(self, other):
        return other.hash == self.hash

    def __ne__(self, other):
        return other.meta != self.meta

    def __gt__(self, other):
        return self.time > other.time

    def __lt__(self, other):
        return self.time < other.time

    def __ge__(self, other):
        return self.time >= other.time

    def __le__(self, other):
        return self.time <= other.time

    @property
    def pinboard(self):
        return Pinboard(self.token)

    def __repr__(self):
        parse_result = urllib.parse.urlparse(self.url)
        return "<Bookmark description=\"{}\" url=\"{}\">".format(self.description.encode("utf-8"), parse_result.netloc)

    def save(self, update_time=False):
        params = {
            'url': self.url,
            'description': self.description.encode("utf-8"),
            'extended': self.extended,
            'tags': self.tags,
            'shared': "yes" if self.shared else "no",
            'toread': "yes" if self.toread else "no",
        }

        if update_time:
            params['dt'] = self.time

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
    DATE_FIELDS = ["dt", "date", "update_time", "created_at", "updated_at"]
    BOOLEAN_FIELDS = ["replace", "shared", "toread"]
    SPACE_DELIMITED_FIELDS = ["tag", "tags"]

    def __init__(self, token):
        self.token = token

    def __getattr__(self, k):
        return PinboardCall(self.token, k)

    @staticmethod
    def date_from_string(value):
        return datetime.datetime.strptime(value, PINBOARD_DATE_FORMAT).date()

    @staticmethod
    def string_from_date(d):
        return d.strftime(PINBOARD_DATE_FORMAT)

    @staticmethod
    def datetime_from_string(value):
        try:
            return datetime.datetime.strptime(value, PINBOARD_DATETIME_FORMAT)
        except ValueError:
            return datetime.datetime.strptime(value, PINBOARD_ALTERNATE_DATETIME_FORMAT)

    @staticmethod
    def string_from_datetime(dt):
        return dt.strftime(PINBOARD_DATETIME_FORMAT)


class PinboardCall(object):
    def __init__(self, token, path):
        self.token = token
        self.components = [path]

    def __getattr__(self, k):
        self.components.append(k)
        return self

    def __getitem__(self, k):
        self.components.append(k)
        return self

    def __call__(self, *args, **kwargs):
        url = "{}{}".format(PINBOARD_API_ENDPOINT, "/".join(self.components))

        parse_response = kwargs.get('parse_response', True)

        if 'parse_response' in kwargs:
            del kwargs['parse_response']

        params = kwargs.copy()

        for field in Pinboard.DATE_FIELDS:
            if field in kwargs:
                try:
                    params[field] = Pinboard.string_from_datetime(kwargs[field])
                except:
                    params[field] = kwargs[field]

        for field in Pinboard.BOOLEAN_FIELDS:
            if field in kwargs:
                if isinstance(kwargs[field], bool):
                    params[field] = "yes" if kwargs[field] else "no"
                else:
                    params[field] = kwargs[field]

        for field in Pinboard.SPACE_DELIMITED_FIELDS:
            if field in kwargs:
                if isinstance(kwargs[field], list):
                    params[field] = ' '.join(kwargs[field])
                else:
                    params[field] = kwargs[field]

        params['format'] = "json"
        params['auth_token'] = self.token

        if 'meta' in params:
            params['meta'] = 1 if kwargs['meta'] else 0

        query_string = urllib.parse.urlencode(params)
        final_url = "{}?{}".format(url, query_string)

        try:
            request = urllib.request.Request(final_url)
            opener = urllib.request.build_opener(urllib.request.HTTPSHandler)
            response = opener.open(request)
        except urllib.error.HTTPError as e:
            error_mappings = {
                401: exceptions.PinboardAuthenticationError,
                403: exceptions.PinboardForbiddenError,
                500: exceptions.PinboardServerError,
                503: exceptions.PinboardServiceUnavailable,
            }
            if e.code in error_mappings:
                Error = error_mappings[e.code]
                raise Error(e.url, e.code, e.msg, e.hdrs, e.fp)
            raise
        else:
            if parse_response:
                json_response = json.load(response)

                for field in Pinboard.DATE_FIELDS:
                    if field in json_response:
                        json_response[field] = Pinboard.datetime_from_string(json_response[field])

                if self.components == ["posts", "all"]:
                    return [Bookmark(k, self.token) for k in json_response]
                elif self.components in [["posts", "get"], ["posts", "recent"]]:
                    json_response['posts'] = [Bookmark(k, self.token) for k in json_response['posts']]
                elif self.components == ["posts", "dates"]:
                    json_response['dates'] = {Pinboard.date_from_string(k): int(v) \
                            for k, v in list(json_response['dates'].items())}
                elif self.components == ["posts", "update"]:
                    return json_response['update_time']
                elif self.components == ["tags", "get"]:
                    tags = [Tag(k, v) for k, v in list(json_response.items())]
                    tags.sort(key=operator.attrgetter('name'))
                    return tags
                elif self.components == ["notes", "list"]:
                    for note in json_response['notes']:
                        for field in Pinboard.DATE_FIELDS:
                            if field in note:
                                note[field] = Pinboard.datetime_from_string(note[field])
                elif 'result_code' in json_response:
                    if json_response['result_code'] == "done":
                        return True
                    else:
                        raise exceptions.PinboardError(json_response['result_code'])

                return json_response
            else:
                return response

