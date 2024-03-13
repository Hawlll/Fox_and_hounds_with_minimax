
from helper_functions import simulate
from constants import HOUND_ICON, FOX_ICON
 
def minimax(board, maximizer, depth, alpha=float('-inf'), beta=float('inf')):

    """
    minimax() recursively finds best possible move and evaluation for desired player. Uses alpha-pruning technique for optmization.

    board: grid of board object
    maximizer: (True or False). False if fox's turn or True for hound's turn
    depth: number of moves looked into the future
    alpha: highest score (leave as default) 
    beta: lowest score (leave as default)

    """


    if depth == 0 or board.is_win(FOX_ICON) or board.is_win(HOUND_ICON):
        return board.evaluation(), None
        
    if maximizer:
        best_score = float('-inf')
        best_move = None
        for move in board.get_all_moves(HOUND_ICON): # move = [move_col, move_row, [hound_col, hound_row]]
            pos = [move[2][0], move[2][1]]
            simulated_board = simulate(board, move[1], move[0], HOUND_ICON, pos)
            score, _ = minimax(simulated_board, False, depth-1, alpha, beta)
            if score > best_score:
                best_score = score
                best_move = move
            alpha = max(alpha, best_score)
            if alpha >= beta:
                break
        return best_score, best_move

    else:
        min_score = float('inf')
        best_move = None
        for move in board.get_all_moves(FOX_ICON):
            simulated_board = simulate(board, move[1], move[0], FOX_ICON)
            score, _ = minimax(simulated_board, True, depth-1, alpha, beta)
            if score < min_score:
                min_score = score
                best_move = move
            beta = min(beta, min_score)
            if beta <= alpha:
                break
        return min_score, best_move
