from .GoRank import GoRank

class RankCalculator:
    '''Classe permettant de calculer le rank d'un joueur'''

    @staticmethod
    def calculate_rank(nb_games:int, win_rate:float, elo: int, nb_tournament_wins: int)->str:
        '''Calcule le rang en fonction du nombre de parties et du taux de victoires

            Args:
                nb_games (int): le nombre de parties du joueur
                win_rate (int): le taux de victoire du joueur
                elo (int): l'elo du joueur
                nb_tournament_wins (int): le nombre de tournois gagnés

            Returns:
                (str): le rang                
        '''
        WINRATE_TOLERANCE = 0.7
        STEP_INCREMENT = 5
        TOURNAMENT_WIN_WEIGHT = 25
        ELO_WEIGHT = 0.5

        experience = 0
        step = STEP_INCREMENT

        # Calcul de l'experience
        nb_games_count = nb_games
        while nb_games_count > 0 and win_rate > 0:
            win_rate -= (step*100/nb_games)*WINRATE_TOLERANCE
            nb_games_count -= step
            experience += 100
            if (experience/1000).is_integer():
                step += STEP_INCREMENT
        experience += nb_games_count
        # Ajout du bonus tournois
        experience += nb_tournament_wins * TOURNAMENT_WIN_WEIGHT
        # Ajout du bonus/malus de elo       
        experience += ELO_WEIGHT * (elo - 1000)
        
        rank = round(experience/100, 0)
        if rank > 38 : rank = 38
        return str(GoRank(rank+1))

    @staticmethod
    def calculate_elo(winner_elo: int, loser_elo: int, k_factor=32)->tuple[int, int]:
        """
        Calcule les nouveaux elos de chaque joueurs

        Args:
            winner_elo (int): Le elo du gagnant
            loser_elo (int): Le elo du perdant
            k_factor (int): Le facteur k permettant de calculer le elo (par defaut 32)

        Returns:
            int, int: Les nouveaux elos
        """
        expected_win = 1 / (1 + 10**((loser_elo - winner_elo) / 400))
        expected_lose = 1 / (1 + 10**((winner_elo - loser_elo) / 400))

        updated_winner_elo = winner_elo + k_factor * (1 - expected_win)
        updated_loser_elo = loser_elo + k_factor * (0 - expected_lose)

        return int(updated_winner_elo), int(updated_loser_elo)