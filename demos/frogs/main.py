# Играта разполага с игрално поле от 2N+1 полета, като в началото
# в най-десните N полета имаме разположени жаби, гледащи наляво,
# а в най-левите N полета - жаби, гледащи надясно.
# Целта на играта е жабите да си разменят местата
# и да се стигне до противоположната конфигурация
#
# Правилата за игра са следните: всяка жаба може да се движи само в посоката, в която гледа.
# Всяка жаба може да скочи на свободно място пред себе си или да прескочи една жаба,
# за да отиде на празно място пред нея.

from enum import Enum

class Action(Enum):
    SHORT_RIGHT_JUMP = 0
    LONG_RIGHT_JUMP = 1
    LONG_LEFT_JUMP = 2
    SHORT_LEFT_JUMP = 3

class Cell(Enum):
    EMPTY_SPACE = 0
    LEFT_FACING_FROG = -1
    RIGHT_FACING_FROG = 1

SHORT_JUMP = 1
LONG_JUMP = 2

ACTIONS = [Action.LONG_RIGHT_JUMP, Action.SHORT_RIGHT_JUMP, Action.SHORT_LEFT_JUMP, Action.LONG_LEFT_JUMP]

class State:
    def __init__(self, board: list[Cell], empty_space_index: int):
        self.board = board
        self.empty_space_index = empty_space_index
        self.left_jumps = 0
        self.right_jumps = 0
        n = len(board) // 2
        self.target_jumps = n * (n+1)

    def is_goal_state(self) -> bool:
        return self.right_jumps == self.target_jumps and self.left_jumps == self.target_jumps

    @classmethod
    def construct_initial_state(cls, n: int) -> State:
        board = [Cell.RIGHT_FACING_FROG] * n + [Cell.EMPTY_SPACE] + [Cell.LEFT_FACING_FROG] * n
        return State(board, n)

    @classmethod
    def construct_goal_state(cls, n: int) -> State:
        board = [Cell.LEFT_FACING_FROG] * n + [Cell.EMPTY_SPACE] +[Cell.RIGHT_FACING_FROG] * n
        return State(board, n)

    def forward_jump(self, action: Action) -> bool:
        match action:
            case Action.LONG_RIGHT_JUMP:
                return self.forward_long_right_jump()
            case Action.SHORT_RIGHT_JUMP:
                return self.forward_short_right_jump()
            case Action.SHORT_LEFT_JUMP:
                return self.forward_short_left_jump()
            case Action.LONG_LEFT_JUMP:
                return self.forward_long_left_jump()

    def forward_long_right_jump(self) -> bool:
        if self.empty_space_index < LONG_JUMP:
            return False

        if self.board[self.empty_space_index - LONG_JUMP] != Cell.RIGHT_FACING_FROG:
            return False

        ind = self.empty_space_index
        self.board[ind], self.board[ind - LONG_JUMP] = self.board[ind - LONG_JUMP], self.board[ind]
        self.empty_space_index -= LONG_JUMP
        self.right_jumps+=LONG_JUMP

        return True


    def forward_short_right_jump(self) -> bool:
        if self.empty_space_index < SHORT_JUMP:
            return False

        if self.board[self.empty_space_index - SHORT_JUMP] != Cell.RIGHT_FACING_FROG:
            return False

        ind = self.empty_space_index
        self.board[ind], self.board[ind - SHORT_JUMP] = self.board[ind - SHORT_JUMP], self.board[ind]
        self.empty_space_index -= SHORT_JUMP
        self.right_jumps+=SHORT_JUMP

        return True

    def forward_long_left_jump(self) -> bool:
        if self.empty_space_index >= len(self.board) - LONG_JUMP:
            return False

        if self.board[self.empty_space_index + LONG_JUMP] != Cell.LEFT_FACING_FROG:
            return False

        ind = self.empty_space_index
        self.board[ind], self.board[ind + LONG_JUMP] = self.board[ind + LONG_JUMP], self.board[ind]
        self.empty_space_index += LONG_JUMP
        self.left_jumps+=LONG_JUMP

        return True

    def forward_short_left_jump(self) -> bool:
        if self.empty_space_index >= len(self.board) - SHORT_JUMP:
            return False

        if self.board[self.empty_space_index + SHORT_JUMP] != Cell.LEFT_FACING_FROG:
            return False

        ind = self.empty_space_index
        self.board[ind], self.board[ind + SHORT_JUMP] = self.board[ind + SHORT_JUMP], self.board[ind]
        self.empty_space_index += SHORT_JUMP
        self.left_jumps+=SHORT_JUMP

        return True

    def backward_jump(self, action: Action):
        match action:
            case Action.LONG_RIGHT_JUMP:
                self.backward_long_right_jump()
            case Action.SHORT_RIGHT_JUMP:
                self.backward_short_right_jump()
            case Action.SHORT_LEFT_JUMP:
                self.backward_short_left_jump()
            case Action.LONG_LEFT_JUMP:
                self.backward_long_left_jump()


    def backward_long_right_jump(self):
        ind = self.empty_space_index
        self.board[ind], self.board[ind + LONG_JUMP] = self.board[ind + LONG_JUMP], self.board[ind]
        self.empty_space_index += LONG_JUMP
        self.right_jumps -= LONG_JUMP

    def backward_short_right_jump(self):
        ind = self.empty_space_index
        self.board[ind], self.board[ind + SHORT_JUMP] = self.board[ind + SHORT_JUMP], self.board[ind]
        self.empty_space_index += SHORT_JUMP
        self.right_jumps -= SHORT_JUMP


    def backward_long_left_jump(self):
        ind = self.empty_space_index
        self.board[ind], self.board[ind - LONG_JUMP] = self.board[ind - LONG_JUMP], self.board[ind]
        self.empty_space_index -= LONG_JUMP
        self.left_jumps -= LONG_JUMP

    def backward_short_left_jump(self):
        ind = self.empty_space_index
        self.board[ind], self.board[ind - SHORT_JUMP] = self.board[ind - SHORT_JUMP], self.board[ind]
        self.empty_space_index -= SHORT_JUMP
        self.left_jumps -= SHORT_JUMP

    def __str__(self) -> str:
        return "".join([cell_to_str(cell) for cell in self.board])

def cell_to_str(cell: Cell) -> str:
    match cell:
        case Cell.EMPTY_SPACE:
            return "_"
        case Cell.RIGHT_FACING_FROG:
            return ">"
        case Cell.LEFT_FACING_FROG:
            return "<"

def find_solution(n: int) -> list[str] | None:
    initial_state = State.construct_initial_state(n)
    path = dfs(initial_state)

    if path is None:
        return None

    path.reverse()
    return path

def dfs(state: State) -> list[str] | None:
    if state.is_goal_state():
        return [str(state)]

    for action in ACTIONS:
        if state.forward_jump(action):
            result = dfs(state)
            state.backward_jump(action)
            if result is not None:
                result.append(str(state))
                return result

    return None

if __name__ == '__main__':
    n = int(input())
    solution = find_solution(n)

    if solution is None:
        print("There is no solution")
        exit(0)

    for board in solution:
        print(board)
