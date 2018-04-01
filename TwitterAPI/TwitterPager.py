__author__ = "geduldig"
__date__ = "June 8, 2013"
__license__ = "MIT"

from requests.exceptions import ConnectionError, ReadTimeout, SSLError
from requests.packages.urllib3.exceptions import ReadTimeoutError, ProtocolError
from .TwitterError import *
import requests
import time

RATE_LIMIT_CODE = 88


class TwitterPager(object):
    """Continuous (stream-like) pagination of response from Twitter REST API resource.

    :param api: An authenticated TwitterAPI object
    :param resource: String with the resource path (ex. search/tweets)
    :param params: Dictionary of resource parameters
    """

    def __init__(self, api, resource, params=None):
        self.api = api
        self.resource = resource
        self.params = params

    def get_iterator(self, wait=0, new_tweets=False):
        """Iterate response from Twitter REST API resource. Resource is called
        in a loop to retrieve consecutive pages of results.

        :param wait: Floating point number (default=0) of seconds wait between requests.
                     Depending on the resource, appropriate values are 5 or 60 seconds.
                     UPDATE: the default was changed to 0 because the pager now handles rate limit
        :param new_tweets: Boolean determining the search direction.
                           False (default) retrieves old results.
                           True retrieves current results.

        :returns: JSON objects containing statuses, errors or other return info.
        :raises: TwitterRequestError
        """
        elapsed = 0
        while True:
            try:
                # get one page of results
                start = time.time()
                r = self.api.request(self.resource, self.params)
                json = r.json()

                # if rate limit reached, go to sleep
                if 'errors' in json and json['errors'][0]['code'] == RATE_LIMIT_CODE:
                    reset = r.get_quota()['reset'] + 5  # plus 5 seconds just to be sure
                    time_to_wait = max(int(reset - time.time()), 0)
                    logging.info(
                        'Rate limit reached for endpoint {0}. Going to sleep for {1} seconds'.format(
                            self.resource, time_to_wait))
                    time.sleep(time_to_wait)
                    continue  # go to the beginning of the loop. try the request again

                it = r.get_iterator()
                if new_tweets:
                    it = reversed(list(it))

                # yield each item in the page
                id = None
                for item in it:
                    if type(item) == dict:
                        if 'id' in item:
                            id = item['id']
                        if 'code' in item:
                            if item['code'] in [130, 131]:
                                # Twitter service error
                                raise TwitterConnectionError(item)
                    yield item

                # if a cursor is present, use it to get next page
                # (otherwise, use id to get next page)
                cursor = -1
                if new_tweets and 'previous_cursor' in json:
                    cursor = json['previous_cursor']
                elif not new_tweets and 'next_cursor' in json:
                    cursor = json['next_cursor']

                # bail when no more results
                if cursor == 0:
                    break
                elif cursor == -1 and not new_tweets and id is None:
                    break

                # sleep before getting another page of results
                elapsed = time.time() - start
                pause = wait - elapsed if elapsed < wait else 0
                time.sleep(pause)

                # waiting for new results to come in
                if id is None:
                    continue

                # use either id or cursor to get a new page
                if cursor != -1:
                    self.params['cursor'] = cursor
                elif new_tweets:
                    self.params['since_id'] = str(id)
                else:
                    self.params['max_id'] = str(id - 1)

            except TwitterRequestError as e:
                if e.status_code < 500:
                    raise
                continue
            except TwitterConnectionError:
                continue
