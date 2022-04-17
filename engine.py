# Responsible for storing current game state, determining valid moves
from re import A, I


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
    def generate_valid_moves(self, row, col, selected_piece, selected_piece_colour):
        selected_piece_type = selected_piece[1]
        self.valid_moves = []

        # Pawn
        if selected_piece_type == "P":
            # White pawn
            if selected_piece_colour == "w":
                self.validate_pawn_move(row, col, -1, +1, 6, selected_piece_colour)
            # Black pawn
            else:
                self.validate_pawn_move(row, col, +1, -1, 1, selected_piece_colour)
        # Knight
        if selected_piece_type == "N":
            self.validate_knight(row, col, selected_piece_colour)     
        # Rook
        if selected_piece_type == "R":
            directions = ((-1, 0), (0, -1), (1, 0), (0, 1))
            self.check_line(directions, 7, row, col, selected_piece_colour)
        # Queen
        if selected_piece_type == "Q":
            directions = ((-1, 0), (0, -1), (1, 0), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1))
            self.check_line(directions, 7, row, col, selected_piece_colour)
        # Bishop
        if selected_piece_type == "B":
            directions = ((-1, -1), (-1, 1), (1, -1), (1, 1))
            self.check_line(directions, 7, row, col, selected_piece_colour)
        # King
        if  selected_piece_type == "K":
            directions = ((-1, 0), (0, -1), (1, 0), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1))
            self.check_line(directions, 1, row, col, selected_piece_colour)
        
        return self.valid_moves

    def validate_pawn_take(self, col, row, selected_piece_colour):
        # Skip check if diaganal is off the board
        if col < 0 or row < 0 or col > 7 or row > 7:
            return
        else:
            # Simulates the move and then checks if the move would result in check for the moving player's king.
            # If it does, move is not valid
            #if not self.simulate_move(row, col):
                # Add to valid moves there is a piece on the diaganal square and the piece is a different colour
                piece = self.board[col][row]
                piece_colour = piece[0]
                if piece != "--" and piece_colour != selected_piece_colour:
                    self.valid_moves.append((col, row))

    def validate_pawn_move(self, row, col, a, b, starting_row, selected_piece_colour):
        # Check for pieces on diagnal to take
        self.validate_pawn_take(row + a, col + a, selected_piece_colour)
        self.validate_pawn_take(row + a, col + b, selected_piece_colour)

        # Check if pawn is on starting position, if so allow double move
        if row == starting_row:
            x = 3
        else:
            x = 2

        for i in range(1, x):
            new_row = row + (i * a)
            print("Original Coordinates: " + str(row) + "," + str(col))
            print("New Coordinates: " + str(new_row) + "," + str(col))
            piece = self.board[new_row][col]
            # Simulates the move and then checks if the move would result in check for the moving player's king.
            # If it does, move is not valid - skip to next move
            #if self.simulate_move(self.old_row, col):
            #    continue

            # If there is a piece in the way, we can't move there - return before added to valid moves
            if piece != "--":
                return
            else:
                self.valid_moves.append((new_row, col))

    def validate_knight(self, row, col, selected_piece_colour):
        # Iterate through a set of coordinates to check if every possible move is valid
        knight_moveset = ((-2, -1), (-2, 1), (-1, -2), (1, -2), (1, 2), (2, -1), (2, 1), (-1, 2))
        for move in knight_moveset:
            new_row = row + move[0]
            new_col = col + move[1]
            # Skip check if position is off the board
            if 0 <= new_col < 8 and 0 <= new_row < 8:
                piece = self.board[new_row][new_col]
                piece_colour = piece[0]
                # Move is valid if the colour is different
                if piece_colour != selected_piece_colour:
                    self.valid_moves.append((new_row, new_col))
    
    def check_line(self, directions, length, row, col, selected_piece_colour):
        for direction in directions:
            a = direction[0]    
            b = direction[1]
            for i in range(length):
                new_col = col + b
                new_row = row + a
                # End loop if square is out of bounds
                if new_col >= 8 or new_col <= -1 or new_row >= 8 or new_row <= -1:
                    break
                # Simulates the move and then checks if the move would result in check for the moving player's king.
                # If it does, move is not valid - skip to next move
                #if self.simulate_move(new_row, new_col):
                #    continue

                piece = self.board[new_row][new_col]
                piece_colour = piece[0]
                # If the piece is the same colour, we stop before it is added to the list
                if piece_colour == selected_piece_colour:
                    break
                self.valid_moves.append((new_row, new_col))
                # If the piece is another colour, we stop after it is added to the list
                if piece != "--":
                    break
                # Iterate the loop by moving in the direction
                a += direction[0]
                b += direction[1]