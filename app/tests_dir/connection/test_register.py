from django.test import TestCase

class SignUpTestCase(TestCase):
	'''Classe permettant de tester la creation d'un utilisateur'''
	def setUp(self):
		'''Fonction permettant de preparer le jeu de test'''
		self.sample_data = {
			'username': 'testuser',
			'email': 'testemail@sezamail.net',
			'password1': 'testpassword123',
			'password2': 'testpassword123',
		}

	def test_successful(self):
		'''Fonction permettant de tester la creation d'un utilisateur lors d'une réussite'''
		response = self.client.post('/register', self.sample_data)
		self.assertEqual(response.status_code, 302)

	def test_failed(self):
		'''Fonction permettant de tester la creation d'un utilisateur lors d'une echec'''
		invalid_sample = {
			'username':'testuser2',
			'email':'testemail@sezamail.net',
			'password1': 'testpassword123',
			'password2': 'error',
		}
		response = self.client.post('/register',invalid_sample)
		self.assertEqual(response.status_code, 400)