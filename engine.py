# Responsible for storing current game state, determining valid moves
class GameState():
    def __init__(self):
        self.starting_board()
        self.current_turn = "w"
        self.check = False
        self.movelog = {}

    # 8x8 2D list represents the board
    # First character represents Black/White
    # Second character represents the piece type R, N, B, K, P
    # -- Represents empty space
    def starting_board(self):
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"],
        ]
    
    # Move the piece - original square is now blank, new square is now filled with the old piece.
    # Piece at the new square is automatically overwritten if it exists.
    def move(self, last_square, selected_square, last_piece):
        print(last_square[0])
        print(last_square[1])
        self.board[last_square[0]][last_square[1]] = "--"
        #self.board[last_square[0]], [last_square[1]] = "--"
        self.board[selected_square[0]][selected_square[1]] = last_piece
        
    
    def change_turn(self):
        if self.current_turn == "w":
            self.current_turn = "b"
        else:
            self.current_turn = "w"
    def generate_valid_moves(self, square_x, square_y, selected_piece, selected_piece_colour):
        selected_piece_type = selected_piece[1]
        self.valid_moves = []
        # Knight
        if selected_piece_type == "N":
            self.validate_knight(square_x, square_y, selected_piece_colour)
        return self.valid_moves

    def validate_knight(self, square_x, square_y, selected_piece_colour):
        # Iterate through a set of coordinates to check if every possible move is valid
        knight_moveset = ((-2, -1), (-2, 1), (-1, -2), (1, -2), (1, 2), (2, -1), (2, 1))
        for move in knight_moveset:
            move_x = square_x + move[0]
            move_y = square_y + move[1]
            # Skip check if position is off the board
            if 0 <= move_y < 8 and 0 <= move_x < 8:
                piece = self.board[move_x][move_y]
                piece_colour = piece[0]
                # Move is valid if the colour is different
                if piece_colour != selected_piece_colour:
                    self.valid_moves.append((move_x, move_y))
                    print(self.valid_moves)
