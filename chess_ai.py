from chess_logic import BoardState, PieceColor, PieceType, ChessPiece
import math
import random

class ChessAI:
    def __init__(self, depth: int = 9999):
        self.depth = depth

    # Piece values for evaluation function
    # These values are standard, but can be tweaked for different AI personalities
    PIECE_VALUES = {
        PieceType.PAWN: 100,
        PieceType.KNIGHT: 320,
        PieceType.BISHOP: 330,
        PieceType.ROOK: 500,
        PieceType.QUEEN: 900,
        PieceType.KING: 20000 # King value is high as losing it means losing the game
    }

    def evaluate_board(self, board: BoardState, player_color: PieceColor) -> int:
        score = 0
        for piece in board.pieces:
            value = self.PIECE_VALUES.get(piece.type, 0)
            if piece.color == player_color:
                score += value
            else:
                score -= value
        
        # Add bonus for controlling the center
        center_squares = [(3, 3), (3, 4), (4, 3), (4, 4)]
        for r, c in center_squares:
            piece = board.get_piece_at(r, c)
            if piece:
                if piece.color == player_color:
                    score += 10 # Small bonus for center control
                else:
                    score -= 10

        # Positional scoring for pawns
        for r in range(8):
            for c in range(8):
                piece = board.get_piece_at(r, c)
                if piece and piece.type == PieceType.PAWN:
                    if piece.color == player_color:
                        # Advanced pawns get a bonus
                        if piece.color == PieceColor.WHITE:
                            score += (r - 1) * 5 # Further up the board is better
                        else: # Black
                            score += (6 - r) * 5 # Further down the board is better
                        
                        # Check for isolated pawns (no friendly pawns on adjacent files)
                        is_isolated = True
                        for dc in [-1, 1]:
                            if 0 <= c + dc <= 7:
                                for dr in range(8):
                                    adj_piece = board.get_piece_at(dr, c + dc)
                                    if adj_piece and adj_piece.type == PieceType.PAWN and adj_piece.color == player_color:
                                        is_isolated = False
                                        break
                            if not is_isolated:
                                break
                        if is_isolated:
                            score -= 20 # Penalty for isolated pawns
                    else: # Opponent's pawns
                        if piece.color == PieceColor.WHITE:
                            score -= (r - 1) * 5
                        else: # Black
                            score -= (6 - r) * 5
                        
                        is_isolated = True
                        for dc in [-1, 1]:
                            if 0 <= c + dc <= 7:
                                for dr in range(8):
                                    adj_piece = board.get_piece_at(dr, c + dc)
                                    if adj_piece and adj_piece.type == PieceType.PAWN and adj_piece.color != player_color:
                                        is_isolated = False
                                        break
                            if not is_isolated:
                                break
                        if is_isolated:
                            score += 20 # Opponent's isolated pawns are good for us

        # Positional scoring for knights (central knights are generally better)
        knight_positions = {\
            (0,0): -50, (0,1): -10, (0,2): -10, (0,3): -10, (0,4): -10, (0,5): -10, (0,6): -10, (0,7): -50,
            (1,0): -10, (1,1):   0, (1,2):   0, (1,3):   0, (1,4):   0, (1,5):   0, (1,6):   0, (1,7): -10,
            (2,0): -10, (2,1):   0, (2,2):  10, (2,3):  10, (2,4):  10, (2,5):  10, (2,6):   0, (2,7): -10,
            (3,0): -10, (3,1):   0, (3,2):  10, (3,3):  20, (3,4):  20, (3,5):  10, (3,6):   0, (3,7): -10,
            (4,0): -10, (4,1):   0, (4,2):  10, (4,3):  20, (4,4):  20, (4,5):  10, (4,6):   0, (4,7): -10,
            (5,0): -10, (5,1):   0, (5,2):  10, (5,3):  10, (5,4):  10, (5,5):  10, (5,6):   0, (5,7): -10,
            (6,0): -10, (6,1):   0, (6,2):   0, (6,3):   0, (6,4):   0, (6,5):   0, (6,6):   0, (6,7): -10,
            (7,0): -50, (7,1): -10, (7,2): -10, (7,3): -10, (7,4): -10, (7,5): -10, (7,6): -10, (7,7): -50
        }
        for piece in board.pieces:
            if piece.type == PieceType.KNIGHT:
                pos_value = knight_positions.get((piece.row, piece.col), 0)
                if piece.color == player_color:
                    score += pos_value
                else:
                    score -= pos_value

        # Positional scoring for rooks (open files, 7th rank)
        for piece in board.pieces:
            if piece.type == PieceType.ROOK:
                is_open_file = True
                for r in range(8):
                    if r != piece.row:
                        p = board.get_piece_at(r, piece.col)
                        if p and p.color == piece.color and p.type == PieceType.PAWN:
                            is_open_file = False
                            break
                if is_open_file:
                    if piece.color == player_color:
                        score += 30 # Bonus for rook on open file
                    else:
                        score -= 30
                
                # 7th rank control
                if (piece.color == PieceColor.WHITE and piece.row == 6) or \
                   (piece.color == PieceColor.BLACK and piece.row == 1):
                    if piece.color == player_color:
                        score += 40 # Bonus for rook on 7th rank
                    else:
                        score -= 40

        # Bishop pair bonus
        white_bishops = sum(1 for p in board.pieces if p.type == PieceType.BISHOP and p.color == PieceColor.WHITE)
        black_bishops = sum(1 for p in board.pieces if p.type == PieceType.BISHOP and p.color == PieceColor.BLACK)
        
        if player_color == PieceColor.WHITE and white_bishops >= 2:
            score += 50
        elif player_color == PieceColor.BLACK and black_bishops >= 2:
            score += 50
        elif player_color == PieceColor.WHITE and black_bishops >= 2:
            score -= 50
        elif player_color == PieceColor.BLACK and white_bishops >= 2:
            score -= 50

        # Add penalty for king exposure (simplified)
        king = next((p for p in board.pieces if p.type == PieceType.KING and p.color == player_color), None)
        if king:
            enemy_color = PieceColor.BLACK if player_color == PieceColor.WHITE else PieceColor.WHITE
            if board.is_square_attacked(king.row, king.col, enemy_color):
                score -= 50 # Penalty for king in check

        return score

    def find_best_move(self, board: BoardState, ai_color: PieceColor):
        best_move = None
        if ai_color == PieceColor.WHITE:
            max_eval = -math.inf
            for piece in board.pieces:
                if piece.color == ai_color:
                    for move in board.calculate_possible_moves(piece):
                        new_board = board.apply_move(piece, move[0], move[1])
                        eval = self.minimax(new_board, self.depth - 1, -math.inf, math.inf, ai_color, False)
                        if eval > max_eval:
                            max_eval = eval
                            best_move = (piece, move)
            return best_move
        else: # AI is Black
            min_eval = math.inf
            for piece in board.pieces:
                if piece.color == ai_color:
                    for move in board.calculate_possible_moves(piece):
                        new_board = board.apply_move(piece, move[0], move[1])
                        eval = self.minimax(new_board, self.depth - 1, -math.inf, math.inf, ai_color, True)
                        if eval < min_eval:
                            min_eval = eval
                            best_move = (piece, move)
            return best_move

    def minimax(self, board: BoardState, depth: int, alpha: int, beta: int, ai_color: PieceColor, is_maximizing_player: bool) -> int:
        if depth == 0 or board.is_checkmate(board.current_turn) or board.is_stalemate(board.current_turn):
            return self.evaluate_board(board, ai_color)

        if is_maximizing_player: # AI's turn
            max_eval = -math.inf
            for piece in board.pieces:
                if piece.color == board.current_turn:
                    for move in board.calculate_possible_moves(piece):
                        new_board = board.apply_move(piece, move[0], move[1])
                        eval = self.minimax(new_board, depth - 1, alpha, beta, ai_color, False)
                        max_eval = max(max_eval, eval)
                        alpha = max(alpha, eval)
                        if beta <= alpha:
                            break
                if beta <= alpha: # Check outer loop as well
                    break
            return max_eval
        else: # Opponent's turn
            min_eval = math.inf
            for piece in board.pieces:
                if piece.color == board.current_turn:
                    for move in board.calculate_possible_moves(piece):
                        new_board = board.apply_move(piece, move[0], move[1])
                        eval = self.minimax(new_board, depth - 1, alpha, beta, ai_color, True)
                        min_eval = min(min_eval, eval)
                        beta = min(beta, eval)
                        if beta <= alpha:
                            break
                if beta <= alpha: # Check outer loop as well
                    break
            return min_eval
