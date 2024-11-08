from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from ...models import Statistic, Tournament, GameConfiguration
from datetime import date

class RankViewTest(TestCase):
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

    def test_global_ranking(self):
        response = self.client.get('/classement-global')
        self.assertEqual(response.status_code, 200)
        
    def test_tournament_ranking(self):
        game_config = GameConfiguration.objects.create(
            is_private=False, ranked=False, map_size=19, komi=6.5, counting_method="Territory",
            clock_type="Fisher", clock_value=300, byo_yomi=30, handicap=None
        )
        tournament = Tournament.objects.create(
            name="Test Tournament",
            register_date=date.today(),
            start_date=date.today(),
            end_date=date.today(),
            organisator="Organizer",
            code="123456",
            description="Tournament Description",
            creator=self.user,
            game_configuration=game_config,
            player_min=4,
            start=False,
            private=False,
        )
        response = self.client.get('/classement-tournament/'+str(tournament.id)+"/")
        self.assertEqual(response.status_code, 200)