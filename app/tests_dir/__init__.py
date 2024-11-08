# connection tests
from .connection.test_login import *
from .connection.test_register import *
# Profil tests
from .profil.test_profil import *
from .profil.test_friends import *
from .profil.test_security import *
# Game tests
from .games.test_init_game import *
from .games.test_place_stone import *
#from .games.test_surrounded_stone import *
# Tournament tests
from .tournament.test_init_tournament import *

from .ranking.test_rank_calculator import *
from .ranking.test_rank_view import *