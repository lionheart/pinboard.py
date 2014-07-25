Pinboard.py
===========

Pinboard.py is an easy-to-use and fully-functional Python wrapper for the Pinboard.in API.

Installation
------------

Pinboard.py is available for download through the Python Package Index (PyPi). You can install it right away using pip or easy_install.

.. code:: bash

   pip install pinboard

No dependencies (besides Python 2.7).

Usage
-----

To get started, you're going to need to get your Pinboard API token from the `password page <https://pinboard.in/settings/password>`_ on the Pinboard website. Once you've got that, you're ready to go.

.. code:: pycon

   >>> import pinboard
   >>> pb = pinboard.Pinboard(api_token)

Once you've done this, you can now use the `pb` object to make calls to the Pinboard API. Here are some examples:

Update
''''''

Returns the most recent time a bookmark was added, updated or deleted.

.. code:: pycon

   >>> pb.posts.update()
   {u'update_time': datetime.datetime(2014, 7, 25, 15, 4, 33)}

Posts
'''''

Add a bookmark:

.. code:: pycon

   >>> pb.posts.add(url="http://google.com/", description="A Great Search Engine", \
           extended="This is a description!", tags=["search", "tools"], shared=True, \
           toread=False)
   {u'result_code': u'done'}

Update a bookmark:

.. code:: pycon

   # First, retrieve the bookmark you'd like to edit
   >>> bookmark = pb.posts.get(url='http://google.com/')['posts'][0]
   >>> bookmark
   <Bookmark description="A Great Search Engine" url="google.com">

   # You can now change description, extended, shared, toread, tags, or time directly with the bookmark object.
   >>> bookmark.description = "Google is pretty awesome"
   >>> bookmark.tags = ["search", "searching"]
   >>> bookmark.save()
   {u'result_code': u'done'}

   # If you want to update the bookmark creation date as well, you'll need to pass in `update_time=True` to the save method
   >>> import datetime
   >>> bookmark.time = datetime.datetime.now() - datetime.timedelta(days=5)
   >>> bookmark.save(update_time=True)

Delete a bookmark:

.. code:: pycon

   >>> pb.posts.delete(url="http://google.com/")
   {u'result_code': u'done'}

Get one or more posts on a single day matching the parameters:

.. code:: pycon

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

.. code:: pycon

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

.. code:: pycon

   >>> pb.posts.dates(tag=["programming", "python"])
   {u'dates': {datetime.date(2008, 12, 5): 1,
     datetime.date(2008, 12, 6): 1,
     ...
     datetime.date(2014, 7, 24): 6,
     datetime.date(2014, 7, 25): 4},
    u'tag': u'programming+python',
    u'user': u'dlo'}

Get all bookmarks in your account:

.. code:: pycon

   >>> pb.posts.all()
   [<Bookmark description="Of Princesses and Dragons" url="medium.com">
    <Bookmark description="A Great Search Engine" url="google.com">,
    ...
    <Bookmark description="Runner Econ 101 - StimHa" url="stimhack.com">,
    <Bookmark description="서인국, 탄탄 근육+ 태평양 어깨…어부바 부른다 : 네이" url="news.naver.com">]

You can also filter by tag, start, results, fromdt, or todt.

.. code:: pycon

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

.. code:: pycon

   >>> pb.posts.suggest(url="https://pinboard.in")
   [{u'popular': [u'pinboard']},
    {u'recommended': [u'bookmark',
      u'bookmarks',
      u'\uc815\ubcf4\ud1b5\uc2e0',
      u'pinboard',
      u'Unread',
      u'webservice']}]

Return all tags in your account along with the number of times they were used:

.. code:: pycon

   >>> pb.tags.get()
   [<Tag name="absurd" count=1>,
    <Tag name="accessibility" count=2>,
    <Tag name="accounting" count=3>,
    <Tag name="zen" count=1>,
    <Tag name="zsh" count=1>,
    <Tag name="zynga" count=1>]

Delete a tag:

.. code:: pycon

   >>> pb.tags.delete(tag="zynga")
   {u'result': u'done'}

Rename a tag:

.. code:: pycon

   >>> pb.tags.rename(old='ppython', new='python')
   {u'result': u'done'}

Miscellaneous
'''''''''''''

By default, pinboard.py will return parsed JSON objects. If you'd like the raw response object for a request, just pass in `parse_response=False`.

.. code:: pycon

   >>> response = pb.tags.get(parse_response=False)
   >>> response
   <addinfourl at 4396047680 whose fp = <socket._fileobject object at 0x105f79850>>
   >>> response.read()
   ... your tags ...

Pinboard.py maps 1-1 to the Pinboard API (e.g., pb.one.two.three() will send a request to "https://api.pinboard.in/v1/one/two/three"). For more information on other methods and usage, please read the `Pinboard API documentation <https://pinboard.in/api/>`_.

One more note--you might have noticed that there is no "title" attribute for bookmarks. This has been done since the Pinboard API calls titles "descriptions" and descriptions "extended" (and this was done to stay consistent with the Delicious API, way back in the day). In order to keep things minimally confusing, this library sticks to how Pinboard names these fields. Just remember--"description" means "title" and "extended" means "description".

TODOs
-----

A command-line utility? Who knows. The future is bright.

License
-------

Apache License, Version 2.0. See `LICENSE <LICENSE>`_ for details.
