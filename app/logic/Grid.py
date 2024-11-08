from .Tile import Tile
from .Vector2 import Vector2
from .Island import Island
from .GoConstants import GoConstants
import math

class Grid:
    '''Grille de jeu.'''
    def __init__(self, size: int) -> None:
        '''Initialise une grille de taille spécifiée.

        Args:
            size (int): Taille de la grille.
        '''
        self._size = Vector2(size, size)
        self._grid: list[list[Tile | None]] = [[None for _ in range(self._size.x)] for _ in range(self._size.y)]


    @property
    def size(self) -> Vector2:
        '''Renvoie la taille de la grille.'''
        return self._size

    @property
    def width(self) -> int:
        '''Renvoie la largeur de la grille.'''
        return self._size.x

    @property
    def height(self) -> int:
        '''Renvoie la hauteur de la grille.'''
        return self._size.y

    @property
    def raw(self) -> list[list[Tile | None]]:
        '''Renvoie la grille sous forme de liste de liste de couleurs.
        
        Returns:
            list[list[Tile | None]]: Grille sous forme de liste de liste de couleurs.
        '''
        l: list[list[Tile | None]] = []

        for y in range(self.size.y):
            l.append([])
            for x in range(self.size.x):
                t = self.get(Vector2(x, y))
                l[y].append(t.value.color if t else None)

        return l


    def __iter__(self) -> iter:
        '''Renvoie un itérateur sur la grille.'''
        return iter(self._grid)

    def __getitem__(self, index: int) -> list[Tile | None]:
        '''Renvoie la liste de tuiles de la ligne d'index spécifié.
        
        Args:
            index (int): Index de la ligne.

        Returns:
            list[Tile | None]: Liste de tuiles de la ligne.
        '''
        return self._grid[index]

    def __str__(self) -> str:
        '''Renvoie la grille sous forme de chaine de caractères.
        
        Returns:
            str: Grille sous forme de chaine de caractères.
        '''
        s = '╔' + '═' * (self.size.x * 3) + '╗\n'
        for y in range(self.size.y):
            s += '║'
            for x in range(self.size.x):
                s += (str(self._grid[y][x]) if self._grid[y][x] else '➕') + ' '
            s += '║\n'
        return s + '╚' + '═' * (self.size.x * 3) + '╝'
    
    def __repr__(self) -> str:
        '''Surcharge de l'opérateur str.'''
        return str(self)


    def get(self, coords: Vector2) -> Tile | None:
        '''Renvoie la tuile aux coordonnées spécifiées.

        Args:
            coords (Vector2): Coordonnées de la tuile.

        Raises:
            ValueError: Si les coordonnées sont en dehors du plateau.

        Returns:
            Tile | None: _description_
        '''
        if self.is_outside(coords): raise ValueError('Les coordonnées sont en dehors du plateau.')
        return self._grid[coords.y][coords.x]


    def set(self, coords: Vector2, value: Tile | None) -> None:
        '''Définit la tuile aux coordonnées spécifiées.

        Args:
            coords (Vector2): Coordonnées de la tuile.
            value (Tile): Valeur de la tuile.

        Raises:
            ValueError: Si les coordonnées sont en dehors du plateau.
        '''
        if self.is_outside(coords): raise ValueError('Les coordonnées sont en dehors du plateau.')
        self._grid[coords.y][coords.x] = value


    def is_outside(self, coords: Vector2) -> bool:
        '''Vérifie si les coordonnées sont en dehors du plateau.

        Args:
            coords (Vector2): Coordonnées.

        Returns:
            bool: True si les coordonnées sont en dehors du plateau, False sinon.
        '''
        return coords.x < 0 or coords.x >= self.size.x or coords.y < 0 or coords.y >= self.size.y


    def is_empty(self) -> bool:
        '''Vérifie si la grille est vide.

        Returns:
            bool: True si la grille est vide, False sinon.
        '''
        for y in range(self.size.y):
            for x in range(self.size.x):
                if self._grid[y][x] is not None:
                    return False

        return True


    @staticmethod
    def from_list(grid: list[list[Tile | None]]) -> 'Grid':
        '''Crée une grille à partir d'une liste de listes.

        Args:
            grid (list[list[Tile | None]]): Liste de listes.

        Returns:
            Grid: Grille.
        '''
        assert all(len(row) == len(grid[0]) for row in grid), 'All rows must have the same length'

        g = Grid(len(grid))
        g._grid = grid

        return g


    def get_neighbors(self, coords: Vector2) -> tuple[Vector2]:
        '''Renvoie les coordonnées des voisins.

        Args:
            coords (Vector2): Coordonnées de la tuile.

        Returns:
            tuple[Vector2]: Coordonnées des voisins.
        '''
        return tuple(coords + c for c in GoConstants.Neighbors if not self.is_outside(coords + c))


    def get_corner_points(self, coords: Vector2) -> tuple[Vector2]:
        '''Renvoie les coordonnées des coins.

        Args:
            coords (Vector2): Coordonnées de la tuile.

        Returns:
            tuple[Vector2]: Coordonnées des coins.
        '''
        return tuple(coords + c for c in GoConstants.Corners if not self.is_outside(coords + c))


    def get_group_and_neighbors(self, starting_point: Vector2) -> tuple[list[Vector2], list[Vector2]]:
        '''Renvoie le groupe et les voisins de la tuile aux coordonnées spécifiées.

        Args:
            starting_point (Vector2): Coordonnées de la tuile.

        Returns:
            tuple[list[Vector2], list[Vector2]]: Groupe et voisins de la tuile.
        '''
        return self.get_group_and_neighbors_from_points([starting_point])


    def get_group_and_neighbors_from_points(self, starting_points: list[Vector2]) -> tuple[list[Vector2], list[Vector2]]:
        '''Renvoie le groupe et les voisins des tuiles aux coordonnées spécifiées.

        Args:
            starting_points (list[Vector2]): Coordonnées des tuiles.

        Returns:
            tuple[list[Vector2], list[Vector2]]: Groupe et voisins des tuiles.
        '''
        tocheck = starting_points.copy()
        neighbors = []
        visited = [[False for _ in range(self.size.x)] for _ in range(self.size.y)]
        matching_value = self.get(starting_points[0])

        group = []

        while tocheck:
            p = tocheck.pop(0)
            if self.get(p) == matching_value:
                group.append(p)
                for neighbor in self.get_neighbors(p):
                    if visited[neighbor.y][neighbor.x]: continue

                    visited[neighbor.y][neighbor.x] = True
                    tocheck.append(neighbor)

            else:
                neighbors.append(p)

        return group, neighbors


    def get_islands(self) -> tuple[Island]:
        '''Renvoie les îles de tuiles.

        Returns:
            tuple[Island]: Îles de tuiles.
        '''
        grid = [[False for _ in range(self.size.x)] for _ in range(self.size.y)]
        islands = []

        for y in range(self.size.y):
            for x in range(self.size.x):
                if grid[y][x]: continue

                tile = self._grid[y][x]
                if tile is None: continue

                island = Island(tile, Vector2(x, y))
                grid[y][x] = True

                stack = [Vector2(x, y)]
                while stack:
                    coords = stack.pop()
                    for neighbor in self.get_neighbors(coords):
                        if grid[neighbor.y][neighbor.x]: continue

                        if self._grid[neighbor.y][neighbor.x] == tile:
                            island.add(neighbor)
                            grid[neighbor.y][neighbor.x] = True
                            stack.append(neighbor)

                islands.append(island)

        return tuple(islands)


    def get_island_from_coords(self, coords: Vector2) -> Island | None:
        '''Renvoie l'île de tuiles aux coordonnées spécifiées.

        Args:
            coords (Vector2): Coordonnées de la tuile.

        Returns:
            Island | None: Île de tuiles.
        '''
        if self.is_outside(coords): return None

        tile = self.get(coords)
        if tile is None: return None

        for island in self.get_islands():
            if island.tile == tile and coords in island.coords:
                return island

        return None


    def is_island_surronded(self, island: Island) -> bool:
        '''Vérifie si l'île de tuiles est entourée de tuiles adverses.

        Args:
            island (Island): Île de tuiles.

        Returns:
            bool: True si l'île est entourée, False sinon.
        '''
        enemy_tile = island.tile.next

        for coords in island.get_arround_tiles():
            if self.is_outside(coords): continue

            tile: Tile = self.get(coords)
            if tile != enemy_tile: return False

        return True


    def match(self, group: list[Vector2], value: Tile | None) -> list[Vector2]:
        '''Renvoie les tuiles du groupe égales à la valeur spécifiée.

        Args:
            group (list[Vector2]): Groupe de tuiles.
            value (Tile | None): Valeur à comparer.

        Returns:
            list[Vector2]: Tuiles du groupe égales à la valeur spécifiée.
        '''
        ret = []
        for coords in group:
            if self.get(coords) == value:
                ret.append(coords)

        return ret


    def not_match(self, group: list[Vector2], value: Tile | None) -> list[Vector2]:
        '''Renvoie les tuiles du groupe différentes de la valeur spécifiée.

        Args:
            group (list[Vector2]): Groupe de tuiles.
            value (Tile | None): Valeur à comparer.

        Returns:
            list[Vector2]: Tuiles du groupe différentes de la valeur spécifiée.
        '''
        ret = []
        for coords in group:
            if self.get(coords) != value:
                ret.append(coords)

        return ret


    def count_equal(self, group: list[Vector2], value: Tile | None) -> int:
        '''Compte le nombre de tuiles égales à la valeur spécifiée.

        Args:
            group (list[Vector2]): Groupe de tuiles.
            value (Tile | None): Valeur à comparer.

        Returns:
            int: Nombre de tuiles égales à la valeur spécifiée.
        '''
        ret = 0
        for coords in group:
            if self.get(coords) == value:
                ret += 1

        return ret


    def all_equal_to(self, group: list[Vector2], value: Tile | None) -> bool:
        '''Vérifie si toutes les tuiles du groupe sont égales à la valeur spécifiée.

        Args:
            group (list[Vector2]): Groupe de tuiles.
            value (Tile | None): Valeur à comparer.

        Returns:
            bool: True si toutes les tuiles du groupe sont égales à la valeur spécifiée, False sinon.
        '''
        for coords in group:
            if self.get(coords) != value:
                return False

        return True


    def get_min_liberties_of_surrounding_groups(self, coords: Vector2) -> int:
        '''Renvoie le nombre minimum de libertés des groupes entourant la tuile aux coordonnées spécifiées.

        Args:
            coords (Vector2): Coordonnées de la tuile.

        Returns:
            int: Nombre minimum de libertés des groupes entourant la tuile.
        '''
        neighbors = self.get_neighbors(coords)

        ret = math.inf

        for neighbor in neighbors:
            group, group_neighbors = self.get_group_and_neighbors(neighbor)

            liberties = self.count_equal(group_neighbors, None)
            ret = min(ret, liberties)

        return ret


    def get_false_eyes(self) -> tuple[Vector2]:
        '''Renvoie les faux yeux.

        Returns:
            tuple[Vector2]: Faux yeux.
        '''
        false_eyes: list[Vector2] = []

        for y in range(self.size.y):
            for x in range(self.size.x):
                coords = Vector2(x, y)
                if self.get(coords) is not None: continue

                neighbors = self.get_neighbors(coords)
                corners = self.get_corner_points(coords)

                if self.get_min_liberties_of_surrounding_groups(coords) > 1: continue

                if self.all_equal_to(neighbors, Tile.Black) and self.count_equal(corners, Tile.White) >= (len(corners) >> 1):
                    false_eyes.append(coords)

                elif self.all_equal_to(neighbors, Tile.White) and self.count_equal(corners, Tile.Black) >= (len(corners) >> 1):
                    false_eyes.append(coords)

        return false_eyes


    def get_raw_territory(self, tile: Tile) -> tuple[Island]:
        '''Renvoie le territoire brut de tuiles du joueur donné. -> Ne prend pas en compte les autres joueurs.

        Args:
            tile (Tile): Tuile du joueur. Renvoie les territoires du joueur si spécifié.

        Returns:
            tuple[Island]: Territoire de tuiles.
        '''
        territories = []

        board = [[(self.get(Vector2(x, y)) == tile) for x in range(self.size.x)] for y in range(self.size.y)]

        def next_tile():
            for y in range(self.size.y):
                for x in range(self.size.x):
                    if board[y][x]: continue

                    return Vector2(x, y)

            return None

        while pos := next_tile():
            group: list[Vector2] = []

            stack = [pos]
            while stack:
                coords = stack.pop()
                group.append(coords)
                board[coords.y][coords.x] = True

                for neighbor in self.get_neighbors(coords):
                    if self.is_outside(neighbor): continue

                    if not board[neighbor.y][neighbor.x]:
                        board[neighbor.y][neighbor.x] = True
                        stack.append(neighbor)

            territories.append(Island(tile, *(group)))

        return tuple(territories)


    def get_raw_territories(self) -> dict[Tile, tuple[Island]]:
        '''Renvoie les territoires bruts de tuiles.

        Returns:
            dict[Tile, tuple[Island]]: Territoires bruts de tuiles.
        '''
        territories = {}

        for tile in Tile:
            territories[tile] = self.get_raw_territory(tile)

        return territories


    def get_territories(self) -> dict[Tile, tuple[Island]]:
        '''Renvoie les territoires de tuiles.

        Returns:
            tuple[Island]: Territoires de tuiles.
        '''
        if self.is_empty(): return {tile: tuple() for tile in Tile}

        false_eyes = self.get_false_eyes()
        grid = self.copy()

        for false_eye in false_eyes:
            neighbor = grid.get_neighbors(false_eye)[0]
            grid.set(false_eye, grid.get(neighbor))

        raw_territories: dict[Tile, tuple[Island]] = grid.get_raw_territories()
        territories: dict[Tile, list[Island]] = {}

        for tile in Tile:
            territories[tile] = list(raw_territories[tile])

        for tile in Tile:
            for other_territory in territories[tile.next].copy():
                for this_territory in territories[tile].copy():
                    if other_territory.contains(this_territory) and other_territory in territories[tile.next]:
                        territories[tile.next].remove(other_territory)

        for tile in Tile:
            for other_territory in territories[tile.next].copy():
                for this_territory in territories[tile].copy():
                    if other_territory.overlaps(this_territory):
                        if other_territory in territories[tile.next]: territories[tile.next].remove(other_territory)
                        if this_territory in territories[tile]: territories[tile].remove(this_territory)

        return {tile: tuple(territories[tile]) for tile in Tile}


    def copy(self) -> 'Grid':
        '''Copie la grille.

        Returns:
            Grid: Copie de la grille.
        '''
        g = Grid(self.size.x)
        g._grid = [[self.get(Vector2(x, y)) for x in range(self.size.x)] for y in range(self.size.y)]

        return g
