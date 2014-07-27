Pinboard.py
===========

.. https://circleci.com/gh/lionheart/pinboard.py/tree/master.png?circle-token=d50700e1c75836063a7951f80ab1913cf6447acf
.. image:: https://api.travis-ci.org/lionheart/pinboard.py.svg


.. image:: http://img.shields.io/pypi/dm/pinboard.png?style=flat


.. image:: http://img.shields.io/pypi/l/pinboard.png?style=flat


.. image:: http://img.shields.io/pypi/v/pinboard.png?style=flat

Pinboard.py is an easy-to-use and fully-functional Python wrapper and `command-line utility <#command-line>`_ for the Pinboard.in API.

Installation
------------

Pinboard.py is available for download through the Python Package Index (PyPi). You can install it right away using pip or easy_install.

.. code-block:: bash

   pip install pinboard

No dependencies (besides Python 2.7).

Usage
-----

To get started, you're going to need to get your Pinboard API token from the `password page <https://pinboard.in/settings/password>`_ on the Pinboard website. Once you've got that, you're ready to go.

.. code-block:: pycon

   >>> import pinboard
   >>> pb = pinboard.Pinboard(api_token)

Once you've done this, you can now use the `pb` object to make calls to the Pinboard API. Here are some examples:

Update
''''''

Returns the most recent time a bookmark was added, updated or deleted.

.. code-block:: pycon

   >>> pb.posts.update()
   datetime.datetime(2014, 7, 27, 18, 11, 29)

Posts
'''''

Add a bookmark:

.. code-block:: pycon

   >>> pb.posts.add(url="http://google.com/", description="A Great Search Engine", \
           extended="This is a description!", tags=["search", "tools"], shared=True, \
           toread=False)
   True

Update a bookmark:

.. code-block:: pycon

   # First, retrieve the bookmark you'd like to edit
   >>> bookmark = pb.posts.get(url='http://google.com/')['posts'][0]
   >>> bookmark
   <Bookmark description="A Great Search Engine" url="google.com">

   # You can now change description, extended, shared, toread, tags, or time directly with the bookmark object.
   >>> bookmark.description = "Google is pretty awesome"
   >>> bookmark.tags = ["search", "searching"]
   >>> bookmark.save()
   True

   # If you want to update the bookmark creation date as well, you'll need to pass in `update_time=True` to the save method
   >>> import datetime
   >>> bookmark.time = datetime.datetime.now() - datetime.timedelta(days=5)
   >>> bookmark.save(update_time=True)

Delete a bookmark:

.. code-block:: pycon

   >>> pb.posts.delete(url="http://google.com/")
   True

Get one or more posts on a single day matching the parameters:

.. code-block:: pycon

   >>> pb.posts.get(url="http://google.com/")
   {u'date': datetime.datetime(2014, 7, 25, 16, 35, 25),
    u'posts': [<Bookmark description="A Great Search Engine" url="google.com">],
    u'user': u'dlo'}

   >>> import datetime
   >>> pb.posts.get(dt=datetime.date.today())
   {u'date': datetime.datetime(2014, 7, 25, 16, 35, 25),
    u'posts': [<Bookmark description="A Great Search Engine" url="google.com">,
     <Bookmark description="Smooth Scrolling | CSS-Tricks" url="css-tricks.com">,
     <Bookmark description="Apple "Frustrated" that "People Don't Want to Pay Anything" on Mobile, Says 'The Banner Saga' Developer | Touch Arcade" url="toucharcade.com">],
    u'user': u'dlo'}

Return all recent bookmarks (optionally filtering by tag):

.. code-block:: pycon

   >>> pb.posts.recent(tag=["programming", "python"])
   {u'date': datetime.datetime(2014, 4, 28, 2, 7, 58),
    u'posts': [<Bookmark description="itunesfs 1.0.0.7 : Python Package Index" url="pypi.python.org">,
     <Bookmark description="mincss "Clears the junk out of your CSS" - Peterbe.com" url="www.peterbe.com">,
     <Bookmark description="Braintree Test Credit Card Account Numbers" url="www.braintreepayments.com">,
     <Bookmark description="Valued Lessons: Monads in Python (with nice syntax!)" url="www.valuedlessons.com">,
     <Bookmark description="Paste #EGY1XPQxQ2UPuT91SH83 at spacepaste" url="bpaste.net">,
     <Bookmark description="40 Random Letters and Numbers" url="gist.github.com">,
     <Bookmark description="PEP 3156 -- Asynchronous IO Support Rebooted" url="www.python.org">,
     <Bookmark description="Brython" url="www.brython.info">,
     <Bookmark description="Django REST framework" url="django-rest-framework.org">,
     <Bookmark description="mypy - A New Python Variant with Dynamic and Static Typing" url="www.mypy-lang.org">,
     <Bookmark description="Julython 2012" url="www.julython.org">,
     <Bookmark description="Stripe Blog: Exploring Python Using GDB" url="stripe.com">,
     <Bookmark description="Python FAQ: Descriptors - fuzzy notepad" url="me.veekun.com">,
     <Bookmark description="A Guide to Python's Magic Methods « rafekettler.com" url="www.rafekettler.com">,
     <Bookmark description="Melopy" url="prezjordan.github.com">,
     <Bookmark description="litl/rauth" url="github.com">],
    u'user': u'dlo'}

Return a list of dates with the number of posts at each date:

.. code-block:: pycon

   >>> pb.posts.dates(tag=["programming", "python"])
   {u'dates': {datetime.date(2008, 12, 5): 1,
     datetime.date(2008, 12, 6): 1,
     ...
     datetime.date(2014, 7, 24): 6,
     datetime.date(2014, 7, 25): 4},
    u'tag': u'programming+python',
    u'user': u'dlo'}

Get all bookmarks in your account:

.. code-block:: pycon

   >>> pb.posts.all()
   [<Bookmark description="Of Princesses and Dragons" url="medium.com">
    <Bookmark description="A Great Search Engine" url="google.com">,
    ...
    <Bookmark description="Runner Econ 101 - StimHa" url="stimhack.com">,
    <Bookmark description="서인국, 탄탄 근육+ 태평양 어깨…어부바 부른다 : 네이" url="news.naver.com">]

You can also filter by tag, start, results, fromdt, or todt.

.. code-block:: pycon

   >>> import datetime
   >>> five_days_ago = datetime.datetime.now() - datetime.timedelta(days=5)
   >>> pb.posts.all(tag=["programming"], start=10, results=100, fromdt=five_days_ago)
   [<Bookmark description="Of Princesses and Dragons" url="medium.com">
    <Bookmark description="A Great Search Engine" url="google.com">,
    ...
    <Bookmark description="Runner Econ 101 - StimHa" url="stimhack.com">,
    <Bookmark description="서인국, 탄탄 근육+ 태평양 어깨…어부바 부른다 : 네이" url="news.naver.com">]

Tags
''''

