#!/usr/bin/env python

from pinboard import Pinboard
import configparser
import datetime
import os
import unittest
import functools
import time
import random
import string

class TestPinboardAPIPropagation(unittest.TestCase):
    def setUp(self):
        self.pinboard = Pinboard(os.environ['PINBOARD_API_TOKEN'])

        response = self.pinboard.posts.recent(count=1, date=datetime.date.today())
        bookmark = response['posts'][0]
        self.url = bookmark.url

    def bookmark(self):
        response = self.pinboard.posts.get(url=self.url, meta="yes")
        return response['posts'][0]

    def test_add_tag_through_website(self):
        bookmark = self.bookmark()

        input("Click enter after adding a tag to this bookmark through the website ({}...)".format(bookmark.url[:20]))

        updated_bookmark = self.bookmark()
        assert(bookmark.meta != updated_bookmark.meta)

    def test_remove_tag_through_website(self):
        bookmark = self.bookmark()

        input("Click enter after removing a tag from this bookmark through the website ({}...)".format(self.url[:20]))

        updated_bookmark = self.bookmark()
        assert(bookmark.meta != updated_bookmark.meta)


class TestPinboardAPI(unittest.TestCase):
    def setUp(self):
        api_token = os.environ.get('PINBOARD_API_TOKEN', None)
        if api_token is None:
            try:
                config_file = os.path.expanduser("~/.pinboardrc")
                config = configparser.RawConfigParser()
                with open(config_file, "r") as f:
                    config.readfp(f)
            except:
                raise
            else:
                api_token = config.get("authentication", "api_token")

        self.pinboard = Pinboard(api_token)

        response = self.pinboard.posts.recent(count=1, date=datetime.date.today())
        bookmark = response['posts'][0]
        self.url = bookmark.url

    def bookmark(self):
        response = self.pinboard.posts.get(url=self.url, meta="yes")
        return response['posts'][0]

    def retry_until_true(self, fun, msg=None, max_seconds=32):
        """
        Retries a test until it resolves to True, backing off and doubling
        the time in between retries.
        """
        seconds = 1
        while seconds < max_seconds:
            result = fun()

            if result:
                # print "\nSucceeded after {} seconds".format(seconds),
                break
            else:
                seconds *= 2
                time.sleep(seconds)
        else:
            if msg:
                self.assertTrue(result, msg="{} ({} second backoff).".format(msg, max_seconds))
            else:
                self.assertTrue(result)

    def ensure_last_update_time_changed(fun):
        """
        Wraps a test to make sure that the update time changed after
        bookmarks were edited
        """
        @functools.wraps(fun)
        def inner(self, *args, **kwargs):
            update_time_1 = self.pinboard.posts.update()

            fun(self, *args, **kwargs)

            update_time_2 = self.pinboard.posts.update()

            self.retry_until_true(lambda: update_time_2 > update_time_1,
                    msg="{} == {}".format(update_time_1, update_time_2),
                    max_seconds=16)

        return inner

    def check_meta_updated(self, bookmark_1, bookmark_2):
        self.retry_until_true(lambda: bookmark_1 != bookmark_2,
                msg="{} == {}".format(bookmark_1.meta, bookmark_2.meta))

    @ensure_last_update_time_changed
    def test_add_and_remove_tag_through_api(self):
        bookmark = self.bookmark()
        bookmark.tags.append("testing")
        bookmark.save()

        updated_bookmark = self.bookmark()
        self.check_meta_updated(bookmark, updated_bookmark)

        bookmark = updated_bookmark
        bookmark.tags.remove("testing")
        bookmark.save()

        updated_bookmark = self.bookmark()
        self.check_meta_updated(bookmark, updated_bookmark)

    @ensure_last_update_time_changed
    def test_change_privacy_through_api(self):
        bookmark = self.bookmark()
        bookmark.shared = not bookmark.shared
        bookmark.save()

        updated_bookmark = self.bookmark()
        self.check_meta_updated(bookmark, updated_bookmark)

        bookmark = updated_bookmark
        bookmark.shared = not bookmark.shared
        bookmark.save()

        updated_bookmark = self.bookmark()
        self.check_meta_updated(bookmark, updated_bookmark)

    @ensure_last_update_time_changed
    def test_change_read_status_through_api(self):
        bookmark = self.bookmark()
        bookmark.toread = not bookmark.toread
        bookmark.save()

        updated_bookmark = self.bookmark()
        self.check_meta_updated(bookmark, updated_bookmark)

        bookmark = updated_bookmark
        bookmark.toread = not bookmark.toread
        bookmark.save()

        updated_bookmark = self.bookmark()
        self.check_meta_updated(bookmark, updated_bookmark)

    @ensure_last_update_time_changed
    def _test_add_bookmark_through_api(self, url):
        self.pinboard.posts.add(url=url, description="Test Bookmark")

    @ensure_last_update_time_changed
    def _test_delete_bookmark_through_api(self, url):
        self.pinboard.posts.delete(url=url)

    def test_add_and_remove_bookmark_through_api(self):
        random_suffix = "".join(random.choice(string.letters) for i in range (6))
        url = "http://example.com/{}".format(random_suffix)

        self._test_add_bookmark_through_api(url)
        self._test_delete_bookmark_through_api(url)

if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestPinboardAPI)
    unittest.TextTestRunner(verbosity=2).run(suite)

