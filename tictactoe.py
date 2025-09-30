"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None

def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]

def player(board):
    """
    Returns player who has the next turn on a board.
    """
    x_count = sum(cell == X for row in board for cell in row)
    o_count = sum(cell == O for row in board for cell in row)

    return X if x_count == o_count else O

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    result = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                result.add((i, j))
    return result

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    i, j = action
    if action not in actions(board):
        raise Exception("Invalid move: action not allowed")
    
    new_board = copy.deepcopy(board)

    new_board[i][j] = player(board)
    
    return new_board

def winner(board):
    """
    Retourne le gagnant du jeux s'il y en a un
    """

    # si une ligne est identique on retourne le joueur
    for row in board:
        if row == [X, X, X]:
            return X
        elif row == [O, O, O]:
            return O

    # si une colonne est identique, on retourne le joueur
    for col in range(3):
        if [board[row][col] for row in range(3)] == [X, X, X]:
            return X
        elif [board[row][col] for row in range(3)] == [O, O, O]:
            return O

    # pour les diagonales
    if [board[i][i] for i in range(3)] == [X, X, X]:
        return X
    elif [board[i][i] for i in range(3)] == [O, O, O]:
        return O

    if [board[i][2 - i] for i in range(3)] == [X, X, X]:
        return X
    elif [board[i][2 - i] for i in range(3)] == [O, O, O]:
        return O

    return None

def terminal(board):
    """
    Retourne True si le jeu est tèrminé, False sinon
    """
    if winner(board):
        return True
    
    for row in board:
        if EMPTY in row:
            return False
    
    return True

def utility(board):
    """
    Retourne +1 si X à gagné, -1 si O à gagné et 0 si partie nulle
    """
    win = winner(board)
    if win == X:
        return 1
    elif win == O:
        return -1
    return 0

def minimax(board):
    """
    Retourne la meilleur action que le joueur puisse faire 
    en utilisant minimax
    """
    
    # si un joueur gagne ou c'est nul, il n'y a plus d'action
    if terminal(board):
        return None

    # on prend le joeur qui doit jouer
    current_player = player(board)

    # on initialise sa meilleur action
    best_action = None

    if current_player == X:
        # initialisation de la meilleur action de X 
        # -inf car on cherche le plus grand
        best_value = float('-inf')
        
        # pour chacune de ses actions possible, 
        # on prend la valeur minimum des actions que peut faire 0
        # si cette valeur est supérieur à la meilleure valeur précédente,
        #  alors cette action est la meilleure
        for action in actions(board):
            value = min_value(result(board, action))
            if value > best_value:
                best_value = value
                best_action = action
    else:
        # si c'est le joueur O
        
        # initialisation de la meilleur action de X 
        # inf car on cherche le min
        best_value = float('inf')
        
        # pour chacune de ses actions possible, 
        # on prend la valeur minimum des actions que peut faire X
        # si cette valeur est inf à la meilleure valeur précédente,
        #  alors cette action est la meilleure
        for action in actions(board):
            value = max_value(result(board, action))
            if value < best_value:
                best_value = value
                best_action = action

    return best_action

def max_value(board):
    """
    Retourne la valeur max d'une action
    """
    
    # on initialise la pire valeur que peut prendre X
    v = float('-inf')
    
    # si un joueur gagne, on retourne son score et c'est la fin
    if terminal(board):
        return utility(board)

    # sinon pour toutes les actions de X, 
    # on prendre le score max de l'action passée de X
    # et le min des actions de 0 à partir de cette action
    for action in actions(board):
        v = max(v, min_value(result(board, action)))
    return v

def min_value(board):
    """
    Retourne la valeur min d'une action
    """
    
    # on initialise la pire valeur que O peut prendre
    v = float('inf')
    
    # si un joueur gagne, on retourne son score et c'est la fin
    if terminal(board):
        return utility(board)

    # sinon pour toutes les actions de 0, on prendre le score min de l'action passée de O et le max des actions de X à partir de cette action
    for action in actions(board):
        v = min(v, max_value(result(board, action)))
    return v

def alphabeta_pruning(board):
    """
    Alpha Beta Pruning
    """
    if terminal(board):
        return None
    
    current_player = player(board)
    best_action = None

    if current_player == X:
        best_value = float('-inf')
        for action in actions(board):
            value = min_value_ab(result(board, action), alpha=float("-inf"), beta=float("inf"))
            if value > best_value:
                best_value = value
                best_action = action
                
    else:
        best_value = float('inf')
        for action in actions(board):
            value = max_value_ab(result(board, action), alpha=float("inf"), beta=float("-inf"))
            if value < best_value:
                best_value = value
                best_action = action

    return best_action

def max_value_ab(board, alpha, beta):
    """
    Retourne la valeur max d'une action
    """
    v = float('-inf')
    if terminal(board):
        return utility(board)
    for action in actions(board):
        v = max(v, min_value_ab(result(board, action), alpha, beta))
        alpha = max(alpha, v)
        if alpha >= beta:
            break
    return v

def min_value_ab(board, alpha, beta):
    """
    Retourne la valeur min d'une action
    """
    v = float('inf')
    if terminal(board):
        return utility(board)
    for action in actions(board):
        v = min(v, max_value_ab(result(board, action), alpha, beta))
        beta = min(beta, v)
        if beta <= alpha:
            break
    return v