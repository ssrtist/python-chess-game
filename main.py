import pygame
import time # Import time for delays
from chess_logic import BoardState, PieceColor, PieceType, ChessPiece
from chess_ai import ChessAI # Import ChessAI

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Python Chess")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_SQUARE = (238, 238, 210)
DARK_SQUARE = (118, 150, 86)
PIECE_WHITE = (240, 240, 240)
PIECE_BLACK = (50, 50, 50)
HIGHLIGHT_COLOR = (255, 255, 0, 100) # Yellow with transparency
MESSAGE_COLOR = (255, 0, 0) # Red for messages

# Board dimensions
BOARD_SIZE = 8
SQUARE_SIZE = SCREEN_WIDTH // BOARD_SIZE

# Fonts
FONT = pygame.font.Font(None, 74) # Default font, size 74

def draw_board(screen):
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            color = LIGHT_SQUARE if (row + col) % 2 == 0 else DARK_SQUARE
            pygame.draw.rect(screen, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

def draw_pieces(screen, board_state):
    for piece in board_state.pieces:
        center_x = piece.col * SQUARE_SIZE + SQUARE_SIZE // 2
        center_y = piece.row * SQUARE_SIZE + SQUARE_SIZE // 2
        piece_color = PIECE_WHITE if piece.color == PieceColor.WHITE else PIECE_BLACK
        outline_color = BLACK if piece.color == PieceColor.WHITE else WHITE

        # Base for all pieces (except pawn)
        if piece.type != PieceType.PAWN:
            pygame.draw.ellipse(screen, piece_color, (center_x - SQUARE_SIZE // 4, center_y + SQUARE_SIZE // 4 - 10, SQUARE_SIZE // 2, 20))
            pygame.draw.ellipse(screen, outline_color, (center_x - SQUARE_SIZE // 4, center_y + SQUARE_SIZE // 4 - 10, SQUARE_SIZE // 2, 20), 2)


        # Draw stylized pieces
        if piece.type == PieceType.PAWN:
            # Base
            pygame.draw.ellipse(screen, piece_color, (center_x - SQUARE_SIZE // 6, center_y + SQUARE_SIZE // 4 - 5, SQUARE_SIZE // 3, 10))
            pygame.draw.ellipse(screen, outline_color, (center_x - SQUARE_SIZE // 6, center_y + SQUARE_SIZE // 4 - 5, SQUARE_SIZE // 3, 10), 2)
            # Body
            pygame.draw.rect(screen, piece_color, (center_x - SQUARE_SIZE // 8, center_y - 5, SQUARE_SIZE // 4, SQUARE_SIZE // 3))
            pygame.draw.rect(screen, outline_color, (center_x - SQUARE_SIZE // 8, center_y - 5, SQUARE_SIZE // 4, SQUARE_SIZE // 3), 2)
            # Head
            pygame.draw.circle(screen, piece_color, (center_x, center_y - 15), SQUARE_SIZE // 8)
            pygame.draw.circle(screen, outline_color, (center_x, center_y - 15), SQUARE_SIZE // 8, 2)

        elif piece.type == PieceType.ROOK:
            # Body
            pygame.draw.rect(screen, piece_color, (center_x - SQUARE_SIZE // 6, center_y - SQUARE_SIZE // 4, SQUARE_SIZE // 3, SQUARE_SIZE // 2))
            pygame.draw.rect(screen, outline_color, (center_x - SQUARE_SIZE // 6, center_y - SQUARE_SIZE // 4, SQUARE_SIZE // 3, SQUARE_SIZE // 2), 2)
            # Top crenellations
            pygame.draw.rect(screen, piece_color, (center_x - SQUARE_SIZE // 4, center_y - SQUARE_SIZE // 4 - 5, SQUARE_SIZE // 2, 10))
            pygame.draw.rect(screen, outline_color, (center_x - SQUARE_SIZE // 4, center_y - SQUARE_SIZE // 4 - 5, SQUARE_SIZE // 2, 10), 2)
            pygame.draw.rect(screen, piece_color, (center_x - SQUARE_SIZE // 4, center_y - SQUARE_SIZE // 4 - 15, SQUARE_SIZE // 8, 10))
            pygame.draw.rect(screen, outline_color, (center_x - SQUARE_SIZE // 4, center_y - SQUARE_SIZE // 4 - 15, SQUARE_SIZE // 8, 10), 2)
            pygame.draw.rect(screen, piece_color, (center_x + SQUARE_SIZE // 8, center_y - SQUARE_SIZE // 4 - 15, SQUARE_SIZE // 8, 10))
            pygame.draw.rect(screen, outline_color, (center_x + SQUARE_SIZE // 8, center_y - SQUARE_SIZE // 4 - 15, SQUARE_SIZE // 8, 10), 2)

        elif piece.type == PieceType.KNIGHT:
            # Body
            pygame.draw.polygon(screen, piece_color, [
                (center_x - SQUARE_SIZE // 6, center_y + SQUARE_SIZE // 4),
                (center_x + SQUARE_SIZE // 6, center_y + SQUARE_SIZE // 4),
                (center_x + SQUARE_SIZE // 4, center_y - SQUARE_SIZE // 8),
                (center_x, center_y - SQUARE_SIZE // 4),
                (center_x - SQUARE_SIZE // 4, center_y - SQUARE_SIZE // 8)
            ])
            pygame.draw.polygon(screen, outline_color, [
                (center_x - SQUARE_SIZE // 6, center_y + SQUARE_SIZE // 4),
                (center_x + SQUARE_SIZE // 6, center_y + SQUARE_SIZE // 4),
                (center_x + SQUARE_SIZE // 4, center_y - SQUARE_SIZE // 8),
                (center_x, center_y - SQUARE_SIZE // 4),
                (center_x - SQUARE_SIZE // 4, center_y - SQUARE_SIZE // 8)
            ], 2)
            # Head/Mane
            pygame.draw.circle(screen, piece_color, (center_x + SQUARE_SIZE // 8, center_y - SQUARE_SIZE // 6), SQUARE_SIZE // 10)
            pygame.draw.circle(screen, outline_color, (center_x + SQUARE_SIZE // 8, center_y - SQUARE_SIZE // 6), SQUARE_SIZE // 10, 2)
            pygame.draw.line(screen, piece_color, (center_x - SQUARE_SIZE // 8, center_y - SQUARE_SIZE // 4), (center_x + SQUARE_SIZE // 8, center_y - SQUARE_SIZE // 4), 5)
            pygame.draw.line(screen, outline_color, (center_x - SQUARE_SIZE // 8, center_y - SQUARE_SIZE // 4), (center_x + SQUARE_SIZE // 8, center_y - SQUARE_SIZE // 4), 2)


        elif piece.type == PieceType.BISHOP:
            # Body
            pygame.draw.polygon(screen, piece_color, [
                (center_x, center_y - SQUARE_SIZE // 4),
                (center_x - SQUARE_SIZE // 6, center_y + SQUARE_SIZE // 4),
                (center_x + SQUARE_SIZE // 6, center_y + SQUARE_SIZE // 4)
            ])
            pygame.draw.polygon(screen, outline_color, [
                (center_x, center_y - SQUARE_SIZE // 4),
                (center_x - SQUARE_SIZE // 6, center_y + SQUARE_SIZE // 4),
                (center_x + SQUARE_SIZE // 6, center_y + SQUARE_SIZE // 4)
            ], 2)
            # Head
            pygame.draw.circle(screen, piece_color, (center_x, center_y - SQUARE_SIZE // 4 - 5), SQUARE_SIZE // 10)
            pygame.draw.circle(screen, outline_color, (center_x, center_y - SQUARE_SIZE // 4 - 5), SQUARE_SIZE // 10, 2)
            # Mitre cut
            pygame.draw.line(screen, outline_color, (center_x - 5, center_y - SQUARE_SIZE // 4 - 10), (center_x + 5, center_y - SQUARE_SIZE // 4 - 10), 2)


        elif piece.type == PieceType.QUEEN:
            # Body
            pygame.draw.polygon(screen, piece_color, [
                (center_x, center_y - SQUARE_SIZE // 4),
                (center_x - SQUARE_SIZE // 4, center_y + SQUARE_SIZE // 4),
                (center_x + SQUARE_SIZE // 4, center_y + SQUARE_SIZE // 4)
            ])
            pygame.draw.polygon(screen, outline_color, [
                (center_x, center_y - SQUARE_SIZE // 4),
                (center_x - SQUARE_SIZE // 4, center_y + SQUARE_SIZE // 4),
                (center_x + SQUARE_SIZE // 4, center_y + SQUARE_SIZE // 4)
            ], 2)
            # Crown
            pygame.draw.circle(screen, piece_color, (center_x, center_y - SQUARE_SIZE // 4 - 10), SQUARE_SIZE // 10)
            pygame.draw.circle(screen, outline_color, (center_x, center_y - SQUARE_SIZE // 4 - 10), SQUARE_SIZE // 10, 2)
            pygame.draw.line(screen, piece_color, (center_x - SQUARE_SIZE // 8, center_y - SQUARE_SIZE // 4 - 5), (center_x + SQUARE_SIZE // 8, center_y - SQUARE_SIZE // 4 - 5), 5)
            pygame.draw.line(screen, outline_color, (center_x - SQUARE_SIZE // 8, center_y - SQUARE_SIZE // 4 - 5), (center_x + SQUARE_SIZE // 8, center_y - SQUARE_SIZE // 4 - 5), 2)


        elif piece.type == PieceType.KING:
            # Body
            pygame.draw.rect(screen, piece_color, (center_x - SQUARE_SIZE // 6, center_y, SQUARE_SIZE // 3, SQUARE_SIZE // 4))
            pygame.draw.rect(screen, outline_color, (center_x - SQUARE_SIZE // 6, center_y, SQUARE_SIZE // 3, SQUARE_SIZE // 4), 2)
            # Head
            pygame.draw.circle(screen, piece_color, (center_x, center_y - SQUARE_SIZE // 4), SQUARE_SIZE // 7)
            pygame.draw.circle(screen, outline_color, (center_x, center_y - SQUARE_SIZE // 4), SQUARE_SIZE // 7, 2)
            # Cross
            pygame.draw.line(screen, piece_color, (center_x - SQUARE_SIZE // 8, center_y - SQUARE_SIZE // 4), (center_x + SQUARE_SIZE // 8, center_y - SQUARE_SIZE // 4), 5)
            pygame.draw.line(screen, outline_color, (center_x - SQUARE_SIZE // 8, center_y - SQUARE_SIZE // 4), (center_x + SQUARE_SIZE // 8, center_y - SQUARE_SIZE // 4), 2)
            pygame.draw.line(screen, piece_color, (center_x, center_y - SQUARE_SIZE // 4 - SQUARE_SIZE // 8), (center_x, center_y - SQUARE_SIZE // 4 + SQUARE_SIZE // 8), 5)
            pygame.draw.line(screen, outline_color, (center_x, center_y - SQUARE_SIZE // 4 - SQUARE_SIZE // 8), (center_x, center_y - SQUARE_SIZE // 4 + SQUARE_SIZE // 8), 2)

def draw_highlights(screen, selected_piece, possible_moves):
    if selected_piece:
        # Highlight selected piece
        s = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
        s.fill(HIGHLIGHT_COLOR)
        screen.blit(s, (selected_piece.col * SQUARE_SIZE, selected_piece.row * SQUARE_SIZE))

        # Highlight possible moves
        for move_row, move_col in possible_moves:
            s = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
            s.fill(HIGHLIGHT_COLOR)
            screen.blit(s, (move_col * SQUARE_SIZE, move_row * SQUARE_SIZE))

def display_message(screen, message):
    text_surface = FONT.render(message, True, MESSAGE_COLOR)
    text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.blit(text_surface, text_rect)


# Create initial board state
board_state = BoardState()
chess_ai = ChessAI(depth=3) # Initialize AI with depth 3 for "very hard"
selected_piece = None
possible_moves = []
game_over = False
game_result = ""

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            if board_state.current_turn == PieceColor.WHITE: # Only allow player input if it's White's turn
                mouse_x, mouse_y = event.pos
                clicked_col = mouse_x // SQUARE_SIZE
                clicked_row = mouse_y // SQUARE_SIZE

                if selected_piece is None:
                    # Try to select a piece
                    piece = board_state.get_piece_at(clicked_row, clicked_col)
                    if piece and piece.color == board_state.current_turn:
                        selected_piece = piece
                        possible_moves = board_state.calculate_possible_moves(selected_piece)
                else:
                    # A piece is already selected, try to move it or change selection
                    if (clicked_row, clicked_col) in possible_moves:
                        # Valid move
                        board_state = board_state.apply_move(selected_piece, clicked_row, clicked_col)
                        selected_piece = None
                        possible_moves = []
                    elif board_state.get_piece_at(clicked_row, clicked_col) == selected_piece:
                        # Clicked on the same piece, deselect
                        selected_piece = None
                        possible_moves = []
                    else:
                        # Clicked elsewhere, deselect and try to select new piece
                        selected_piece = None
                        possible_moves = []
                        piece = board_state.get_piece_at(clicked_row, clicked_col)
                        if piece and piece.color == board_state.current_turn:
                            selected_piece = piece
                            possible_moves = board_state.calculate_possible_moves(selected_piece)

    # AI's turn
    if not game_over and board_state.current_turn == PieceColor.BLACK: # Assuming AI plays as Black
        time.sleep(0.5) # Small delay for AI to "think"
        ai_move = chess_ai.find_best_move(board_state, PieceColor.BLACK)
        if ai_move:
            piece_to_move, target_square = ai_move
            # Find the actual piece object from the current board_state
            # This is important because the piece_to_move in ai_move might be an old instance
            actual_piece = board_state.get_piece_at(piece_to_move.row, piece_to_move.col)
            if actual_piece and actual_piece == piece_to_move: # Ensure it's the same piece
                board_state = board_state.apply_move(actual_piece, target_square[0], target_square[1])
        else:
            # AI has no legal moves
            if board_state.is_king_in_check(PieceColor.BLACK):
                game_result = "Checkmate! White Wins!"
            else:
                game_result = "Stalemate!"
            game_over = True


    # Check for game over conditions after each move
    if not game_over:
        if board_state.is_checkmate(board_state.current_turn):
            game_result = f"Checkmate! {'White' if board_state.current_turn == PieceColor.BLACK else 'Black'} Wins!"
            game_over = True
        elif board_state.is_stalemate(board_state.current_turn):
            game_result = "Stalemate!"
            game_over = True


    # Draw the board
    draw_board(SCREEN)
    # Draw highlights
    draw_highlights(SCREEN, selected_piece, possible_moves)
    # Draw the pieces
    draw_pieces(SCREEN, board_state)

    # Display game over message if applicable
    if game_over:
        display_message(SCREEN, game_result)

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()