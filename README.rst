Pinboard.py
===========

Pinboard.py is an easy-to-use and fully-functional Python wrapper for the Pinboard.in API.

Installation
------------

Pinboard.py is available for download through the Python Package Index (PyPi). You can install it right away using pip or easy_install.

.. code:: bash

   pip install pinboard

Usage
-----

To get started, you're going to need to get your Pinboard API token from the `password page <https://pinboard.in/settings/password>`_ on the Pinboard website. Once you've got that, you're ready to go.

.. code:: pycon

   >>> import pinboard
   >>> pb = pinboard.Pinboard(api_token)

Once you've done this, you can now use the `pb` object to make calls to the Pinboard API. Here are some examples:

.. code:: pycon

   # Retrieve all bookmarks
   >>> pb.posts.all()

   # Retrieve a single bookmark
   >>> bookmark = pb.posts.all(results=1)[0]
   <Bookmark title="Of Princesses and Dragons — Medium" url="medium.com">

   # Make a change to a bookmark and save it
   >>> bookmark.title = "Of Princesses and Dragons"
   >>> bookmark.tags = ["blogs", "interesting"]
   >>> bookmark.save()
   {u'result_code': u'done'}

   # You can also save a bookmark without a bookmark object
   >>> pb.posts.add(url="http://google.com/", description="A Great Search Engine", tags=["search", "tools"])
   {u'result_code': u'done'}

   # If you want to update the bookmark creation date, you need to manually override that
   >>> import datetime
   >>> bookmark.time = datetime.datetime.now() - datetime.timedelta(days=5)
   >>> bookmark.save(update_time=True)

   # Retrieve all tags
   >>> pb.tags.get()

In general, Pinboard.py maps 1-1 to the Pinboard API. Please read the `Pinboard API documentation <https://pinboard.in/api/>`_ for other methods and parameters.

License
-------

Apache License, Version 2.0. See `LICENSE <LICENSE>`_ for details.
