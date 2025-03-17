from copy import deepcopy
from figures import Figure, King, Queen, Rook, Bishop, Knight, Pawn


class Board:
    """Класс представляющий шахматную доску и управляющий игровым процессом

    Args:
        grid (list[list[Figure]]): Двумерный список, представляющий шахматную доску
        move_now (str): Команда, которая должна сделать следующий ход ('white' или 'blak')
        history (list): Список для хранения истории ходов
    """

    def __init__(self):
        """Инициализирует шахматную доску и настраивает начальную расстановку фигур"""
        self.__generate()
        self.move_now = 'white'
        self.history = []

    def __generate(self):
        """Генерирует начальную расстановку фигур на шахматной доске"""
        self.grid = [[Figure() for _ in range(8)] for _ in range(8)]

        row = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]
        self.grid[0] = [row[i]('black', [0, i]) for i in range(len(row))]
        self.grid[1] = [Pawn('black', [1, i]) for i in range(8)]
        self.grid[6] = [Pawn('white', [1, 7 - i]) for i in range(8)]
        self.grid[7] = [row[i]('white', [0, 7 - i]) for i in range(len(row))]
        self.print()

    def unpack_full_notation(self, notation: str) -> dict:
        """Преобразует шахматную нотацию (например, 'Nf6') в словарь с данными о ходе.

        Args:
            notation (str): Шахматная нотация (например, 'Nf6').

        Returns:
            dict: Словарь с информацией о ходе, включая начальную и конечную позиции, фигуру и тип хода.
        """
        kill_figure = notation.find('x') != -1
        notation = notation.replace('x', '')

        long_castling = notation.find('O-O-O') != -1
        notation = notation.replace('O-O-O', '')

        short_castling = notation.find('O-O') != -1
        notation = notation.replace('O-O', '')

        notation = notation.replace('-', '')

        obj = {}

        if len(notation) > 0:
            i = notation[0].isupper() and 1 or 0

            column_start = notation[i]
            index_start = notation[i + 1]
            column_end = notation[i + 2]
            index_end = notation[i + 3]

            figure = self.grid[column_start][index_start]
            obj = {'column_start': column_start, 'index_start': index_start, 'column_end': column_end,
                   'index_end': index_end, 'figure': figure}

        return {
            'obj': obj,
            'kill_figure': kill_figure,
            'long_castling': long_castling,
            'short_castling': short_castling
        }

    def back(self):
        """Отменяет последний ход и переключает очередь хода"""
        self.__switch_move()

    def __switch_move(self):
        """Переключает очередь хода между 'white' и 'black'"""
        self.move_now = self.move_now == 'white' and 'black' or 'white'

    def next(self, notation: str):
        """Переходит к следующему ходу (пока не реализовано)"""
        pass

    def transtale(self, address: str):
        """Преобразует шахматные координаты (например, 'e4') в индексы для доски

        Args:
            address (str): Шахматные координаты (например, 'e4')

        Returns:
            tuple[int]: Кортеж с индексами строки и столбца на доске
        """
        return '87654321'.index(address[1]), 'abcdefgh'.index(address[0])

    def upend_grid(self, fig, grid=None, need=None) -> list[list]:
        """Переворачивает доску для удобства отображения.

        Args:
            fig (Figure): Фигура, для которой переворачивается доска
            grid (list[list], optional): Исходная доска. По умолчанию None
            need (bool, optional): Флаг для принудительного переворачивания. По умолчанию None

        Returns:
            list[list]: Перевёрнутая доска
        """
        grid = grid or self.grid
        return (fig.team == 'white' or need) and [row[::-1] for row in grid[::-1]] or grid

    def upend_pos(self, a: int, b: int) -> tuple[int]:
        """Переворачивает координаты для отображения.

        Args:
            a (int): Индекс строки
            b (int): Индекс столбца

        Returns:
            tuple[int]: Перевёрнутые координаты
        """
        return (7 - a, 7 - b)

    def move(self, start: str, end: str):
        """Выполняет ход фигуры с одной клетки на другую

        Args:
            start (str): Начальная позиция фигуры (например 'e2')
            end (str): Конечная позиция фигуры (например 'e4')

        Returns:
            bool: True, если ход выполнен успешно, иначе False
        """
        old_row, old_col = self.transtale(start)
        fig = self.grid[old_row][old_col]
        row, col = self.transtale(end)
        grid = self.upend_grid(fig)
        if fig.team != self.move_now: return print('Сейчас не ваш ход!')

        if fig.team == 'white':
            row, col = (self.upend_pos(row, col))

        if row == fig.row and col == fig.column: return print('Нельзя оставаться на месте')
        if fig.team == grid[row][col].team: return print('Нельзя ходить на место своей фигуры')

        if fig.move(row, col, self.upend_grid(fig)):
            if fig.team == 'white':
                row, col = (self.upend_pos(row, col))
            if type(fig) == King:
                print('вы победили')
                return True

            self.history.append({'move': self.move_now, 'grid': deepcopy(self.grid)})
            self.grid[row][col] = self.grid[old_row][old_col]
            self.grid[old_row][old_col] = Figure()

            self.__switch_move()
        else:
            fig.cant_move()

    def print_predict(self, a: str):
        """Показывает возможные ходы для выбранной фигуры

        Args:
            a (str): Координаты фигуры (например 'e2')
        """
        print('подсказка!')
        row, col = self.transtale(a)
        fig = self.grid[row][col]
        print(fig.team)
        grid = deepcopy(self.upend_grid(fig, grid=self.grid))
        for i in range(8):
            for j in range(8):
                if fig.move(i, j, grid, True):
                    print('есть')
                    grid[i][j].icon = '*'

        if fig.team == 'white':
            grid = self.upend_grid(fig, grid=grid, need=True)
        self.print(grid)

    def print(self, grid: list[list] = None):
        """Выводит текущее состояние шахматной доски.

        Args:
            grid (list[list], optional): Доска для отображения. По умолчанию используется текущая доска.
        """
        grid = grid or self.grid
        print("    a b c d e f g h")
        print("    ---------------")
        row_num = 8
        for i in grid:
            print(f"{row_num} | {' '.join(list(map(lambda fig: fig.icon, i)))} |")
            row_num -= 1
        print("  ------------------")
