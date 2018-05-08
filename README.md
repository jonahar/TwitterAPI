This is a modified version of TwitterAPI, to be used by [TwitterMine](https://github.com/jonahar/TwitterMine).  
**Disclaimer**: some files from the original repository were removed, so don't count on this README examples and instructions.  
  
  
  
  
TwitterAPI is a Python package for accessing Twitter's REST APIs and Streaming APIs. It supports OAuth 1.0 and OAuth 2.0 authentication.  And, it works with the latest Python versions in both 2.x and 3.x branches. 

Installation
------------
From the command line::

	pip install TwitterAPI

Documentation
-------------
* `An Introduction <http://geduldig.github.com/TwitterAPI>`_
* `Authentication <http://geduldig.github.com/TwitterAPI/authentication.html>`_
* `Error Handling <http://geduldig.github.com/TwitterAPI/errors.html>`_
* `Paging Results <http://geduldig.github.com/TwitterAPI/paging.html>`_
* `Tiny Examples <http://geduldig.github.com/TwitterAPI/examples.html>`_
* `Fault Tolerant Streams and Pages <http://geduldig.github.com/TwitterAPI/faulttolerance.html>`_

Some Code...
------------
[See `TwitterAPI/examples <https://github.com/geduldig/TwitterAPI/tree/master/examples>`_ for working examples.]

First, authenticate with your application credentials::

	from TwitterAPI import TwitterAPI
	api = TwitterAPI(consumer_key, consumer_secret, access_token_key, access_token_secret)

Tweet something::

	r = api.request('statuses/update', {'status':'This is a tweet!'})
	print(r.status_code)

Get tweet by its id::

	r = api.request('statuses/show/:%d' % 210462857140252672)
	print(r.text)

Get some tweets::

	r = api.request('search/tweets', {'q':'pizza'})
	for item in r:
		print(item)

Stream tweets from New York City::

	r = api.request('statuses/filter', {'locations':'-74,40,-73,41'})
	for item in r:
		print(item)
		
Notice that ``request()`` works with all endpoints found in either the REST APIs or the Streaming APIs. Usually ``request()`` takes two arguments: a Twitter endpoint and a dictionary of endpoint parameters.  The above examples use ``get_iterator()`` to consume each tweet object.  The iterator knows how to iterate results returned from either the REST APIs or the Streaming APIs.  

You also have access to the response object returned by ``request()``.  From a response object ``r`` you can get the raw response with ``r.text`` and the HTTP status code with ``r.status_code``.  See the `requests <http://docs.python-requests.org/en/latest/user/quickstart/>`_ library documentation for more details.

Extra Goodies
-------------
Command-Line Utility (`examples/cli <https://github.com/geduldig/TwitterAPI/blob/master/examples/cli>`_)
