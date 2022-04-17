# Responsible for storing current game state, determining valid moves
from re import I


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

        # Pawn
        if selected_piece_type == "P":
            # White pawn
            if selected_piece_colour == "w":
                self.validate_pawn_move(square_x, square_y, -1, +1, 6, selected_piece_colour)
            # Black pawn
            else:
                self.validate_pawn_move(square_x, square_y, +1, -1, 1, selected_piece_colour)
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

    def validate_pawn_take(self, square_y, square_x, selected_piece_colour):
        # Skip check if diaganal is off the board
        if square_y < 0 or square_x < 0 or square_y > 7 or square_x > 7:
            return
        else:
            # Simulates the move and then checks if the move would result in check for the moving player's king.
            # If it does, move is not valid
            #if not self.simulate_move(square_x, square_y):
                # Add to valid moves there is a piece on the diaganal square and the piece is a different colour
                piece = self.board[square_y][square_x]
                piece_colour = piece[0]
                if piece != "--" and piece_colour != selected_piece_colour:
                    self.valid_moves.append((square_y, square_x))

    def validate_pawn_move(self, square_x, square_y, a, b, starting_row, selected_piece_colour):
        # Check for pieces on diagnal to take
        self.validate_pawn_take(square_x + a, square_y + a, selected_piece_colour)
        self.validate_pawn_take(square_x + a, square_y + b, selected_piece_colour)

        # Check if pawn is on starting position, if so allow double move
        if square_x == starting_row:
            x = 3
        else:
            x = 2

        for i in range(1, x):
            new_square_x = square_x + (i * a)
            print("Original Coordinates: " + str(square_x) + "," + str(square_y))
            print("New Coordinates: " + str(new_square_x) + "," + str(square_y))
            piece = self.board[new_square_x][square_y]
            # Simulates the move and then checks if the move would result in check for the moving player's king.
            # If it does, move is not valid - skip to next move
            #if self.simulate_move(self.old_square_x, square_y):
            #    continue

            # If there is a piece in the way, we can't move there - return before added to valid moves
            if piece != "--":
                return
            else:
                self.valid_moves.append((new_square_x, square_y))

    def validate_w_pawn_move(self):

        # Check for pieces on diagnal to take
        self.validate_pawn_take(self.old_posY - 1, self.old_posX - 1)
        self.validate_pawn_take(self.old_posY - 1, self.old_posX + 1)

        # Check if pawn is on starting position, if so allow double move
        if self.old_posY == 6:
            x = 2
        else:
            x = 1
        for i in range(x):
            posY = self.old_posY - (i + 1)
            piece = self.board[posY][self.old_posX]
            # Simulates the move and then checks if the move would result in check for the moving player's king.
            # If it does, move is not valid - skip to next move
            if self.simulate_move(self.old_posX, posY):
                continue
            # If there is a piece in the way, we can't move there - return before added to valid moves
            if piece != "--":
                return
            else:
                self.valid_list.append((posY, self.old_posX))

    def validate_b_pawn_move(self):
        # Check for pieces on diagnal to take
        self.validate_pawn_take(self.old_posY + 1, self.old_posX + 1)
        self.validate_pawn_take(self.old_posY + 1, self.old_posX - 1)

        # Check if pawn is on starting position, if so allow double move
        if self.old_posY == 1:
            x = 2
        else:
            x = 1
        for i in range(x):
            posY = self.old_posY + (i + 1)
            piece = self.board[posY][self.old_posX]
            # Simulates the move and then checks if the move would result in check for the moving player's king.
            # If it does, move is not valid - skip to next move
            if self.simulate_move(self.old_posX, posY):
                continue
            # If there is a piece in the way, we can't move there - return before added to valid moves
            if piece != "--":
                return
            else:
                self.valid_list.append((posY, self.old_posX))

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