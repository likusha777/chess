# from board import Board
from new_board import Board

class Game:
    def __init__(self):
        self.board = Board()

    def move(self, start: str, end: str):
        is_win = self.board.move(start, end)
        self.board.print()
        if is_win:
            print(f'Игра окончена! Победили {self.board.move_now}.')
        else:
            print(f'\nОжидание хода от {self.board.move_now}')

    def default_game(self):
        is_win = False
        while is_win != True:
            print(f'Номер хода: {len(self.board.history)+1}')
            print(f'Текущий ход у {self.board.move_now}')
            a = input('Введите координаты фигуры или `назад` чтобы вернуть ход: ')
            if 'назад' in a: 
                i = int(input(f'На сколько ходов хотите вернуться? Всего было {len(self.board.history)}\n> '))
                obj = self.board.history[-i]
                self.board.grid = obj['grid']
                self.board.move_now = obj['move']
                self.board.print()
                continue
            self.board.print_predict(a)
            b = input('Введите координаты клетки, куда хотите передвинуть: ')
            is_win = self.board.move(a, b)
            self.board.print()

    def load_file(self):
        try:
            with open('history.txt', 'r') as f:
                moves = f.readlines()
                for move in moves:
                    start, end = move.strip().split()
                    self.move(start, end)
                print('История ходов успешно загружена.')
        except FileNotFoundError:
            print('Файл history.txt не найден.')
        except Exception as e:
            print(f'Ошибка при загрузке файла: {e}')

