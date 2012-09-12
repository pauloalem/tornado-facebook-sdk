from tornado import testing
from facebook import facebook
from tornado.ioloop import IOLoop
from tests import test_user_id, test_app_key

class GraphAPITestCase(testing.AsyncTestCase):

    def get_new_ioloop(self):
        return IOLoop.instance()

    def test_get_object(self):
        graph = facebook.GraphAPI(test_app_key)
        graph.get_object(test_user_id, callback=self.stop)
        response = self.wait()
        expected = {
            u'first_name': u'Helen', 
            u'last_name': u'Martinazzisen',
            u'middle_name': u'Amdcjhcaafjc',
            u'name': u'Helen Amdcjhcaafjc Martinazzisen',
            u'locale': u'pt_BR',
            u'gender': u'female',
            u'link': u'http://www.facebook.com/people/Helen-Amdcjhcaafjc-Martinazzisen/100004308311603',
            u'id': u'100004308311603'
        }
        self.assertDictEqual(expected, response)

    def test_invalid_key_assert_raises_graph_api_error(self):
        with self.assertRaises(facebook.GraphAPIError):
            graph = facebook.GraphAPI('notavalidkey')
            graph.get_object(test_user_id, callback=self.stop)
            self.wait()

    def test_put_object(self):
        graph = facebook.GraphAPI(test_app_key)
        graph.put_object(test_user_id, "feed", self.stop, message="Another message in the Wall")
        response = self.wait()
        import pdb; pdb.set_trace()
