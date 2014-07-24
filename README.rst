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

Retrieve All Bookmarks
^^^^^^^^^^^^^^^^^^^^^^

.. code:: pycon

   >>> pb.posts.all()

Retrieve a single bookmark
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: pycon

   >>> bookmark = pb.posts.all(results=1)[0]
   <Bookmark title="Of Princesses and Dragons — Medium" url="medium.com">

   >>> bookmark.time
   datetime.datetime(2014, 7, 21, 11, 11, 59)

   # Make a change to a bookmark and save it
   >>> bookmark.title = "Of Princesses and Dragons"
   >>> bookmark.tags = ["blogs", "interesting"]
   >>> bookmark.save()
   {u'result_code': u'done'}

   # You can also save a bookmark without a bookmark object
   >>> pb.posts.add(url="http://google.com/", description="A Great Search Engine", tags=["search", "tools"])
   {u'result_code': u'done'}

   # If you want to update the bookmark creation date as well, you'll need to pass in `update_time=True` to the save method
   >>> import datetime
   >>> bookmark.time = datetime.datetime.now() - datetime.timedelta(days=5)
   >>> bookmark.save(update_time=True)

   # Retrieve all tags
   >>> pb.tags.get()

   # By default, the Pinboard object will return parsed JSON objects. If you'd like the raw response object, just pass in `parse_response=False`
   >>> response = pb.tags.get(parse_response=False)
   >>> response
   <addinfourl at 4396047680 whose fp = <socket._fileobject object at 0x105f79850>>
   >>> response.read()
   ... your tags ...

Pinboard.py maps 1-1 to the Pinboard API. For more information on other methods and usage, please read the `Pinboard API documentation <https://pinboard.in/api/>`_.


License
-------

Apache License, Version 2.0. See `LICENSE <LICENSE>`_ for details.
