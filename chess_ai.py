from chess_logic import BoardState, PieceColor, PieceType, ChessPiece
import math
import random

class ChessAI:
    def __init__(self, depth: int = 3):
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
