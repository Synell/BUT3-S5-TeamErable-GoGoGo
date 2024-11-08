from ..logic.Board import Board
import json, os

class GameStorage:
    def __new__(cls) -> None:
        '''Fait en sorte que la classe ne puisse pas être instanciée'''
        return None


    @staticmethod
    def load_game(path: str) -> Board:
        '''Charge une partie depuis la base de données

        Args:
            path (str): Le chemin vers la partie

        Returns:
            Board: Le plateau de jeu
        '''
        with open(path, 'r', encoding = 'utf-8') as f:
            board = Board(json.load(f))

        return board


    @staticmethod
    def save_game(path: str, board: Board) -> None:
        '''Sauvegarde une partie dans la base de données

        Args:
            path (str): Le chemin vers la partie
            board (Board): Le plateau de jeu
        '''
        with open(path, 'w', encoding = 'utf-8') as f:
            json.dump(board.export(), f)


    @staticmethod
    def delete_game(path: str) -> None:
        '''Supprime une partie de la base de données

        Args:
            path (str): Le chemin vers la partie
        '''
        if os.path.exists(path):
            os.remove(path)
