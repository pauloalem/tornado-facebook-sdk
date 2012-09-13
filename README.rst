====================
tornado-facebook-sdk
====================

What is it?
-----------
The tornado-facebook-sdk is a library that aims
to ease the task of writing non-blocking, server side,
facebook social graph accessing code.
It's built using `tornado <https://github.com/facebook/tornado>`_.
This makes tornado-facebook-sdk a perfect fit if you're
developing an application using tornado.

Installing
----------
The prefered way to install is via pip ::

$ pip install tornado-facebook-sdk

From github, for the last version ::

$ pip install git+https://github.com/pauloalem/tornado-facebook-sdk.git

Or you can just download it and install via setup.py, it's up to you.

Using
-----
Getting facebook's public page ::

    from tornado import ioloop
    from facebook import GraphAPI

    ioloop = ioloop.IOLoop.instance()
    graph = GraphAPI()

    # a simple callback that prints social graph responses
    def print_callback(data):
        print data
        ioloop.stop()

    graph.get_object('/facebook', callback=print_callback)

    ioloop.start()

Authenticating with a user auth token and printing it's name ::

    graph = GraphAPI(access_token)

    #do something with the user's data, like print it's first name
    def get_first_name(me):
        print me['first_name']
        ioloop.stop()

    result = graph.get_object('/me', callback=get_first_name)
    ioloop.start()

Posting on an user's wall ::


    def callback(response):
        # ...
    graph.post_wall("Maoe!", callback=callback)

Which is just a shortcut for ::


    def callback(response):
        # ...
    graph.put_object('me', 'feed', message="Maoe!!", callback=callback)


Deleting an object ::

    def callback(response):
        # ...
    graph.delete_object(obj_id, callback=callback)

License
-------
Read LICENSE.txt

History
-------
This library is based on the `facebook-sdk <https://github.com/pythonforfacebook/facebook-sdk/blob/master/facebook.py>`_ library.
Originaly, I was going to use it as it's simple and has a nice
interface, but it's blocking code makes it a no-no.
