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

from tornado import testing
import facebook
from tornado.ioloop import IOLoop
from tests import test_user_id, test_app_key
import time

def create_msg():
    return "Another message in the Wall {}".format(time.time())

class GraphAPITestCase(testing.AsyncTestCase):

    #TODO: create a test user for each run
    # example: POST 256248457829889/accounts/test-users?installed=true&name=John Doe&permissions=publish_stream&method=POST&access_token=256248457829889|VdsmNePcAFQ6wQrMmU6Qmz2FVnw

    def get_new_ioloop(self):
        return IOLoop.instance()

    def test_get_object(self):
        graph = facebook.GraphAPI(test_app_key)
        graph.get_object(test_user_id, callback=self.stop)
        response = self.wait()
        expected = {
            u'first_name': u'John',
            u'last_name': u'Doe',
            u'name': u'John Doe',
            u'locale': u'pt_BR',
            u'gender': u'female',
            u'link': u'http://www.facebook.com/people/John-Doe/100004430523129',
            u'id': u'100004430523129'
        }
        self.assertDictEqual(expected, response)

    def test_invalid_key_assert_raises_graph_api_error(self):
        with self.assertRaises(facebook.GraphAPIError):
            graph = facebook.GraphAPI('notavalidkey')
            graph.get_object(test_user_id, callback=self.stop)
            self.wait()

    def test_put_object(self):
        graph = facebook.GraphAPI(test_app_key)
        graph.put_object(
                test_user_id,
                "feed",
                {'message': create_msg()},
                callback=self.stop)
        response = self.wait()
        self.assertIn('id', response)

    def test_delete_object(self):
        graph = facebook.GraphAPI(test_app_key)

        graph.put_object(
                test_user_id,
                "feed",
                {'message': create_msg()},
                callback=self.stop)
        response = self.wait()
        object_id = response['id']
        graph.delete_object(object_id, callback=self.stop)
        deleted_response = self.wait()
        self.assertTrue(deleted_response)

    def test_post_wall(self):
        graph = facebook.GraphAPI(test_app_key)
        graph.post_wall(create_msg(), profile_id=test_user_id, callback=self.stop)
        response = self.wait()
        self.assertIn('id', response)
        graph.delete_object(response['id'], callback=self.stop)
        deleted_response = self.wait()
        self.assertTrue(deleted_response)

    def test_fql_query(self):
        graph = facebook.GraphAPI(test_app_key)
        graph.fql("select name from user where uid=100004430523129", callback=self.stop)
        response = self.wait()
        self.assertIn('data', response)
        self.assertEqual(len(response['data']), 1)
        self.assertEqual(response['data'][0]['name'], "John Doe")

    def test_fql_multiquery(self):
        graph = facebook.GraphAPI(test_app_key)
        queries = {
            'q1':"select name from user where uid=100004430523129",
            'q2':"select name from user where uid=100004430523129"
        }
        graph.fql(queries, callback=self.stop)
        response = self.wait()
        self.assertIn('data', response)
        self.assertEqual(len(response['data']), 2)
        for q in response['data']:
                self.assertEqual(q['fql_result_set'][0]['name'], "John Doe")

    def test_api(self):
        graph = facebook.GraphAPI(test_app_key)
        graph.api('100004430523129', query={'fields': 'first_name, last_name'}, callback=self.stop)
        response = self.wait()
        self.assertEqual(response['first_name'], "John")
        self.assertEqual(response['last_name'], "Doe")
