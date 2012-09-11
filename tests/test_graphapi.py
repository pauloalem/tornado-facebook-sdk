from tornado import testing
from facebook import facebook
from tornado.ioloop import IOLoop
from tests import test_user_id, test_app_key

class GraphAPITestCase(testing.AsyncTestCase):

    def get_new_ioloop(self):
        return IOLoop.instance()

    def test_get_object(self):
        graph = facebook.GraphAPI(test_app_key)
        graph.get_object('{0}'.format(test_user_id), callback=self.stop)
        response = self.wait()
        expected = {
            u'first_name': u'Will', 
            u'last_name': u'Sharpeescu', 
            u'middle_name': u'Amdddkccjaa',
            u'name': u'Will Amdddkccjaa Sharpeescu', 
            u'locale': u'pt_BR', 
            u'gender': u'male', 
            u'link': u'http://www.facebook.com/people/Will-Amdddkccjaa-Sharpeescu/100004440033011',
            u'id': u'100004440033011'
        }
        self.assertDictEqual(expected, response)

    def test_invalid_key_assert_raises_graph_api_error(self):
        with self.assertRaises(facebook.GraphAPIError):
            graph = facebook.GraphAPI('notavalidkey')
            graph.get_object('/{0}'.format(test_user_id), callback=self.stop)
            self.wait()
