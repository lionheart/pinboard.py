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

   # Retrieve all tags
   >>> pb.tags.get()

License
-------

Apache License, Version 2.0. See `LICENSE <LICENSE>`_ for details.
