# -*- coding: utf-8
#  Copyright 2012 Paulo Alem<biggahed@gmail.com>
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at

#    http://www.apache.org/licenses/LICENSE-2.0

#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import urllib

from tornado import gen
from tornado.httpclient import HTTPRequest, AsyncHTTPClient
import logging


try:
    import json
except ImportError:
    import simplejson as json

GRAPH_URL = "https://graph.facebook.com/"

class GraphAPI(object):


    def __init__(self, access_token=None):
        self.access_token = access_token

    def get_object(self, uid, query=None, **kwargs):
        """
        Fetchs given `uid` object from the graph.

        uid -- object's facebook graph id
        """
        query = query or {}
        self._make_request(uid, method='GET', query=query, **kwargs)

    def put_object(self, uid, name, body=None, **kwargs):
        """
        Writes given `name` object to the graph, connected to `uid`
        """
        body = body or {}
        self._make_request("{0}/{1}".format(uid, name), method='POST',
                body=body, **kwargs)

    def delete_object(self, uid, **kwargs):
        """
        Deletes a object via it's identifier `uid`
        """
        self._make_request(uid, method='DELETE', **kwargs)

    def fql(self, fql, **kwargs):
        """
        Queries the graph api using the facebook query language

        fql -- a string(simple query) or dictionary(in case you want do do a multiquery)
        query -- A dictionary that becomes a query string to be appended to the path
        method -- GET, POST, etc
        body -- message body
        callback -- function to be called when the async request finishes
        """

        query = kwargs.get('query', {})
        query['q'] = fql

        self._make_request('fql', query=query, **kwargs)

    def post_wall(self, message, profile_id='me', body=None, **kwargs):
        #XXX move to separate User class?
        body = body or {}
        body['message'] = message
        self._make_request("{0}/feed".format(profile_id), method='POST',
                body=body, **kwargs)

    def api(self, path, **kwargs):
        self._make_request(path, **kwargs)

    @gen.engine
    def _make_request(self, path, query=None, method="GET", body=None,
                callback=None):
        """
        Makes request on `path` in the graph.

        path -- endpoint to the facebook graph api
        query -- A dictionary that becomes a query string to be appended to the path
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

        url = GRAPH_URL + path
        if query_string:
            url += "?" + query_string

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
            raise GraphAPIError('Maintype was not text nor image')

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
