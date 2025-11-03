from enum import Enum

class PieceType(Enum):
    PAWN = 1
    ROOK = 2
    KNIGHT = 3
    BISHOP = 4
    QUEEN = 5
    KING = 6

class PieceColor(Enum):
    WHITE = 1
    BLACK = 2

class ChessPiece:
    def __init__(self, type: PieceType, color: PieceColor, row: int, col: int, has_moved: bool = False):
        self.type = type
        self.color = color
        self.row = row
        self.col = col
        self.has_moved = has_moved

    def __repr__(self):
        return f"ChessPiece({self.type.name}, {self.color.name}, {self.row}, {self.col})"

    def __eq__(self, other):
        if not isinstance(other, ChessPiece):
            return NotImplemented
        return self.type == other.type and self.color == other.color and self.row == other.row and self.col == other.col

    def __hash__(self):
        return hash((self.type, self.color, self.row, self.col))

class BoardState:
    def __init__(self, pieces=None, current_turn: PieceColor = PieceColor.WHITE, en_passant_target_square=None):
        self.pieces = pieces if pieces is not None else []
        self.current_turn = current_turn
        self.en_passant_target_square = en_passant_target_square

        if not self.pieces:
            self._setup_initial_board()

    def _setup_initial_board(self):
        # Black pieces
        self.pieces.append(ChessPiece(PieceType.ROOK, PieceColor.BLACK, 0, 0))
        self.pieces.append(ChessPiece(PieceType.KNIGHT, PieceColor.BLACK, 0, 1))
        self.pieces.append(ChessPiece(PieceType.BISHOP, PieceColor.BLACK, 0, 2))
        self.pieces.append(ChessPiece(PieceType.QUEEN, PieceColor.BLACK, 0, 3))
        self.pieces.append(ChessPiece(PieceType.KING, PieceColor.BLACK, 0, 4))
        self.pieces.append(ChessPiece(PieceType.BISHOP, PieceColor.BLACK, 0, 5))
        self.pieces.append(ChessPiece(PieceType.KNIGHT, PieceColor.BLACK, 0, 6))
        self.pieces.append(ChessPiece(PieceType.ROOK, PieceColor.BLACK, 0, 7))
        for i in range(8):
            self.pieces.append(ChessPiece(PieceType.PAWN, PieceColor.BLACK, 1, i))

        # White pieces
        for i in range(8):
            self.pieces.append(ChessPiece(PieceType.PAWN, PieceColor.WHITE, 6, i))
        self.pieces.append(ChessPiece(PieceType.ROOK, PieceColor.WHITE, 7, 0))
        self.pieces.append(ChessPiece(PieceType.KNIGHT, PieceColor.WHITE, 7, 1))
        self.pieces.append(ChessPiece(PieceType.BISHOP, PieceColor.WHITE, 7, 2))
        self.pieces.append(ChessPiece(PieceType.QUEEN, PieceColor.WHITE, 7, 3))
        self.pieces.append(ChessPiece(PieceType.KING, PieceColor.WHITE, 7, 4))
        self.pieces.append(ChessPiece(PieceType.BISHOP, PieceColor.WHITE, 7, 5))
        self.pieces.append(ChessPiece(PieceType.KNIGHT, PieceColor.WHITE, 7, 6))
        self.pieces.append(ChessPiece(PieceType.ROOK, PieceColor.WHITE, 7, 7))

    def get_piece_at(self, row: int, col: int):
        for piece in self.pieces:
            if piece.row == row and piece.col == col:
                return piece
        return None

    def is_occupied(self, row: int, col: int) -> bool:
        return self.get_piece_at(row, col) is not None

    def is_occupied_by_ally(self, row: int, col: int, color: PieceColor) -> bool:
        piece = self.get_piece_at(row, col)
        return piece is not None and piece.color == color

    def is_occupied_by_enemy(self, row: int, col: int, color: PieceColor) -> bool:
        piece = self.get_piece_at(row, col)
        return piece is not None and piece.color != color

    def is_square_attacked(self, row: int, col: int, by_color: PieceColor) -> bool:
        # Check for Pawn attacks
        if by_color == PieceColor.WHITE:
            if self.get_piece_at(row + 1, col - 1) and self.get_piece_at(row + 1, col - 1).type == PieceType.PAWN and self.get_piece_at(row + 1, col - 1).color == by_color: return True
            if self.get_piece_at(row + 1, col + 1) and self.get_piece_at(row + 1, col + 1).type == PieceType.PAWN and self.get_piece_at(row + 1, col + 1).color == by_color: return True
        else: # Black pawns
            if self.get_piece_at(row - 1, col - 1) and self.get_piece_at(row - 1, col - 1).type == PieceType.PAWN and self.get_piece_at(row - 1, col - 1).color == by_color: return True
            if self.get_piece_at(row - 1, col + 1) and self.get_piece_at(row - 1, col + 1).type == PieceType.PAWN and self.get_piece_at(row - 1, col + 1).color == by_color: return True

        # Check for Knight attacks
        knight_moves = [
            (-2, -1), (-2, 1), (-1, -2), (-1, 2),
            (1, -2), (1, 2), (2, -1), (2, 1)
        ]
        for dr, dc in knight_moves:
            r, c = row + dr, col + dc
            piece = self.get_piece_at(r, c)
            if piece and piece.type == PieceType.KNIGHT and piece.color == by_color: return True

        # Check for King attacks (only one square away)
        king_moves = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]
        for dr, dc in king_moves:
            r, c = row + dr, col + dc
            piece = self.get_piece_at(r, c)
            if piece and piece.type == PieceType.KING and piece.color == by_color: return True

        # Check for Rook/Queen (horizontal/vertical) attacks
        straight_directions = [
            (-1, 0), (1, 0), (0, -1), (0, 1)
        ]
        for dr, dc in straight_directions:
            r, c = row + dr, col + dc
            while 0 <= r <= 7 and 0 <= c <= 7:
                piece = self.get_piece_at(r, c)
                if piece:
                    if piece.color == by_color and (piece.type == PieceType.ROOK or piece.type == PieceType.QUEEN): return True
                    break # Blocked by another piece (either ally or enemy)
                r += dr
                c += dc

        # Check for Bishop/Queen (diagonal) attacks
        diagonal_directions = [
            (-1, -1), (-1, 1), (1, -1), (1, 1)
        ]
        for dr, dc in diagonal_directions:
            r, c = row + dr, col + dc
            while 0 <= r <= 7 and 0 <= c <= 7:
                piece = self.get_piece_at(r, c)
                if piece:
                    if piece.color == by_color and (piece.type == PieceType.BISHOP or piece.type == PieceType.QUEEN): return True
                    break # Blocked by another piece (either ally or enemy)
                r += dr
                c += dc

        return False

    def is_king_in_check(self, color: PieceColor) -> bool:
        king = next((p for p in self.pieces if p.type == PieceType.KING and p.color == color), None)
        if king is None: return False # Should not happen in a valid game

        enemy_color = PieceColor.BLACK if color == PieceColor.WHITE else PieceColor.WHITE
        return self.is_square_attacked(king.row, king.col, enemy_color)

    def can_castle_king_side(self, color: PieceColor) -> bool:
        king = next((p for p in self.pieces if p.type == PieceType.KING and p.color == color), None)
        king_side_rook = next((p for p in self.pieces if p.type == PieceType.ROOK and p.color == color and p.col == 7), None)

        if king is None or king_side_rook is None: return False
        if king.has_moved or king_side_rook.has_moved: return False

        king_row = king.row
        enemy_color = PieceColor.BLACK if color == PieceColor.WHITE else PieceColor.WHITE

        # Check if squares between King and Rook are empty
        if self.is_occupied(king_row, 5) or self.is_occupied(king_row, 6): return False

        # Check if King is in check or passes through attacked squares
        if self.is_square_attacked(king_row, 4, enemy_color): return False # King's current position
        if self.is_square_attacked(king_row, 5, enemy_color): return False # Square King passes through
        if self.is_square_attacked(king_row, 6, enemy_color): return False # Square King lands on

        return True

    def can_castle_queen_side(self, color: PieceColor) -> bool:
        king = next((p for p in self.pieces if p.type == PieceType.KING and p.color == color), None)
        queen_side_rook = next((p for p in self.pieces if p.type == PieceType.ROOK and p.color == color and p.col == 0), None)

        if king is None or queen_side_rook is None: return False
        if king.has_moved or queen_side_rook.has_moved: return False

        king_row = king.row
        enemy_color = PieceColor.BLACK if color == PieceColor.WHITE else PieceColor.WHITE

        # Check if squares between King and Rook are empty
        if self.is_occupied(king_row, 1) or self.is_occupied(king_row, 2) or self.is_occupied(king_row, 3): return False

        # Check if King is in check or passes through attacked squares
        if self.is_square_attacked(king_row, 4, enemy_color): return False # King's current position
        if self.is_square_attacked(king_row, 3, enemy_color): return False # Square King passes through
        if self.is_square_attacked(king_row, 2, enemy_color): return False # Square King lands on

        return True

    def calculate_possible_moves(self, piece: ChessPiece):
        moves = []
        current_row, current_col = piece.row, piece.col

        if piece.type == PieceType.PAWN:
            direction = -1 if piece.color == PieceColor.WHITE else 1
            start_row = 6 if piece.color == PieceColor.WHITE else 1

            # Forward one square
            if not self.is_occupied(current_row + direction, current_col):
                moves.append((current_row + direction, current_col))

            # Forward two squares
            if current_row == start_row and not self.is_occupied(current_row + direction, current_col) and not self.is_occupied(current_row + 2 * direction, current_col):
                moves.append((current_row + 2 * direction, current_col))

            # Captures
            for dc in [-1, 1]:
                target_row, target_col = current_row + direction, current_col + dc
                if 0 <= target_row <= 7 and 0 <= target_col <= 7:
                    if self.is_occupied_by_enemy(target_row, target_col, piece.color):
                        moves.append((target_row, target_col))

            # En passant
            if self.en_passant_target_square:
                ep_row, ep_col = self.en_passant_target_square
                if ep_row == current_row + direction and abs(ep_col - current_col) == 1:
                    # Check if the attacking pawn is on its 5th rank
                    if (piece.color == PieceColor.WHITE and current_row == 3) or \
                       (piece.color == PieceColor.BLACK and current_row == 4):
                        moves.append(self.en_passant_target_square)

        elif piece.type == PieceType.ROOK:
            directions = [(-1, 0), (1, 0), (0, -1), (0, 1)] # Up, Down, Left, Right
            for dr, dc in directions:
                r, c = current_row + dr, current_col + dc
                while 0 <= r <= 7 and 0 <= c <= 7:
                    if self.is_occupied_by_ally(r, c, piece.color): break
                    moves.append((r, c))
                    if self.is_occupied_by_enemy(r, c, piece.color): break
                    r, c = r + dr, c + dc

        elif piece.type == PieceType.KNIGHT:
            knight_moves = [
                (-2, -1), (-2, 1), (-1, -2), (-1, 2),
                (1, -2), (1, 2), (2, -1), (2, 1)
            ]
            for dr, dc in knight_moves:
                r, c = current_row + dr, current_col + dc
                if 0 <= r <= 7 and 0 <= c <= 7 and not self.is_occupied_by_ally(r, c, piece.color):
                    moves.append((r, c))

        elif piece.type == PieceType.BISHOP:
            directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)] # Diagonals
            for dr, dc in directions:
                r, c = current_row + dr, current_col + dc
                while 0 <= r <= 7 and 0 <= c <= 7:
                    if self.is_occupied_by_ally(r, c, piece.color): break
                    moves.append((r, c))
                    if self.is_occupied_by_enemy(r, c, piece.color): break
                    r, c = r + dr, c + dc

        elif piece.type == PieceType.QUEEN:
            # Queen combines Rook and Bishop moves
            directions = [
                (-1, 0), (1, 0), (0, -1), (0, 1),  # Rook directions
                (-1, -1), (-1, 1), (1, -1), (1, 1)   # Bishop directions
            ]
            for dr, dc in directions:
                r, c = current_row + dr, current_col + dc
                while 0 <= r <= 7 and 0 <= c <= 7:
                    if self.is_occupied_by_ally(r, c, piece.color): break
                    moves.append((r, c))
                    if self.is_occupied_by_enemy(r, c, piece.color): break
                    r, c = r + dr, c + dc

        elif piece.type == PieceType.KING:
            king_moves = [
                (-1, -1), (-1, 0), (-1, 1),
                (0, -1), (0, 1),
                (1, -1), (1, 0), (1, 1)
            ]
            for dr, dc in king_moves:
                r, c = current_row + dr, current_col + dc
                if 0 <= r <= 7 and 0 <= c <= 7 and not self.is_occupied_by_ally(r, c, piece.color):
                    moves.append((r, c))

            # Castling
            if self.can_castle_king_side(piece.color):
                moves.append((current_row, 6)) # King moves to g1 or g8
            if self.can_castle_queen_side(piece.color):
                moves.append((current_row, 2)) # King moves to c1 or c8

        # Filter out moves that would leave the king in check
        legal_moves = []
        for target_row, target_col in moves:
            simulated_board = self.apply_move(piece, target_row, target_col, simulate=True)
            if not simulated_board.is_king_in_check(piece.color):
                legal_moves.append((target_row, target_col))

        return legal_moves

    def apply_move(self, piece: ChessPiece, target_row: int, target_col: int, simulate: bool = False):
        new_pieces = [p.__dict__.copy() for p in self.pieces] # Deep copy pieces
        new_pieces = [ChessPiece(**p) for p in new_pieces]

        # Create a new BoardState for simulation or actual move
        new_board = BoardState(new_pieces, self.current_turn, self.en_passant_target_square)

        # Find the piece on the new board to move
        piece_to_move = next((p for p in new_board.pieces if p == piece), None)
        if piece_to_move is None: # Should not happen if piece is from current board
            return new_board

        # Handle en passant capture
        if piece_to_move.type == PieceType.PAWN and target_col != piece_to_move.col and new_board.get_piece_at(target_row, target_col) is None:
            # This is an en passant capture
            captured_pawn_row = piece_to_move.row # The captured pawn is on the same row as the attacking pawn, but in the target_col
            captured_pawn = new_board.get_piece_at(captured_pawn_row, target_col)
            if captured_pawn: # Ensure captured_pawn exists
                new_board.pieces.remove(captured_pawn)
        else:
            captured_piece = new_board.get_piece_at(target_row, target_col)
            if captured_piece:
                new_board.pieces.remove(captured_piece)

        # Update piece position and has_moved
        piece_to_move.row = target_row
        piece_to_move.col = target_col
        piece_to_move.has_moved = True

        # Handle castling: move the rook
        if piece_to_move.type == PieceType.KING and abs(piece.col - target_col) == 2:
            # King-side castling
            if target_col == 6:
                rook = next((p for p in new_board.pieces if p.type == PieceType.ROOK and p.color == piece_to_move.color and p.col == 7), None)
                if rook: # Ensure rook exists
                    rook.col = 5
                    rook.has_moved = True
            # Queen-side castling
            elif target_col == 2:
                rook = next((p for p in new_board.pieces if p.type == PieceType.ROOK and p.color == piece_to_move.color and p.col == 0), None)
                if rook: # Ensure rook exists
                    rook.col = 3
                    rook.has_moved = True

        # Handle pawn promotion
        if piece_to_move.type == PieceType.PAWN and \
           ((piece_to_move.color == PieceColor.WHITE and piece_to_move.row == 0) or \
            (piece_to_move.color == PieceColor.BLACK and piece_to_move.row == 7)):
            piece_to_move.type = PieceType.QUEEN # Automatic promotion to Queen

        # Set new en passant target square
        new_board.en_passant_target_square = None # Clear previous target
        if piece.type == PieceType.PAWN and abs(piece.row - target_row) == 2:
            new_board.en_passant_target_square = (piece.row + (1 if piece.color == PieceColor.BLACK else -1), piece.col)

        if not simulate:
            new_board.current_turn = PieceColor.BLACK if self.current_turn == PieceColor.WHITE else PieceColor.WHITE

        return new_board

    def has_any_legal_moves(self, color: PieceColor) -> bool:
        total_moves = 0
        for piece in self.pieces:
            if piece.color == color:
                moves = self.calculate_possible_moves(piece)
                total_moves += len(moves)
                if moves:  # If any legal moves exist for this piece
                    return True
        print(f"Total legal moves for {color}: {total_moves}")  # Debug output
        return False

    def is_checkmate(self, color: PieceColor) -> bool:
        return self.is_king_in_check(color) and not self.has_any_legal_moves(color)

    def is_stalemate(self, color: PieceColor) -> bool:
        # Safety check - at least one piece of each color must exist
        has_white_pieces = any(p.color == PieceColor.WHITE for p in self.pieces)
        has_black_pieces = any(p.color == PieceColor.BLACK for p in self.pieces)
        if not (has_white_pieces and has_black_pieces):
            return False

        no_check = not self.is_king_in_check(color)
        no_moves = not self.has_any_legal_moves(color)
        return no_check and no_moves