Suggest tags for a given URL:

.. code-block:: pycon

   >>> pb.posts.suggest(url="https://pinboard.in")
   [{u'popular': [u'pinboard']},
    {u'recommended': [u'bookmark',
      u'bookmarks',
      u'\uc815\ubcf4\ud1b5\uc2e0',
      u'pinboard',
      u'Unread',
      u'webservice']}]

Return all tags in your account along with the number of times they were used:

.. code-block:: pycon

   >>> pb.tags.get()
   [<Tag name="absurd" count=1>,
    <Tag name="accessibility" count=2>,
    <Tag name="accounting" count=3>,
    <Tag name="zen" count=1>,
    <Tag name="zsh" count=1>,
    <Tag name="zynga" count=1>]

Delete a tag:

.. code-block:: pycon

   >>> pb.tags.delete(tag="zynga")
   True

Rename a tag:

.. code-block:: pycon

   >>> pb.tags.rename(old='ppython', new='python')
   True

Miscellaneous
'''''''''''''

By default, pinboard.py will return parsed JSON objects. If you'd like the raw response object for a request, just pass in `parse_response=False`.

.. code-block:: pycon

   >>> response = pb.tags.get(parse_response=False)
   >>> response
   <addinfourl at 4396047680 whose fp = <socket._fileobject object at 0x105f79850>>
   >>> response.read()
   ... your tags ...

Pinboard.py maps 1-1 to the Pinboard API (e.g., pb.one.two.three() will send a request to "https://api.pinboard.in/v1/one/two/three"). For more information on other methods and usage, please read the `Pinboard API documentation <https://pinboard.in/api/>`_.

One more note--you might have noticed that there is no "title" attribute for bookmarks. This has been done since the Pinboard API calls titles "descriptions" and descriptions "extended" (and this was done to stay consistent with the Delicious API, way back in the day). In order to keep things minimally confusing, this library sticks to how Pinboard names these fields. Just remember--"description" means "title" and "extended" means "description".

Command-Line
------------

In addition to providing full Python-level support for the Pinboard API, pinboard.py also comes bundled with a handy command-line utility called "pinboard". Just type "pinboard -h" for a full list of supported commands. To get started, type "pinboard login" and have your API token ready.

