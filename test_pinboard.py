#!/usr/bin/env python

from pinboard import Pinboard
import ConfigParser
import datetime
import os
import unittest
import functools
import time

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

        raw_input("Click enter after adding a tag to this bookmark through the website ({}...)".format(bookmark.url[:20]))

        updated_bookmark = self.bookmark()
        assert(bookmark.meta != updated_bookmark.meta)

    def test_remove_tag_through_website(self):
        bookmark = self.bookmark()

        raw_input("Click enter after removing a tag from this bookmark through the website ({}...)".format(self.url[:20]))

        updated_bookmark = self.bookmark()
        assert(bookmark.meta != updated_bookmark.meta)


class TestPinboardAPI(unittest.TestCase):
    def setUp(self):
        api_token = os.environ.get('PINBOARD_API_TOKEN', None)
        if api_token is None:
            try:
                config_file = os.path.expanduser("~/.pinboardrc")
                config = ConfigParser.RawConfigParser()
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

    def retry_until_true(self, fun):
        """
        Retries a test until it resolves to True, backing off and doubling
        the time in between retries.
        """
        seconds = 1
        while seconds < 16:
            result = fun()

            suffix = "s" if seconds != 1 else ""
            self.assertTrue(result, msg="Meta failed to update after {} second{}.".format(seconds, suffix))

            if result:
                break
            else:
                time.sleep(seconds)
                seconds *= 2

    def ensure_last_update_time_changed(fun):
        """
        Wraps a test to make sure that the update time changed after
        bookmarks were edited
        """
        @functools.wraps(fun)
        def inner(self):
            update_time_1 = self.pinboard.posts.update()

            fun(self)

            update_time_2 = self.pinboard.posts.update()
            self.assertTrue(update_time_2 > update_time_1)

        return inner

    @ensure_last_update_time_changed
    def test_add_and_remove_tag_through_api(self):
        bookmark = self.bookmark()
        bookmark.tags.append("testing")
        bookmark.save()

        updated_bookmark = self.bookmark()
        self.retry_until_true(lambda: bookmark <> updated_bookmark)

        bookmark = updated_bookmark
        bookmark.tags.remove("testing")
        bookmark.save()

        updated_bookmark = self.bookmark()
        self.retry_until_true(lambda: bookmark <> updated_bookmark)

    @ensure_last_update_time_changed
    def test_change_privacy_through_api(self):
        bookmark = self.bookmark()
        bookmark.shared = not bookmark.shared
        bookmark.save()

        updated_bookmark = self.bookmark()
        self.retry_until_true(lambda: bookmark <> updated_bookmark)

        bookmark = updated_bookmark
        bookmark.shared = not bookmark.shared
        bookmark.save()

        updated_bookmark = self.bookmark()
        self.retry_until_true(lambda: bookmark <> updated_bookmark)

    @ensure_last_update_time_changed
    def test_change_read_status_through_api(self):
        bookmark = self.bookmark()
        bookmark.toread = not bookmark.toread
        bookmark.save()

        updated_bookmark = self.bookmark()
        self.retry_until_true(lambda: bookmark <> updated_bookmark)

        bookmark = updated_bookmark
        bookmark.toread = not bookmark.toread
        bookmark.save()

        updated_bookmark = self.bookmark()
        self.retry_until_true(lambda: bookmark <> updated_bookmark)

        last_updated = self.pinboard.posts.update()

if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestPinboardAPI)
    unittest.TextTestRunner(verbosity=2).run(suite)

