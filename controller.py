# from board import Board
from new_board import Board

class Game:
    """класс управляющий игровым процессом и взаимодействием с пользователем

    Args:
        board (Board): Объект шахматной доски
    """

    def __init__(self):
        """Инициализирует игру создавая новую шахматную доску"""
        self.board = Board()

    def move(self):
        """выполняет ход и обновляет состояние доски
        """
        self.board.move()
        self.board.print()
        print(f'\nОжидание хода от {self.move_now}')

    def default_game(self):
        """Запускает стандартную игру с пошаговым вводом ходов от пользователя"""
        is_win = False
        while is_win != True:
            print(f'номер хода: {len(self.board.history)+1}')
            print(f'текущий ход у {self.board.move_now}')
            a = input('введите координаты фигуры или `назад` чтобы вернуть ход: ')
            if 'назад' in a: 
                i = int(input(f'на сколько ходов хотите вернуться? Всего было {len(self.board.history)}\n> '))
                obj = self.board.history[-i]
                self.board.grid = obj['grid']
                self.board.move_now = obj['move']
                self.board.print()
                continue
            self.board.print_predict(a)
            b = input('введите координаты клетки, куда хотите передвинуть: ')
            is_win = self.board.move(a, b)
            self.board.print()
    
    def load_file(self):
    """Загружает историю ходов из файла 'history.txt' и воспроизводит их."""
    try:
        with open('history.txt', 'r') as f:
            moves = f.readlines()  # Читаем все строки из файла
            for move in moves:
                start, end = move.strip().split()  # Разделяем начальную и конечную клетки
                print(f'Выполняю ход: {start} → {end}')
                self.board.move(start, end)  # Выполняем ход
                self.board.print()  # Показываем доску после каждого хода
            print('История ходов успешно загружена.')
    except FileNotFoundError:
        print('Файл history.txt не найден.')
    except Exception as e:
        print(f'Ошибка при загрузке файла: {e}')
