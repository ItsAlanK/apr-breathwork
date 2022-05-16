from django.test import TestCase


class TestViews(TestCase):
    """ Class for testing home app views """

    def test_get_homepage_response(self):
        """Test response for homepage """
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_check_homepage_templates(self):
        """ Test homepage uses correct templates """
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home/index.html')
