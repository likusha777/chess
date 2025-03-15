class Figure:
    """базовый класс для всех фигур

    Args:
        team (str): команда фигуры (ч/б)
        code (str): уникальный код фигуры (K для короля и тд)
        icon (str): символ, отображаемый на доске для этой фигуры
        row (int): текущая строка на доске от 0 до 7
        column (int): текущий столбец на доске
    """

    def __init__(self, team=None, pos: list[int] = None):
        """Инициализация фигуры

        Args:
            team (str, optional): команда фигуры
            pos (list[int], optional): позиция фигуры на доске [строка, столбец]
        """
        self.team = team
        self.code = ''.join([k for k, v in code.items() if v == type(self)])
        self.icon = team and icons[self.code][team] or '.'

        if pos:
            self.row = pos[0]
            self.column = pos[1]

        """
        Если надо выключить рисование иконок - раскоментировать строку ниже
        """
        self.icon = self.code.lower() if team == 'white' else self.code.upper()

    def set_icon(self, icon):
        """устанавливает иконку фигуры

        Args:
            icon (str): новый символ для отображения фигуры
        """
        self.icon = icon

    def move(self, row: int, col: int, grid: list[list], check=None):
        """перемещает фигуру на новую позицию

        метод будет переопределён в дочерних классах
        """
        return False

    def eat(self):
        """Выполняет действие съедания другой фигуры

        метод должен быть переопределён в дочерних классах.
        """
        pass

    def cant_move(self):
        """Выводит сообщение о невозможности хода"""
        print('Туда ходить нельзя')



class King(Figure):
    """класс представляющий короля в шахматах"""

    def __init__(self, team, pos):
        """Инициализация короля

        Args:
            team (str): команда короля ('white' или 'black')
            pos (list[int]): позиция короля на доске [строка, столбец]
        """
        super().__init__(team=team, pos=pos)

    def move(self, row: int, col: int, grid: list[list], check = None):
        """перемещает короля на новую позицию

               Args:
                   row (int): новая строка на доске
                   col (int): новый столбец на доске
                   grid (list[list]): игровая доска
                   check (bool, optional): флаг для проверки возможности хода

               Returns:
                   bool: True, если ход возможен, иначе False
               """
        if type(grid[row][col]) != Figure and grid[row][col].team == self.team: return
        if abs(row-self.row) <= 1 and abs(col - self.column) <=1: return True 
    
    def eat(self):
        """Выполняет действие съедания другой фигуры"""
        return self.move()


class Queen(Figure):
    """класс представляющий ферзя в шахматах"""

    def __init__(self, team, pos):
        """Инициализирует ферзя.

            Args:
                team (str): Команда ферзя ('white' или 'black').
                pos (list[int]): Позиция ферзя на доске [строка, столбец].
                """

        super().__init__(team=team, pos=pos)

    def move(self, row: int, col: int, grid: list[list], check=None):
        """Перемещает ферзя на новую позицию

        Args:
            row (int): Новая строка на доске
            col (int): Новый столбец на доске
            grid (list[list]): Игровая доска
            check (bool, optional): Флаг для проверки возможности хода

        Returns:
            bool: True, если ход возможен, иначе False
        """

        if self.row == row or self.column == col or abs(self.row - row) == abs(self.column - col):
           row_step = (row - self.row) // max(1, abs(row - self.row)) if row != self.row else 0
           col_step = (col - self.column) // max(1, abs(col - self.column)) if col != self.column else 0
           r = self.row + row_step
           c = self.column + col_step
      
           while (r != row) or (c != col):
               if type(grid[r][c]) != Figure and grid[r][c].team == self.team: return

               r += row_step
               c += col_step
           
           if check==None: self.row, self.column = row, col
           return True

    def eat(self, row: int, col: int, grid: list[list]):
        """Выполняет действие "съедания" другой фигуры

        Args:
            row (int): Строка фигуры, которую нужно съесть
            col (int): Столбец фигуры, которую нужно съесть
            grid (list[list]): Игровая доска

        Returns:
            bool: True, если съедение возможно, иначе False
        """
        return self.move(row, col, grid)


class Rook(Figure):
    """Класс представляющий ладью в шахматах"""

    def __init__(self, team, pos):
        """инициализация ладьи

        Args:
            team (str): Команда ладьи ('white' или 'black')
            pos (list[int]): Позиция ладьи на доске [строка, столбец]
        """

        super().__init__(team=team, pos=pos)

    def move(self, row: int, col: int, grid: list[list], check=None):
        """Перемещает ладью на новую позицию

        Args:
            row (int): Новая строка на доске
            col (int): Новый столбец на доске
            grid (list[list]): Игровая доска
            check (bool, optional): Флаг для проверки возможности хода. По умолчанию None.

        Возвращает:
            bool: True, если ход возможен, иначе False.
        """
        if (row-self.row) * (col-self.column) == 0 and type(grid[row][col]) == Figure:
            if check == None: self.row, self.column = row, col
            return True
        

    def eat(self, row: int, col: int, grid: list[list]):
        """Выполняет действие "съедания" другой фигуры

               Args:
                   row (int): Строка фигуры, которую нужно съесть
                   col (int): Столбец фигуры, которую нужно съесть
                   grid (list[list]): Игровая доска

               Returns:
                   bool: True, если съедение возможно, иначе False
               """
        return self.move(row, col, grid)


