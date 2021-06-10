from collections import defaultdict


class Board:

    def __init__(self, height=10, width=20, **kwargs):

        self.HEIGHT = height
        self.WIDTH = width

        self.alive_cells = set()

        if 'string_map' in kwargs:
            self.fill_from_map(kwargs['string_map'])

    def fill_from_map(self, string_map):

        self.alive_cells = set()

        for x, string in enumerate(string_map):
            if x >= self.HEIGHT:
                break

            for y, character in enumerate(string):
                if y >= self.WIDTH:
                    break
                if character == '#':
                    self.alive_cells.add((x, y))

    def get_neighbours(self, x, y):

        def loop(neighbour_x, neighbour_y):

            return neighbour_x % self.HEIGHT, neighbour_y % self.WIDTH

        return (
            loop(*cell) for cell in (
                (x-1, y-1),
                (x-1, y),
                (x-1, y+1),
                (x, y-1),
                (x, y+1),
                (x+1, y-1),
                (x+1, y),
                (x+1, y+1),
            ) 
        )

    def update(self):

        neighbours_count = defaultdict(int)
        for cell in self.alive_cells:
            for neigbour in self.get_neighbours(*cell):
                neighbours_count[neigbour] += 1

        new_board = set()
        for cell, count in neighbours_count.items():
            if (count == 2 and cell in self.alive_cells) or count == 3:
                new_board.add(cell)

        self.alive_cells = new_board


if __name__ == '__main__':

    from time import sleep
    from os import system

    class ConsoleBoard(Board):

        def print(self):

            print('-'*(self.WIDTH+2)+'\n|'+'|\n|'.join(
                ''.join(
                    '#' if (x, y) in self.alive_cells else ' '
                    for y in range(self.WIDTH)
                ) for x in range(self.HEIGHT)
            )+'|\n'+'-'*(self.WIDTH+2))

    SAMPLE_STRING_MAP = [
        '                    ',
        '    ##              ',
        '    ##              ',
        '                    ',
        '  #      #######    ',
        '   #                ',
        ' ###                ',
        '                    ',
        '                    ',
        '                    ',
    ]
    TURNS_TO_SIMULATE = 200
    SLEEP_DELAY = 0.1

    board = ConsoleBoard(string_map=SAMPLE_STRING_MAP)
    board.print()

    for _ in range(TURNS_TO_SIMULATE):
        board.update()
        system('cls')
        board.print()
        sleep(SLEEP_DELAY)
