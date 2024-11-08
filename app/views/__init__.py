from .reusable import *
from .index import index
# Imports connection
from .connection.login import login_, logout_
from .connection.register import register
from .connection.forgottenpassword import forgotten_password
# Imports profil
from .profil.public.profile import profile
from .profil.public.change_pfp import change_pfp
from .profil.public.change_user_info import change_user_info
from .profil.security.change_pwd import change_pwd
from .profil.security.delete_account import delete_account
from .profil.security.passwordresetconfirm import password_reset_confirm
from .profil.friend.add_friend import add_friend
from .profil.friend.delete_friend import delete_friend
from .profil.friend.friend_list import friend_list
from .profil.friend.search_notfriend_user import search_notfriend_user
# Imports footer
from .footer.termsofuse import termsofuse
from .footer.privacypolicy import privacypolicy
from .footer.legalmention import legalmention
from .footer.history import history
from .footer.team import team
from .footer.help import help
# Import tournament
from .tournament.tournament import tournament
from .tournament.tournament_manager import tournament_manager, tournament_join
from .tournament.create_tournament import create_tournament
from .tournament.edit_tournament import edit_tournament
from .tournament.tournament_game import create_tournament_game
from .tournament.tournament import search_tournament, search_current_tournament, tournament_code
from .tournament.tournament_struct import TournamentStruct
from .tournament.delete_tournament import delete_tournament
from .tournament.tournament_manager import tournament_player_list
# Import game
from .game.create_game import create_game
from .game.join_game import join_game, search_game, search_current_game
from .game.game import game, game_code, game_view_player
from .game.game_struct import GameStruct
from .game.game_configuration_struct import GameConfigurationStruct
from .game.game_configuration import create_game_config
# Import watch_game
from .watch_game.watch_game import watch_game
# Import classement
from .ranking.global_ranking import global_ranking
from .ranking.tournament_ranking import tournament_ranking
# Imports carrière
from .profil.career.career import search_games_historic, career, import_game, export_game, stats, public_career
from .profil.career.stats_struct import StatsStruct
