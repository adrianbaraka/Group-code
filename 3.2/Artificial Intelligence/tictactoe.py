import time
import random

class TicTacToe:
    def __init__(self):
        self.board = [' ' for _ in range(9)]
        self.current_winner = None

    def print_board(self):
        for row in [self.board[i*3:(i+1)*3] for i in range(3)]:
            print('|'.join(row))
            print('-' * 5)

    def available_moves(self):
        return [i for i, spot in enumerate(self.board) if spot == ' ']

    def empty_squares(self):
        return ' ' in self.board

    def make_move(self, square, letter):
        if self.board[square] == ' ':
            self.board[square] = letter
            if self.winner(square, letter):
                self.current_winner = letter
            return True
        return False

    def winner(self, square, letter):
        # Check row
        row_ind = square // 3
        row = self.board[row_ind*3:(row_ind + 1)*3]
        if all([spot == letter for spot in row]):
            return True

        # Check column
        col_ind = square % 3
        column = [self.board[col_ind+i*3] for i in range(3)]
        if all([spot == letter for spot in column]):
            return True

        # Check diagonal
        if square % 2 == 0:
            diagonal1 = [self.board[i] for i in [0, 4, 8]]
            if all([spot == letter for spot in diagonal1]):
                return True
            diagonal2 = [self.board[i] for i in [2, 4, 6]]
            if all([spot == letter for spot in diagonal2]):
                return True
        return False

def minimax(game, maximizing):
    # Base cases
    if game.current_winner:
        return {'score': 1} if game.current_winner == 'X' else {'score': -1}
    if not game.empty_squares():
        return {'score': 0}

    if maximizing:
        best = {'score': -float('inf'), 'position': None}
        for possible_move in game.available_moves():
            game.make_move(possible_move, 'X')
            sim_score = minimax(game, False)
            game.board[possible_move] = ' '
            game.current_winner = None
            sim_score['position'] = possible_move
            
            if sim_score['score'] > best['score']:
                best = sim_score
        return best
    else:
        best = {'score': float('inf'), 'position': None}
        for possible_move in game.available_moves():
            game.make_move(possible_move, 'O')
            sim_score = minimax(game, True)
            game.board[possible_move] = ' '
            game.current_winner = None
            sim_score['position'] = possible_move
            
            if sim_score['score'] < best['score']:
                best = sim_score
        return best

def alpha_beta(game, maximizing, alpha=-float('inf'), beta=float('inf')):
    # Base cases
    if game.current_winner:
        return {'score': 1} if game.current_winner == 'X' else {'score': -1}
    if not game.empty_squares():
        return {'score': 0}

    if maximizing:
        best = {'score': -float('inf'), 'position': None}
        for possible_move in game.available_moves():
            game.make_move(possible_move, 'X')
            sim_score = alpha_beta(game, False, alpha, beta)
            game.board[possible_move] = ' '
            game.current_winner = None
            sim_score['position'] = possible_move
            
            if sim_score['score'] > best['score']:
                best = sim_score
            alpha = max(alpha, best['score'])
            if beta <= alpha:
                break
        return best
    else:
        best = {'score': float('inf'), 'position': None}
        for possible_move in game.available_moves():
            game.make_move(possible_move, 'O')
            sim_score = alpha_beta(game, True, alpha, beta)
            game.board[possible_move] = ' '
            game.current_winner = None
            sim_score['position'] = possible_move
            
            if sim_score['score'] < best['score']:
                best = sim_score
            beta = min(beta, best['score'])
            if beta <= alpha:
                break
        return best

def play_game(algorithm):
    game = TicTacToe()
    current_player = 'X'
    start_time = time.time()
    
    while game.empty_squares():
        if algorithm == 'minimax':
            move = minimax(game, current_player == 'X')
        else:
            move = alpha_beta(game, current_player == 'X')
            
        game.make_move(move['position'], current_player)
        # game.print_board()
        # print()
        
        if game.current_winner:
            break
        current_player = 'O' if current_player == 'X' else 'X'
    
    end_time = time.time()
    return end_time - start_time, game

# Run and compare both algorithms
print("Running Min-Max Algorithm:")
minimax_time, minimax_game = play_game('minimax')
print("Final board (Min-Max):")
minimax_game.print_board()
print(f"Time taken: {minimax_time:.4f} seconds")
print(f"Winner: {minimax_game.current_winner if minimax_game.current_winner else 'Draw'}\n")

print("Running Alpha-Beta Algorithm:")
alpha_beta_time, alpha_beta_game = play_game('alpha_beta')
print("Final board (Alpha-Beta):")
alpha_beta_game.print_board()
print(f"Time taken: {alpha_beta_time:.4f} seconds")
print(f"Winner: {alpha_beta_game.current_winner if alpha_beta_game.current_winner else 'Draw'}")
print(f"\nTime difference (Min-Max - Alpha-Beta): {minimax_time - alpha_beta_time:.4f} seconds")