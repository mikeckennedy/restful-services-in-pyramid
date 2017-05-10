import unittest

from pyramid import testing


class ViewTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    def test_my_view(self):
        from restful_auto_service.views.home_page import home
        request = testing.DummyRequest()
        info = home(request)
        self.assertEqual(info['project'], 'RESTful Auto Service')


class FunctionalTests(unittest.TestCase):
    def setUp(self):
        from restful_auto_service import main
        app = main({})
        from webtest import TestApp
        self.testapp = TestApp(app)

    def test_root(self):
        res = self.testapp.get('/', status=200)
        self.assertTrue(b'Pyramid' in res.body)
