# -*- coding: utf-8
import urllib

from tornado import gen
from tornado.httpclient import HTTPRequest, AsyncHTTPClient


try:
    import json
except ImportError:
    import simplejson as json


class GraphAPI(object):
    def __init__(self, access_token=None):
        self.access_token = access_token

    def get_object(self, path, callback):
        """Fetchs the given object from the graph."""
        self.request(path, callback=callback)

    @gen.engine
    def request(self, path, method="GET", query=None, body=None,
                callback=None):
        """Makes request on `path` in the Graph API.

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

        url = "https://graph.facebook.com/" + path + "?" + query_string

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