class Bishop(Figure): # слон
    """Класс представляющий слона в шахматах"""

    def __init__(self, team, pos):
        """Инициализирует слона

        Args:
            team (str): Команда слона ('white' или 'black')
            pos (list[int]): Позиция слона на доске [строка, столбец]
        """

        super().__init__(team=team, pos=pos)

    def move(self, row: int, col: int, grid: list[list], check=None):
        """Перемещает слона на новую позицию.

                Args:
                    row (int): Новая строка на доске.
                    col (int): Новый столбец на доске.
                    grid (list[list]): Игровая доска.
                    check (bool, optional): Флаг для проверки возможности хода. По умолчанию None.

                Returns:
                    bool: True, если ход возможен, иначе False.
                """
        if abs(self.row - row) != abs(self.column - col):
            return False
        
        row_step = 1 if row > self.row else -1
        col_step = 1 if col > self.column else -1
        
        current_row = self.row + row_step
        current_col = self.column + col_step
        
        while (current_row != row) and (current_col != col):
            if grid[current_row][current_col] != Figure and grid[current_row][current_col].team == self.team:
                return False
            current_row += row_step
            current_col += col_step

        if check == None: self.row, self.column = row, col
        return True

    def eat(self, row: int, col: int, grid: list[list]):
        """Выполняет действие "съедания" другой фигуры

        Args:
            row (int): Строка фигуры, которую нужно съесть
            col (int): Столбец фигуры, которую нужно съесть
            grid (list[list]): Игровая доска

        Returns:
            bool: True, если съедение возможно, иначе False
        """
        return self.move(row, col, grid)


class Knight(Figure): # конь
    """Класс представляющий коня в шахматах"""

    def __init__(self, team, pos):
        """Инициализирует коня

        Args:
            team (str): Команда коня ('whiteили black)
            pos (list[int]): Позиция коня на доске [строка, столбец]
        """
        super().__init__(team=team, pos=pos)

    def move(self, row: int, col: int, grid: list[list], check=None):
        """Перемещает коня на новую позицию

               Args:
                   row (int): Новая строка на доске
                   col (int): Новый столбец на доске
                   grid (list[list]): Игровая доска
                   check (bool, optional): Флаг для проверки возможности хода. По умолчанию None

               Returns:
                   bool: True, если ход возможен, иначе False.
               """
        if (abs(self.row - row) == 2 and abs(self.column - col) == 1) or (abs(self.row - row) == 1 and abs(self.column - col) == 2):
                if type(grid[row][col]) != Figure and grid[row][col].team == self.team: return False
                if check == None: self.row, self.column = row, col
                return True

    def eat(self, row: int, col: int, grid: list[list]):
        """Выполняет действие "съедания" другой фигуры

              Args:
                  row (int): Строка фигуры, которую нужно съесть
                  col (int): Столбец фигуры, которую нужно съесть
                  grid (list[list]): Игровая доск

              Returns:
                  bool: True, если съедение возможно, иначе False
              """
        return self.move(row, col, grid)


class Pawn(Figure):
    """Класс, представляющий пешку в шахматах"""
    def __init__(self, team, pos):
        """Инициализирует пешку

        Args:
            team (str): Команда пешки ('white' или 'black')
            pos (list[int]): Позиция пешки на доске [строка, столбец]
        """
        super().__init__(team=team, pos=pos)

    def is_my_half(self):
        """Проверяет, находится ли пешка на своей половине доски

               Returns:
                   bool: True, если пешка на своей половине, иначе False
               """
        return self.row < 4

    def move(self, row: int, col: int, grid: list[list], check=None):
        """Перемещает пешку на новую позицию

        Args:
            row (int): Новая строка на доске
            col (int): Новый столбец на доске
            grid (list[list]): Игровая доска
            check (bool, optional): Флаг для проверки возможности хода. По умолчанию None

        Returns:
            bool: True, если ход возможен, иначе False
        """
        if type(type(grid[row][col])) == Figure and check==None: 
            return self.eat(row, col, grid)
        if self.row == row and self.column == col: return 
        if row < self.row: return 

        if col == self.column  and (row - self.row) <= (self.is_my_half() and 2 or 1): 
            if check == None: self.row, self.column = row, col
            return True

    def eat(self, row: int, col: int, grid: list[list]):
        """Выполняет действие съедания другой фигуры

        Args:
            row (int): Строка фигуры, которую нужно съесть
            col (int): Столбец фигуры, которую нужно съесть
            grid (list[list]): Игровая доска

        Returns:
            bool: True, если съедение возможно, иначе False.
        """
        if abs(self.column - col) == 1 and row == self.row + 1:
            if isinstance(grid[row][col], Figure) and grid[row][col].team != self.team:
                grid[row][col] = Figure()  # Заменяем съеденную фигуру на пустую клетку
                return True
        return False

code = {
    'K': King,
    'Q': Queen,
    'N': Knight,
    'R': Rook,
    'B': Bishop,
    'P': Pawn,
    '.': Figure
}

icons = {
    'K': {'white': '♚', 'black': '♔'},
    'Q': {'white': '♛', 'black': '♕'},
    'N': {'white': '♞', 'black': '♘'},
    'R': {'white': '♜', 'black': '♖'},
    'B': {'white': '♝', 'black': '♗'},
    'P': {'white': '♟', 'black': '♙'},
}