from figures import Figure, King, Queen, Rook, Bishop, Knight, Pawn
from copy import deepcopy
# from controller import Controller


"""
Король - K
Королева - Q
Конь - N
Ладья - R
Слон - B
Пешка - без буквы

"""

def get_icon(figure: Figure):
    t = type(figure)
    return t(figure.team, t)


class Board:
    def __init__(self):
        self.__generate() # вызывает метод для генерации начальной расстановки фигур
        # self.controller = Controller(self.grid)
        self.move_now = 'white' #Определяет чей сейчас ход ('white' или 'black')
        self.history = []

    def __generate(self):
        """
        Генерирация дэфолтного поля
        """
        self.grid = [[Figure() for _ in range(8)] for _ in range(8)]

        row = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]
        self.grid[0] = [row[i]('black', [0, i]) for i in range(len(row))]
        self.grid[1] = [Pawn('black', [1, i]) for i in range(8)]
        self.grid[6] = [Pawn('white', [1, 7-i]) for i in range(8)]
        self.grid[7] = [row[i]('white', [0, 7-i]) for i in range(len(row))]
        self.print()
        


    def unpack_full_notation(self, notation: str) -> dict:
        """
        Позволяет из нотации ( пример: Nf6 ) получить норм данные\n
        Return dict
        """
        kill_figure = notation.find('x') != -1 #Определяет, был ли ход со взятием фигуры
        notation = notation.replace('x', '')

        long_castling = notation.find('O-O-O') != -1 #Определяют, была ли рокировка
        notation = notation.replace('O-O-O', '')

        short_castling = notation.find('O-O') != -1
        notation = notation.replace('O-O', '')

        notation = notation.replace('-', '')

        obj = {} #Содержит информацию о начальной и конечной позиции фигуры


        if len(notation) > 0:
            i = notation[0].isupper() and 1 or 0

            column_start = notation[i]
            index_start = notation[i+1]
            column_end = notation[i+2]
            index_end = notation[i+3]
        
            figure = self.grid[column_start][index_start]
            obj = {'column_start': column_start, 'index_start': index_start, 'column_end': column_end, 'index_end': index_end, 'figure': figure}

        return {
            'obj': obj,
            'kill_figure': kill_figure,
            'long_castling': long_castling,
            'short_castling': short_castling
        }     

    def back(self):
        """
        Универсальная функция, позволяет вернуться на шаг назад
        """

        self.__switch_move()

    def __switch_move(self): 
        self.move_now = self.move_now == 'white' and 'black' or 'white'

    def next(self, notation: str):
        """
        Перейти на следуюищй шаг. Разумеется работает только при чтении
        """

    def transtale(self, address: str):
        """
        Переводим заголовки в индексы
        """
        return '87654321'.index(address[1]), 'abcdefgh'.index(address[0])

    def upend_grid(self, fig, grid=None, need=None) -> list[list]:
        """Переворачивает доску для удобства отображения (например для белых фигур)"""
        grid = grid or self.grid
        return (fig.team == 'white' or need) and [row[::-1] for row in grid[::-1]] or grid
    
    def upend_pos(self, a:int, b: int) -> tuple[int]:
        """Переворачивает координаты для отображения"""
        return (7-a, 7-b)

    def move(self, start: str, end: str):
        try:
            old_row, old_col = self.transtale(start)
            fig = self.grid[old_row][old_col]

            # Проверяем, что фигура не является базовой (пустой клеткой)
            if isinstance(fig, Figure) and fig.code == '.':
                print('На этой клетке нет фигуры!')
                return

            row, col = self.transtale(end)
            grid = self.upend_grid(fig)

            if fig.team != self.move_now:
                print('Сейчас не ваш ход!')
                return

            if fig.team == 'white':
                row, col = self.upend_pos(row, col)

            if row == fig.row and col == fig.column:
                print('Нельзя оставаться на месте')
                return

            if fig.team == grid[row][col].team:
                print('Нельзя ходить на место своей фигуры')
                return

            if fig.move(row, col, self.upend_grid(fig)):
                if fig.team == 'white':
                    row, col = self.upend_pos(row, col)
                if type(fig) == King:
                    print('Вы победили!')
                    return True

                self.history.append({'move': self.move_now, 'grid': deepcopy(self.grid)})
                self.grid[row][col] = self.grid[old_row][old_col]
                self.grid[old_row][old_col] = Figure()

                self.__switch_move()
            else:
                fig.cant_move()
        except (ValueError, IndexError):
            print('Некорректные координаты!')

    def print_predict(self, a: str):
        """Показывает возможные ходы для выбранной фигуры"""
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
        """Выводит текущее состояние доски"""
        grid = grid or self.grid
        print("    a b c d e f g h")
        print("    ---------------")
        row_num = 8
        for i in grid:
            print(f"{row_num} | {' '.join(list(map(lambda fig: fig.icon, i)))} |")
            row_num -= 1 
        print("  ------------------")