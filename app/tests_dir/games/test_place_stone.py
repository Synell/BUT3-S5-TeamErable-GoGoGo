from django.test import Client
from django.contrib.auth import get_user_model
from django.test import TestCase
from channels.testing import WebsocketCommunicator
from ...models import Statistic, GameConfiguration, GameParticipate, Game
from ...logic import Board
from ...logic.rules import RuleFactory
from ...logic.timer import TimerFactory
from ...channels import GameJoinAndLeave
from datetime import timedelta
import json

class PlaceStoneTestCase(TestCase):
    '''Classe permettant de tester la creation de partie'''
    def setUp(self):
        '''Fonction permettant de preparer le jeu de test'''
        self.client = Client()
        self.statistic = Statistic.objects.create(
            game_win=0,
            game_loose=0,
            game_ranked_win=0,
            game_ranked_loose=0,
        )
        self.user1 = get_user_model().objects.create_user(username='user1', password='password1', stat=self.statistic)
        self.user2 = get_user_model().objects.create_user(username='user2', password='password2', stat=self.statistic)

        self.client.login(username='user1', password='password1')
        #Creation d'une nouvelle partie
        game_config = GameConfiguration.objects.create(
            map_size=9, komi=6.5, counting_method='japanese', clock_type='byo-yomi',
            clock_value=3600, byo_yomi=30,
        )
        game_participate = GameParticipate.objects.create(player1=self.user1, player2=self.user2, score_player1=0, score_player2=0)
        self.game = Game.objects.create(id_game=999, name="Test Game", description="desc", start_date='2023-01-01', duration=60,
                                        move_list='dynamic/games/999.json', game_configuration=game_config,
                                        game_participate=game_participate)
        #Reinitialisation du json de la partie de test

        with open('dynamic/games/999.json', 'w') as f:
            b = Board(
                game_config.map_size,
                game_config.komi,
                RuleFactory().get(game_config.counting_method),
                game_config.byo_yomi,
                timedelta(seconds = game_config.clock_value),
                None,
                TimerFactory().get(game_config.counting_method),
                None,
            )
            json.dump(b.export(), f)


    async def connect(self, communicator, game_id, user):
        '''Fonction pour creer et tester la connection a une partie'''
        communicator.scope['user'] = user
        communicator.scope['url_route']={'kwargs':{'game_id':game_id}}
        connected, _ = await communicator.connect()
        self.assertTrue(connected)

    async def disconnect(self, communicator):
        '''Fonction pour se deconnecter et tester la deconnection d'une partie'''
        await communicator.send_json_to({'type': 'disconnect'})
        await communicator.disconnect()

    async def test_placement(self):
        '''Fonction permettant de tester le placement d\'une pierre sur le terrain'''
        game_id = self.game.id_game
        communicator = WebsocketCommunicator(GameJoinAndLeave.as_asgi(), f'/ws/game/{game_id}/')

        # Connection de l'utilisateur
        await self.connect(communicator, game_id, self.user1)
        # Placement d'une pierre en 1,1
        event = {'type': 'play', 'data': '1;1'}
        await communicator.send_json_to(event)
        # On recoit la reponse
        response = await communicator.receive_json_from()
        # On verifie le type de reponse puis les donnees renvoyees
        self.assertEqual(response['type'], 'play')
        self.assertEqual(response['data'], '{"w": "1;1", "b": "", "r": ""}')
        response = await communicator.receive_json_from()
        self.assertEqual(response['type'], 'can-play')
        # Disconnect user
        await self.disconnect(communicator)

    async def test_alternate_placement(self):
        '''Fonction test du placement alterne entre blanc et noir'''
        game_id = self.game.id_game
        communicator = WebsocketCommunicator(GameJoinAndLeave.as_asgi(), f'/ws/game/{game_id}/')
        # Connection de l'utilisateur
        await self.connect(communicator, game_id, self.user1)
        # Placement d'une pierre en 1,1 en tant que noir
        event = {'type': 'play', 'data': '1;1'}
        await communicator.send_json_to(event)
        # On recoit les reponses et on verifie les types de reponses
        response = await communicator.receive_json_from()
        self.assertEqual(response['type'], 'play')
        response = await communicator.receive_json_from()
        self.assertEqual(response['type'], 'can-play')
        # On place une autre pierre en 1,2 en tant que noir
        event = {'type': 'play', 'data': '1;2'}
        await communicator.send_json_to(event)
        # Cela doit revoyer une erreur puisque ce n'est pas le tour du joueur noir
        response = await communicator.receive_json_from()
        self.assertEqual(response['type'], 'error') 
        await self.disconnect(communicator)

        # Connection de l'utilisateur 2
        #await self.connect(communicator, game_id, self.user2)


    def test_illegal(self):
        '''Fonction permettant de tester les coups illégaux'''
        pass
