from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from ...models import Statistic, Tournament, GameConfiguration

class InitTournamentTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.statistic = Statistic.objects.create(
            game_win=0,
            game_loose=0,
            game_ranked_win=0,
            game_ranked_loose=0,
        )
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='testpass',
            email='testuser@example.com',
            stat=self.statistic
        )
        self.client.login(username='testuser', password='testpass')

    def test_main_tournament_page(self):
        response = self.client.get('/tournament')
        self.assertEqual(response.status_code, 200)

    def test_create_tournament_page(self):
        response = self.client.get('/create-tournament')
        self.assertEqual(response.status_code, 200)

    def test_create_tournament(self):
        response = self.client.post('/create-tournament',{
            'tournament-name': 'test name', 
            'tournament-organizer': 'testuser',
            'tournament-desc': '2024-12-22',
            'start-date':'2024-12-22',
            'end-date':'2024-12-22',
            'tournament-player-min':8,
            'tournament-private':True,
            'map-size':9,
            'counting-method':'japanese',
            'byo-yomi':30,
            'clock-type':'japanese',
            'time-clock':'01:00:00',
            'komi':6.5,
            'is-handicap':False,
            'handicap':0,
            'game-private':True
        })
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/tournament/1/')
        self.assertEqual(response.status_code, 200)

        