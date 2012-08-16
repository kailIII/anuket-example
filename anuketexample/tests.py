import os
import sys
import unittest

from paste.deploy.loadwsgi import appconfig
from pyramid import testing


# minimum settings for tests
here = os.path.abspath(os.path.dirname(__file__))
settings = {
    'pyramid.available_languages': 'en fr',
    'mako.directories':
        ('{0}/../anuketexample/templates'.format(here),
        'anuket:templates'),
    'sqlalchemy.url': 'sqlite:///anuket-example.test.db',
    'anuket.brand_name': 'Example',
}


class ViewIntegrationTests(unittest.TestCase):
    """ Integration tests for the views."""
    def setUp(self):
        self.config = testing.setUp()
        # register the routes
        self.config.include('anuketexample.views')

    def tearDown(self):
        testing.tearDown()

    def test_routes(self):
        """ Test the routes of the views."""
        request = testing.DummyRequest()
        self.assertEqual(request.route_path('hello'), '/hello')
        self.assertEqual(request.route_path('hello_admin'), '/hello/admin')

    def test_hello_world_view(self):
        """ Test the response of the `root_view`."""
        from anuketexample.views import hello_world
        request = testing.DummyRequest()
        response = hello_world(request)
        self.assertEqual(response, {'hello': u'Hello World!'})

    def test_hello_admin_view(self):
        """ Test the response of the `root_view`."""
        from anuketexample.views import hello_admin
        request = testing.DummyRequest()
        response = hello_admin(request)
        self.assertEqual(response, {'hello': u'Hello Admin!'})


class ViewFunctionalTests(unittest.TestCase):
    """ Functional tests for the views."""
    def setUp(self):
        from anuketexample import main
        app = main({}, **settings)
        from webtest import TestApp
        self.testapp = TestApp(app)

    def test_hello_world_page(self):
        """ Test the hello world page response for everybody."""
        response = self.testapp.get('/hello', status=200)
        self.assertTrue('Hello World!' in response.body)

    def test_hello_admin_page(self):
        """ Test than the hello admin page is forbiden for non logged users."""
        response = self.testapp.get('/hello/admin', status=302)
        redirect = response.follow()
        self.assertEqual(redirect.status, '200 OK')
        self.assertEqual(redirect.request.path, '/login')
        self.assertTrue('You are not connected.' in redirect.body)
