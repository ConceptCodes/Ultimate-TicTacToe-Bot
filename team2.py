from time import time
from copy import deepcopy

# import datetime

# from test import MOVE

global block_heuristics
global place_values
# global=[]
place_values = [[0.3, 0.2, 0.2, 0.3], [0.2, 0.3, 0.3, 0.2], [0.2, 0.3, 0.3, 0.2], [0.3, 0.2, 0.2, 0.3]]

block_heuristics = [0 for i in range(16)]


class Player2:
    def __init__(self):
        # self.old_time = 0
        pass

    def find_allowed_cells(self, board, oldmove, block):
        # print 'in allowed cells'
        x = oldmove[0] % 4
        y = oldmove[1] % 4

        fx = (oldmove[0] % 4) * 4
        fy = (oldmove[1] % 4) * 4
        allowed_cells = []

        if block[x][y] is not '-':
            allowed_cells = self.random_allotment(board, block)
            return allowed_cells, 1
        else:
            # print x,y
            for i in range(0, 4):
                for j in range(0, 4):
                    if board[fx + i][fy + j] == '-':
                        allowed_cells.append((fx + i, fy + j))

        # print allowed_cells
        return allowed_cells, 0

    def find_allowed_cells_move(self, board, oldmove):
        # print 'in allowed cells'
        x = (oldmove[0] % 4) * 4
        y = (oldmove[1] % 4) * 4
        # print x,y
        allowed_cells = []

        for i in range(0, 4):
            for j in range(0, 4):
                if board[x + i][y + j] == '-':
                    allowed_cells.append((x + i, y + j))
        # print allowed_cells
        return allowed_cells

    def check_block(self, board, old_move):
        x = (old_move[0] % 4)
        y = (old_move[1] % 4)

        if board.block_status[x][y] != '-':
            return 0

        x *= 4
        y *= 4

        for i in range(x, x + 4):
            if board.board_status[i][y] == board.board_status[i][y + 1] == board.board_status[i][y + 2] == \
                    board.board_status[i][y + 3] and (
                            board.board_status[i][y] == 'x' or board.board_status[i][y] == 'o'):
                return 0

        for i in range(y, y + 4):
            if board.board_status[x][i] == board.board_status[x + 1][i] == board.board_status[x + 2][i] == \
                    board.board_status[x + 3][i] and (
                            board.board_status[x][i] == 'x' or board.board_status[x][i] == 'o'):
                return 0

        if board.board_status[x][y] == board.board_status[x + 1][y + 1] == board.board_status[x + 2][y + 2] == \
                board.board_status[x + 3][y + 3] and (
                        board.board_status[x][y] == 'x' or board.board_status[x][y] == 'o'):
            return 0

        if (board.board_status[x][y + 3] == board.board_status[x + 1][y + 2] == board.board_status[x + 2][y + 1] ==
                board.board_status[x + 3][y] and (
                        board.board_status[x][y + 3] == 'x' or board.board_status[x][y + 3] == 'o')):
            return 0

        return 1

    def empty_cells(self, board, old_move):
        x = (old_move[0] % 4) * 4
        y = (old_move[1] % 4) * 4

        for i in range(0, 4):
            for j in range(0, 4):
                if board.board_status[x + i][y + j] == '-':
                    return 1
        return 0

    def random_allotment(self, board, block):
        # print 'in random'
        allowed_cells = []
        # x = (old_move[0] % 4) * 4
        # y = (old_move[1] % 4) * 4

        for i in range(0, 16):
            for j in range(0, 16):
                # print i,j
                if board[i][j] == '-' and block[i / 4][j / 4] == '-':
                    allowed_cells.append((i, j))

        return allowed_cells

    def initial(self, board):
        allowed_cells = []

        for i in range(0, 16):
            for j in range(0, 16):
                if board.board_status[i][j] == '-':
                    allowed_cells.append((i, j))

        return allowed_cells

    def evaluate(self, board, tx, ty, player, x, y):

        # global level
        # print level
        xnew = tx - (tx % 4)
        ynew = ty - (ty % 4)
        sumval = 0
        #
        # # print 'in evaluate, board is:'
        # # for p in range(xnew,xnew+4):
        # #     print board[p][ynew], board[p][ynew + 1], board[p][ynew + 2], board[p][ynew + 3]
        # # print 'in evaluate'
        # # print 'xnew=',xnew,'ynew=',ynew,'player=',player
        #
        ax = [0 for i in range(10)]
        ao = [0 for i in range(10)]

        # countr1x =
        ax[0] = (board[xnew][ynew], board[xnew][ynew + 1], board[xnew][ynew + 2], board[xnew][ynew + 3]).count('x')
        # countr2x
        ax[1] = (
            board[xnew + 1][ynew], board[xnew + 1][ynew + 1], board[xnew + 1][ynew + 2],
            board[xnew + 1][ynew + 3]).count(
            'x')
        # countr3x
        ax[2] = (
            board[xnew + 2][ynew], board[xnew + 2][ynew + 1], board[xnew + 2][ynew + 2],
            board[xnew + 2][ynew + 3]).count(
            'x')
        # countr4x
        ax[3] = (
            board[xnew + 3][ynew], board[xnew + 3][ynew + 1], board[xnew + 3][ynew + 2],
            board[xnew + 3][ynew + 3]).count(
            'x')

        # countc1x
        ax[4] = (board[xnew][ynew], board[xnew + 1][ynew], board[xnew + 2][ynew], board[xnew + 3][ynew]).count('x')
        # countc2x
        ax[5] = (
            board[xnew][ynew + 1], board[xnew + 1][ynew + 1], board[xnew + 2][ynew + 1],
            board[xnew + 3][ynew + 1]).count(
            'x')
        # countc3x
        ax[6] = (
            board[xnew][ynew + 2], board[xnew + 1][ynew + 2], board[xnew + 2][ynew + 2],
            board[xnew + 3][ynew + 2]).count(
            'x')
        # countc4x
        ax[7] = (
            board[xnew][ynew + 3], board[xnew + 1][ynew + 3], board[xnew + 2][ynew + 3],
            board[xnew + 3][ynew + 3]).count(
            'x')

        # countr1o
        ao[0] = (board[xnew][ynew], board[xnew][ynew + 1], board[xnew][ynew + 2], board[xnew][ynew + 3]).count('o')
        # countr2o
        ao[1] = (
            board[xnew + 1][ynew], board[xnew + 1][ynew + 1], board[xnew + 1][ynew + 2],
            board[xnew + 1][ynew + 3]).count(
            'o')
        # countr3o
        ao[2] = (
            board[xnew + 2][ynew], board[xnew + 2][ynew + 1], board[xnew + 2][ynew + 2],
            board[xnew + 2][ynew + 3]).count(
            'o')
        # countr4o
        ao[3] = (
            board[xnew + 3][ynew], board[xnew + 3][ynew + 1], board[xnew + 3][ynew + 2],
            board[xnew + 3][ynew + 3]).count(
            'o')

        # countc1o
        ao[4] = (board[xnew][ynew], board[xnew + 1][ynew], board[xnew + 2][ynew], board[xnew + 3][ynew]).count('o')
        # countc2o
        ao[5] = (
            board[xnew][ynew + 1], board[xnew + 1][ynew + 1], board[xnew + 2][ynew + 1],
            board[xnew + 3][ynew + 1]).count(
            'o')
        # countc3o
        ao[6] = (
            board[xnew][ynew + 2], board[xnew + 1][ynew + 2], board[xnew + 2][ynew + 2],
            board[xnew + 3][ynew + 2]).count(
            'o')
        # countc4o
        ao[7] = (
            board[xnew][ynew + 3], board[xnew + 1][ynew + 3], board[xnew + 2][ynew + 3],
            board[xnew + 3][ynew + 3]).count(
            'o')

        # countd1x
        ax[8] = (
            board[xnew][ynew], board[xnew + 1][ynew + 1], board[xnew + 2][ynew + 2], board[xnew + 3][ynew + 3]).count(
            'x')
        # countd1o
        ao[8] = (
            board[xnew][ynew], board[xnew + 1][ynew + 1], board[xnew + 2][ynew + 2], board[xnew + 3][ynew + 3]).count(
            'o')

        # countd2x
        ax[9] = (
            board[xnew][ynew + 3], board[xnew + 1][ynew + 2], board[xnew + 2][ynew + 1], board[xnew + 3][ynew]).count(
            'x')
        # countd2o
        ao[9] = (
            board[xnew][ynew + 3], board[xnew + 1][ynew + 2], board[xnew + 2][ynew + 1], board[xnew + 3][ynew]).count(
            'o')

        tcount = 0
        for i in range(4):
            for j in range(4):
                if board[xnew + i][ynew + j] == '-':
                    tcount += 1
        if tcount is 0:
            return 0
        # return 0
        # if level==2:
        if player == 'x':
            for i in range(10):
                if ax[i] != 0 and ao[i] != 0:
                    continue
                elif ax[i] != 0:
                    temp = 1
                    for j in range(ax[i] - 1):
                        temp *= 10
                    sumval += temp
                elif ao[i] != 0:
                    temp = 1
                    for j in range(ao[i] - 1):
                        temp *= 10
                    sumval -= temp
                    # global place_values
                    # for i in range(0,4):
                    #     for j in range(0,4):
                    #         if board[xnew+i][xnew+j] == 'x':
                    #             sumval+=place_values[i][j]
                    #         elif board[xnew+i][xnew+j] == 'o':
                    #             sumval-=place_values[i][j]

        else:
            for i in range(10):
                if ax[i] != 0 and ao[i] != 0:
                    continue
                elif ax[i] != 0:
                    temp = 1
                    for j in range(ax[i] - 1):
                        temp *= 10
                    sumval -= temp
                elif ao[i] != 0:
                    temp = 1
                    for j in range(ao[i] - 1):
                        temp *= 10
                    sumval += temp
                    # global place_values
                    #
                    # for i in range(0,4):
                    #     for j in range(0,4):
                    #         if board[xnew+i][xnew+j] == 'o':
                    #             sumval+=place_values[i][j]
                    #         elif board[xnew+i][xnew+j] == 'x':
                    #             sumval-=place_values[i][j]

        # if level==1:
        win_flag = 0
        for i in range(10):
            if ao[i] == 4 or ax[i] == 4:
                win_flag = 1
        my_char = deepcopy(board[x][y])
        # print 'in level 1.',my_char
        board[x][y] = '-'
        # print my_char
        row = x % 4
        flag_t = 0
        column = y % 4 + 4
        diag = 0
        # print row, column
        if x % 4 == y % 4:
            diag = 8
            flag_t = 1
        elif (xnew == x and (ynew + 3) == y) or (xnew + 1 == x and ynew + 2 == y) or (
                            xnew + 2 == x and ynew + 1 == y) or (xnew + 3 == x and ynew == y):
            diag = 9
            flag_t = 1
        # print diag
        if my_char == 'x' and win_flag == 0:
            # print 'x hai'
            ax[row] -= 1
            ax[column] -= 1
            if flag_t == 1:
                ax[diag] -= 1
            if (ao[row] == 3) and ax[row] == 0:
                # print 'i am x in level 1. 3 o in a row.'
                if player == 'x':
                    sumval += 0.5 * (10 ** (ao[row] - 1))
                if player == 'o':
                    sumval -= 0.5 * (10 ** (ao[row] - 1))
            if (ao[column] == 3) and ax[column] == 0:
                # print 'i am x in level 1. 3 o in a col.'
                if player == 'x':
                    sumval += 0.5 * (10 ** (ao[column] - 1))
                if player == 'o':
                    sumval -= 0.5 * (10 ** (ao[column] - 1))
            if (ao[diag] == 3) and flag_t == 1 and ax[diag] == 0:
                # print 'i am x in level 1. 3 o in a diag.'
                if player == 'x':
                    sumval += 0.5 * (10 ** (ao[diag] - 1))
                if player == 'o':
                    sumval -= 0.5 * (10 ** (ao[diag] - 1))
            ax[row] += 1
            ax[column] += 1
            if flag_t == 1:
                ax[diag] += 1

        if my_char == 'o' and win_flag == 0:
            # print 'o hai'
            ao[row] -= 1
            ao[column] -= 1
            if flag_t == 1:
                ao[diag] -= 1
            if (ax[row] == 3) and ao[row] == 0:
                if player == 'o':
                    sumval += 0.5 * (10 ** (ax[row] - 1))
                if player == 'x':
                    sumval -= 0.5 * (10 ** (ax[row] - 1))
            if (ax[column] == 3) and ao[column] == 0:
                if player == 'o':
                    sumval += 0.5 * (10 ** (ax[column] - 1))
                if player == 'x':
                    sumval -= 0.5 * (10 ** (ax[column] - 1))
            if (ax[diag] == 3) and flag_t == 1 and ao[diag] == 0:
                if player == 'o':
                    sumval += 0.5 * (10 ** (ax[diag] - 1))
                if player == 'x':
                    sumval -= 0.5 * (10 ** (ax[diag] - 1))
            ax[row] += 1
            ax[column] += 1
            if flag_t == 1:
                ax[diag] += 1
        board[x][y] = my_char
        # print level

        if win_flag == 1:
            return sumval / 1000.0

        elif win_flag == 0:
            return sumval / 1300.0

    def evaluate_board(self):
        heu = 0
        flag = 0
        # print 'in evaluate_board. Level is ',level

        for i in range(4):
            flag = 0
            temp = block_heuristics[4 * i] + block_heuristics[4 * i + 1] + block_heuristics[4 * i + 2] + \
                   block_heuristics[4 * i + 3]
            if temp < 0:
                flag = 1
                temp *= -1
            if 0 <= temp <= 1:
                val = temp
            elif 1 < temp <= 2:
                val = 1 + 9 * (temp - 1)
            elif 2 < temp <= 3:
                val = 10 + 90 * (temp - 2)
            elif 3 < temp < 4:
                val = 100 + 900 * (temp - 3)
            elif temp >= 4:
                val = 10000
            if flag == 1:
                heu -= val
                flag = 0
            else:
                heu += val
        for i in range(4):
            temp = block_heuristics[i] + block_heuristics[i + 4] + block_heuristics[i + 8] + block_heuristics[i + 12]
            if temp < 0:
                flag = 1
                temp *= -1
            if 0 <= temp <= 1:
                val = temp
            elif 1 < temp <= 2:
                val = 1 + 9 * (temp - 1)
            elif 2 < temp <= 3:
                val = 10 + 90 * (temp - 2)
            elif 3 < temp < 4:
                val = 100 + 900 * (temp - 3)
            elif temp >= 4:
                val = 10000
            if flag == 1:
                heu -= val
                flag = 0
            else:
                heu += val
        temp = block_heuristics[0] + block_heuristics[5] + block_heuristics[10] + block_heuristics[15]
        flag = 0
        if temp < 0:
            flag = 1
            temp *= -1
        if 0 <= temp <= 1:
            val = temp
        elif 1 < temp <= 2:
            val = 1 + 9 * (temp - 1)
        elif 2 < temp <= 3:
            val = 10 + 90 * (temp - 2)
        elif 3 < temp < 4:
            val = 100 + 900 * (temp - 3)
        elif temp >= 4:
            val = 10000
        if flag == 1:
            heu -= val
            flag = 0
        else:
            heu += val

        temp = block_heuristics[3] + block_heuristics[6] + block_heuristics[9] + block_heuristics[12]
        flag = 0
        if temp < 0:
            flag = 1
            temp *= -1
        if 0 <= temp <= 1:
            val = temp
        elif 1 < temp <= 2:
            val = 1 + 9 * (temp - 1)
        elif 2 < temp <= 3:
            val = 10 + 90 * (temp - 2)
        elif 3 < temp < 4:
            val = 100 + 900 * (temp - 3)
        elif temp >= 4:
            val = 10000
        if flag == 1:
            heu -= val
            flag = 0
        else:
            heu += val

        return heu

    def minmax(self, board, block, ismax, x, y, player, depth, alpha, beta, Parentalpha, Parentbeta, old_time,
               current_depth):
        # xnew = (x % 4) * 4
        # ynew = (y % 4) * 4

        # print xnew,ynew

        if player == 'x':
            nextplayer = 'o'
        else:
            nextplayer = 'x'

        new_time = time()
        if new_time - old_time > 14 or depth >= current_depth:
            # print 'time up or depth finished'
            # print 'stopped at depth=', depth
            # if depth == 5:
            if ismax == 1:
                d = self.evaluate_board()
            else:
                d = self.evaluate_board()
            # print 'd returned is', d
            return d

        if ismax == 1:
            # print 'max payer'
            allowed_cells, notgo = self.find_allowed_cells(board, [x, y], block)
            # if notgo is 1:
            #     return -100

            # print allowed_cells

            if len(allowed_cells) is 0:
                # if ismax===1:
                d = self.evaluate_board()
                # else:
                #     d = self.evaluate_board(block,nextplayer)
                # print 'd returned is', d
                return d
            temp_heuristic = self.fetch_heuristic(x, y)
            board[x][y] = player
            # latest_move = [x,y]
            self.update_heuristic(board, x, y, player)
            for p in range(len(allowed_cells)):
                i = allowed_cells[p][0]
                j = allowed_cells[p][1]
                beta = Parentbeta
                if alpha < beta:
                    best = self.minmax(board, block, not ismax, i, j, nextplayer, depth + 1, -1000000000003,
                                       1000000000003, alpha,
                                       beta, old_time, current_depth)
                    # print best
                    if alpha < best:
                        alpha = best
                        # board[i][j]='-'
                        # self.update_heuristic(board,i,j,nextplayer)
                else:
                    break
            board[x][y] = '-'
            self.restore_heuristic(x, y, temp_heuristic)
            # self.update_heuristic(board, x, y, player)
            return alpha
        else:
            # print 'min'
            allowed_cells, notgo = self.find_allowed_cells(board, [x, y], block)

            if len(allowed_cells) is 0:
                # if ismax==1:
                d = self.evaluate_board()
                # else:
                #     d = self.evaluate_board(block,)
                # print 'd returned is', d
                return d

            temp_heuristic = self.fetch_heuristic(x, y)
            board[x][y] = player
            self.update_heuristic(board, x, y, nextplayer)
            for p in range(len(allowed_cells)):
                i = allowed_cells[p][0]
                j = allowed_cells[p][1]
                # print 'i=',i,'j=',j
                alpha = Parentalpha
                if alpha < beta:
                    best = self.minmax(board, block, not ismax, i, j, nextplayer, depth + 1, -1000000000003,
                                       1000000000003, alpha,
                                       beta, old_time, current_depth)
                    # print best
                    if beta > best:
                        beta = best
                        # board[i][j]='-'
                        # self.update_heuristic(board,i,j,nextplayer)

                else:

                    break
            board[x][y] = '-'
            self.restore_heuristic(x, y, temp_heuristic)
            # self.update_heuristic(board, x, y, nextplayer)
            return beta

    def fetch_heuristic(self, x, y):
        global block_heuristics
        temp1 = x - x % 4
        temp2 = y - y % 4
        val = block_heuristics[temp1 + (temp2 / 4)]
        return val

    def restore_heuristic(self, x, y, val):
        global block_heuristics
        temp1 = x - x % 4
        temp2 = y - y % 4
        block_heuristics[temp1 + (temp2 / 4)] = val

    def update_heuristic(self, board, x, y, player):
        global block_heuristics
        temp1 = x - x % 4
        temp2 = y - y % 4
        # print temp1, temp2 , x, y
        h = self.evaluate(board, temp1, temp2, player, x, y)
        # print 't'

        # print h
        block_heuristics[temp1 + (temp2 / 4)] = h

    def number_free_cells(self, board):
        count = 0
        for i in range(16):
            for j in range(16):
                if board[i][j] == '-':
                    count += 1
        return count

    def move(self, board, old_move, player):
        # print old_move
        global block_heuristics
        global level
        old_time = time()
        g = 0
        f = 0
        flag = self.check_block(board, old_move)  # Check to see if block is conquered
        flag2 = self.empty_cells(board, old_move)  # Check to see if block is full
        # cells = []
        free_cells = self.number_free_cells(board.board_status)
        # print 'free cells',free_cells
        # if free_cells > 120:
        #     level=1
        # else:
        #     level=2
        # print 'pranav'
        if old_move[0] is -1 and old_move[1] is -1:
            # cells = self.initial(board)
            return 1, 13
        elif flag is 1 and flag2 is 1:  # when block is not conquered and there are empty cells
            cells = self.find_allowed_cells_move(board.board_status, old_move)
        else:
            cells = self.random_allotment(board.board_status, board.block_status)
            temp = len(cells)
            # for i in range(temp / 2):
            #     cells.remove(cells[0])
            # print cells
        # for p in range(4):
        #     for q in range(4):
                # self.update_heuristic(board.board_status, p * 4, q * 4, player)
        # print block_heuristics
        finalf = 0
        finalg = 0
        # print cells,len(cells)
        current_depth = 3
        new_time = time()
        best = -1000000000003  # -10 ** 12 - 3
        while new_time - old_time < 14:

            # tcount = 0
            for i in range(0, len(cells)):

                # tcount += 1
                x1, y1 = cells[i][0], cells[i][1]
                # print x1,y1
                # print 'going into main move loop for',x1,y1
                h = self.minmax(board.board_status, board.block_status, 1, x1, y1, player, 0, -1000000000002,
                                1000000000002,
                                -1000000000002, 1000000000002, old_time, current_depth)
                # print 'hello'

                if h > best:
                    f, g = x1, y1
                    best = h
                    # print best

                board.board_status[x1][y1] = '-'
            new_time = time()
            if new_time - old_time < 14:
                if current_depth >= 3:
                    print current_depth
                finalf = f
                finalg = g
                new_time = time()
                # if level==2:
                current_depth += 1
                # else:
                # current_depth=3

        # print f, g
        board.board_status[finalf][finalg] = player
        # self.update_heuristic(board.board_status, finalf, finalg, player)
        board.board_status[finalf][finalg] = '-'
        print finalf, finalg
        # print 'level=',level
        return finalf, finalg
