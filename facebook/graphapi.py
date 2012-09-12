# -*- coding: utf-8
import urllib

from tornado import gen
from tornado.httpclient import HTTPRequest, AsyncHTTPClient
import logging

log = logging.Logger(__name__)


try:
    import json
except ImportError:
    import simplejson as json


class GraphAPI(object):
    def __init__(self, access_token=None):
        self.access_token = access_token

    def get_object(self, uid, callback):
        """
        Fetchs given `uid` object from the graph.

        uid -- object's facebook graph id
        callback -- function to be called when the async request data is ready
        """
        self.request(uid, callback=callback)

    def put_object(self, profile_id, name, callback, **kwargs):
        """
        Writes given `name` object to the graph, connected to `uid`
        """

        self.request("{0}/{1}".format(profile_id, name), 'POST', body=kwargs,
                     callback=callback)

    def delete_object(self, uid, callback):
        """
        Deletes a object via it's identifier `uid`
        """
        self.request(uid, 'DELETE', callback=callback)

    def post_wall(self, message, profile_id='me', callback=None, **kwargs):
        kwargs['message'] = message
        self.request("{0}/feed".format(profile_id), 'POST', body=kwargs,
                     callback=callback)

    @gen.engine
    def request(self, path, method="GET", query=None, body=None,
                callback=None):
        """
        Makes request on `path` in the graph.

        path -- endpoint to the facebook graph api
        method -- GET, POST, etc
        body -- message body
        callback -- function to be called when the async request finishes
        """
        if not query:
            query = {}

        if self.access_token:
            if body is not None:
                body["access_token"] = self.access_token
            else:
                query["access_token"] = self.access_token

        query_string = urllib.urlencode(query) if query else ""
        body = urllib.urlencode(body) if body else None

        url = "https://graph.facebook.com/" + path 
        if query_string:
            url += "?" + query_string
        log.debug(url)

        client = AsyncHTTPClient()
        request = HTTPRequest(url, method=method, body=body)
        response = yield gen.Task(client.fetch, request)

        content_type = response.headers.get('Content-Type')
        if 'text' in content_type:
            data = json.loads(response.body)
        elif 'image' in content_type:
            data = {
                "data": response.body,
                "mime-type": content_type,
                "url": response.request.url,
            }
        else:
            raise GraphAPIError('Maintype was not text or image')

        if data and isinstance(data, dict) and data.get("error"):
            raise GraphAPIError(data)
        callback(data)


class GraphAPIError(Exception):
    def __init__(self, result):
        self.result = result
        try:
            self.type = result["error_code"]
        except:
            self.type = ""

        # OAuth 2.0 Draft 10
        try:
            self.message = result["error_description"]
        except:
            # OAuth 2.0 Draft 00
            try:
                self.message = result["error"]["message"]
            except:
                # REST server style
                try:
                    self.message = result["error_msg"]
                except:
                    self.message = result

        Exception.__init__(self, self.message)