All of the commands pre-process and indent the JSON output. If you would like to shoot the raw response data to stdout, just pass "--raw" before the subcommand (e.g., "pinboard --raw bookmarks").

Examples:

.. code-block:: sh

   $ pinboard login
   Enter your Pinboard API token: username:XXXXX
   Saved Pinboard credentials to ~/.pinboardrc
   $ pinboard suggest-tags --url http://pymotw.com/2/argparse/
   [
       {
           "popular": [
               "python"
           ]
       },
       {
           "recommended": [
               "python",
               "argument",
               "parsing"
           ]
       }
   ]
   $ pinboard get --date 7-13-2014
   {
       "date": "2014-07-13T03:03:58Z",
       "posts": [
           {
               "extended": "",
               "hash": "e2311835eb0de6bff2595a9b1525bb98",
               "description": "Python 2.7.x and Python 3.x key differences",
               "tags": "python",
               "href": "http://sebastianraschka.com/Articles/2014_python_2_3_key_diff.html",
               "meta": "561d1f53791a8c50109393411f0301fc",
               "time": "2014-07-13T03:03:58Z",
               "shared": "yes",
               "toread": "no"
           },
           {
               "extended": "",
               "hash": "4abe28f70154bd35f84be73cec0c53ef",
               "description": "Miami, the great world city, is drowning while the powers that be look away | World news | The Observer",
               "tags": "",
               "href": "http://www.theguardian.com/world/2014/jul/11/miami-drowning-climate-change-deniers-sea-levels-rising",
               "meta": "2ca547789553ba9d3202a5cd3d367685",
               "time": "2014-07-13T02:53:54Z",
               "shared": "yes",
               "toread": "yes"
           }
       ],
       "user": "dlo"
   }
   $ pinboard --raw get --date 7/13/2014
   {"date":"2014-07-13T03:03:58Z","user":"dlo","posts":[{"href":"http:\/\/sebastianraschka.com\/Articles\/2014_python_2_3_key_diff.html","description":"Python 2.7.x and Python 3.x key differences","extended":"","meta":"561d1f53791a8c50109393411f0301fc","hash":"e2311835eb0de6bff2595a9b1525bb98","time":"2014-07-13T03:03:58Z","shared":"yes","toread":"no","tags":"python"},{"href":"http:\/\/www.theguardian.com\/world\/2014\/jul\/11\/miami-drowning-climate-change-deniers-sea-levels-rising","description":"Miami, the great world city, is drowning while the powers that be look away | World news | The Observer","extended":"","meta":"2ca547789553ba9d3202a5cd3d367685","hash":"4abe28f70154bd35f84be73cec0c53ef","time":"2014-07-13T02:53:54Z","shared":"yes","toread":"yes","tags":""}]}

You can print a full list of pinboard commands by passing the "-h" flag.

.. code-block:: sh

   $ pinboard -h
   usage: pinboard [-h] [--raw]

                   {login,last-update,add,delete,get,recent,dates,bookmarks,suggest-tags,tags,delete-tag,rename-tag,notes,note,rss-key,api-token}
                   ...

   positional arguments:
     {login,last-update,add,delete,get,recent,dates,bookmarks,suggest-tags,tags,delete-tag,rename-tag,notes,note,rss-key,api-token}
       add                 posts/add
       delete              posts/delete
       get                 posts/get
       recent              posts/recent
       dates               posts/dates
       bookmarks           posts/all
       suggest-tags        posts/suggest
       tags                tags/get
       delete-tag          tags/delete
       rename-tag          tags/rename
       notes               notes/list
       note                notes/ID
       rss-key             user/secret
       api-token           user/api_token
   
   optional arguments:
     -h, --help            show this help message and exit
     --raw                 Print the raw data from the Pinboard API without any
                           formatting.

...or help for a specific subcommand by passing the subcommand and then the "-h" flag.

.. code-block:: sh

   $ pinboard bookmarks -h
   usage: pinboard bookmarks [-h] [--from_date FROM_DATE] [--to_date TO_DATE]
                             [--tags TAGS [TAGS ...]] [--count COUNT]
                             [--offset OFFSET]

   optional arguments:
     -h, --help            show this help message and exit
     --from_date FROM_DATE
     --to_date TO_DATE
     --tags TAGS [TAGS ...]
     --count COUNT
     --offset OFFSET

Donate
------

If you like this library, consider supporting me on Gittip.

|gittip|_

.. |gittip| image:: http://img.shields.io/gittip/dlo.png?style=flat
.. _gittip: https://www.gittip.com/dlo/

License
-------

Apache License, Version 2.0. See `LICENSE <LICENSE>`_ for details.

