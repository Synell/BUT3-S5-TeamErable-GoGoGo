from django.test import TestCase

class PlaceStoneTestCase(TestCase):
	def setUp(self):
        self.client = Client()
        self.sample_user = get_user_model().objects.create_user(
            username='testuser',
            email='testemail@sezamail.net',
            password='testpassword123'
        )
		self.client.login(username='testuser', password='testpass')

	def test_placement(self):
		pass

	def test_alternate_placement(self):
		pass

	def test_illegal(self):
		pass