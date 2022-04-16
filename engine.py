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
        # Rook
        if selected_piece_type == "R":
            directions = ((-1, 0), (0, -1), (1, 0), (0, 1))
            self.check_line(directions, 7, square_x, square_y, selected_piece_colour)
        # Queen
        if selected_piece_type == "Q":
            directions = ((-1, 0), (0, -1), (1, 0), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1))
            self.check_line(directions, 7, square_x, square_y, selected_piece_colour)
        # Bishop
        if selected_piece_type == "B":
            directions = ((-1, -1), (-1, 1), (1, -1), (1, 1))
            self.check_line(directions, 7, square_x, square_y, selected_piece_colour)
        # King
        if  selected_piece_type == "K":
            directions = ((-1, 0), (0, -1), (1, 0), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1))
            self.check_line(directions, 1, square_x, square_y, selected_piece_colour)
        
        return self.valid_moves

    def validate_knight(self, square_x, square_y, selected_piece_colour):
        # Iterate through a set of coordinates to check if every possible move is valid
        knight_moveset = ((-2, -1), (-2, 1), (-1, -2), (1, -2), (1, 2), (2, -1), (2, 1), (-1, 2))
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
    
    def check_line(self, directions, length, square_x, square_y, selected_piece_colour):
        for direction in directions:
            x = direction[0]    
            y = direction[1]
            for i in range(length):
                new_y = square_y + y
                new_x = square_x + x
                # End loop if square is out of bounds
                if new_y >= 8 or new_y <= -1 or new_x >= 8 or new_x <= -1:
                    break
                # Simulates the move and then checks if the move would result in check for the moving player's king.
                # If it does, move is not valid - skip to next move
                #if self.simulate_move(new_x, new_y):
                #    continue

                piece = self.board[new_x][new_y]
                piece_colour = piece[0]
                # If the piece is the same colour, we stop before it is added to the list
                if piece_colour == selected_piece_colour:
                    break
                self.valid_moves.append((new_x, new_y))
                # If the piece is another colour, we stop after it is added to the list
                if piece != "--":
                    break
                # Iterate the loop by moving in the direction
                x += direction[0]
                y += direction[1]