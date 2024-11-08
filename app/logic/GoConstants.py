from .Vector2 import Vector2

class GoConstants:
    '''Constantes du jeu de Go.'''
    Neighbors = [
        Vector2(1, 0),
        Vector2(-1, 0),
        Vector2(0, 1),
        Vector2(0, -1),
    ]

    Corners = [
        Vector2(1, 1),
        Vector2(-1, 1),
        Vector2(1, -1),
        Vector2(-1, -1),
    ]

    AllowPlayInDeadZones = False

    # Nombre de pierres et positions à placer pour chaque handicap
    HandicapStones = {
        9: [
            Vector2(6, 2), # Haut droite
            Vector2(2, 6), # Bas gauche
            Vector2(6, 6), # Bas droite
            Vector2(2, 2), # Haut gauche
        ],
        13: [
            Vector2(9, 3), # Haut droite
            Vector2(3, 9), # Bas gauche
            Vector2(6, 6), # Bas droite
            Vector2(3, 3), # Haut gauche
            Vector2(9, 9), # Milieu
        ],
        19: [
            Vector2(15, 3), # Haut droite
            Vector2(3, 15), # Bas gauche
            Vector2(15, 15), # Bas droite
            Vector2(3, 3), # Haut gauche
            Vector2(9, 9), # Milieu
            Vector2(3, 9), # Milieu gauche
            Vector2(15, 9), # Milieu droite
            Vector2(9, 3), # Milieu haut
            Vector2(9, 15), # Milieu bas
        ],
    }
