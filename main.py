from controller import Game

def main():
    """Основная функция для запуска шахматной игры."""
    game = Game()
    board = game.board

    # Выводим начальное состояние доски
    board.print()

    # Основной цикл для выбора режима игры
    while True:
        cmd = input('Что вы хотите?\n1 - Сыграть\n2 - Загрузить файл\n> ')
        if '1' in cmd:
            game.default_game()
            break
        elif '2' in cmd:
            game.load_file()
            break
        else:
            print('Некорректный ввод. Пожалуйста, выберите 1 или 2.')

if __name__ == '__main__':
    main()

"""
Выполнены пункты:

Подсказка хода: 1 балл
Вернуться назад: 1 балл

Итого: 2
"""