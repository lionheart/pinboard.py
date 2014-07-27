#!/usr/bin/env python

from pinboard import Pinboard
import ConfigParser
import datetime
import os
import unittest

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

    def test_add_and_remove_tag_through_api(self):
        bookmark = self.bookmark()
        bookmark.tags.append("testing")
        bookmark.save()

        updated_bookmark = self.bookmark()
        assert(bookmark.meta != updated_bookmark.meta)

        bookmark = updated_bookmark
        bookmark.tags.remove("testing")
        bookmark.save()

        updated_bookmark = self.bookmark()
        assert(bookmark.meta != updated_bookmark.meta)

    def test_change_privacy_through_api(self):
        bookmark = self.bookmark()
        bookmark.shared = not bookmark.shared
        bookmark.save()

        updated_bookmark = self.bookmark()
        assert(bookmark.meta != updated_bookmark.meta)

        bookmark = updated_bookmark
        bookmark.shared = not bookmark.shared
        bookmark.save()

        updated_bookmark = self.bookmark()
        assert(bookmark.meta != updated_bookmark.meta)

    def test_change_read_status_through_api(self):
        bookmark = self.bookmark()
        bookmark.toread = not bookmark.toread
        bookmark.save()

        updated_bookmark = self.bookmark()
        assert(bookmark.meta != updated_bookmark.meta)

        bookmark = updated_bookmark
        bookmark.toread = not bookmark.toread
        bookmark.save()

        updated_bookmark = self.bookmark()
        assert(bookmark.meta != updated_bookmark.meta)

if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestPinboardAPI)
    unittest.TextTestRunner(verbosity=2).run(suite)

