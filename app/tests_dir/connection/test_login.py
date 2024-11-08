from django.test import TestCase
from django.contrib.auth import get_user_model
from ...models.statistic import Statistic

class LogInTestCase(TestCase):
    '''Classe permettant de tester la connexion d'un utilisateur'''
    def setUp(self):
        '''Fonction permettant de preparer le jeu de test'''
        self.statistic = Statistic.objects.create(
            game_win = 0,
            game_loose = 0,
            game_ranked_win = 0,
            game_ranked_loose = 0,
        )
        self.sample_user = get_user_model().objects.create_user(
            username='testuser',
            email='testemail@sezamail.net',
            password='testpassword123',
            stat=self.statistic
        )
        sample_data = {
            "username":'testuser',
            "email":'testemail@sezamail.net',
            "password1":'testpassword123',
            "password2":'testpassword123'
        }
        response = self.client.post('/register', sample_data)
        self.login_data = {
            'username':'testuser',
            'password':'testpassword123'
        }

    def test_successful_login(self):
        '''Fonction permettant de tester la connexion d'un utilisateur'''
        response = self.client.post('/login', self.login_data)
        self.assertEqual(response.status_code, 302)