#!/usr/bin/env python3
# Chess Game Implementation

import tkinter as tk
from tkinter import messagebox
import os

class ChessGame:
    def __init__(self, master=None):
        # If no master window is provided, create our own
        self.standalone = master is None
        if self.standalone:
            self.master = tk.Tk()
            self.master.title("Chess")
            self.master.geometry("700x700")
        else:
            self.master = master
        
        # Game constants
        self.BOARD_SIZE = 8
        self.SQUARE_SIZE = 70
        self.BOARD_WIDTH = self.BOARD_SIZE * self.SQUARE_SIZE
        self.BOARD_HEIGHT = self.BOARD_SIZE * self.SQUARE_SIZE
        self.COLORS = {
            "light_square": "#f0d9b5",
            "dark_square": "#b58863",
            "selected": "#aad751",
            "possible_move": "#cdd26a",
            "check": "#f44336"
        }
        
        # Game state
        self.board = self.create_initial_board()
        self.selected_piece = None
        self.current_player = "white"
        self.white_king_pos = (7, 4)
        self.black_king_pos = (0, 4)
        self.game_over = False
        
        # Create UI elements
        self.create_widgets()
        
        # Initialize piece images
        self.piece_images = {}
        self.load_piece_images()
    
    def create_widgets(self):
        # Create a frame for the game
        self.game_frame = tk.Frame(self.master)
        self.game_frame.pack(padx=10, pady=10)
        
        # Create canvas for drawing the board
        self.canvas = tk.Canvas(
            self.game_frame, 
            width=self.BOARD_WIDTH, 
            height=self.BOARD_HEIGHT
        )
        self.canvas.pack()
        
        # Bind mouse click event
        self.canvas.bind("<Button-1>", self.on_square_click)
        
        # Create status label
        self.status_var = tk.StringVar()
        self.status_var.set("White's turn")
        self.status_label = tk.Label(
            self.master,
            textvariable=self.status_var,
            font=("Helvetica", 16),
            bg=self.master["bg"]
        )
        self.status_label.pack(pady=5)
        
        # Create buttons frame
        self.buttons_frame = tk.Frame(self.master, bg=self.master["bg"])
        self.buttons_frame.pack(pady=5)
        
        # Create restart button
        self.restart_button = tk.Button(
            self.buttons_frame,
            text="New Game",
            command=self.restart_game,
            bg="#3498db",
            fg="white",
            font=("Helvetica", 10),
            relief=tk.FLAT,
            padx=20
        )
        self.restart_button.pack(side=tk.LEFT, padx=5)
        
        # Create exit button
        self.exit_button = tk.Button(
            self.buttons_frame,
            text="Exit",
            command=self.exit_game,
            bg="#e74c3c",
            fg="white",
            font=("Helvetica", 10),
            relief=tk.FLAT,
            padx=20
        )
        self.exit_button.pack(side=tk.LEFT, padx=5)
        
        # Draw the initial board
        self.draw_board()
        self.draw_pieces()
    
    def create_initial_board(self):
        """Create the initial chess board setup"""
        # Initialize empty board
        board = [[None for _ in range(self.BOARD_SIZE)] for _ in range(self.BOARD_SIZE)]
        
        # Set up pawns
        for col in range(self.BOARD_SIZE):
            board[1][col] = {"type": "pawn", "color": "black"}
            board[6][col] = {"type": "pawn", "color": "white"}
        
        # Set up other pieces
        back_row = ["rook", "knight", "bishop", "queen", "king", "bishop", "knight", "rook"]
        for col in range(self.BOARD_SIZE):
            board[0][col] = {"type": back_row[col], "color": "black"}
            board[7][col] = {"type": back_row[col], "color": "white"}
        
        return board
    
    def load_piece_images(self):
        """Load chess piece images"""
        # We're not actually loading images - just using Unicode symbols
        # This method is kept for compatibility
        pass
    
    def draw_board(self):
        """Draw the chess board"""
        self.canvas.delete("square")
        for row in range(self.BOARD_SIZE):
            for col in range(self.BOARD_SIZE):
                # Determine square color
                color = self.COLORS["light_square"] if (row + col) % 2 == 0 else self.COLORS["dark_square"]
                
                # Draw square
                self.canvas.create_rectangle(
                    col * self.SQUARE_SIZE, row * self.SQUARE_SIZE,
                    (col + 1) * self.SQUARE_SIZE, (row + 1) * self.SQUARE_SIZE,
                    fill=color, outline="",
                    tags="square"
                )
                
                # Add coordinate labels (optional)
                if col == 0:
                    self.canvas.create_text(
                        5, row * self.SQUARE_SIZE + 10,
                        text=str(8 - row),
                        fill="#333" if color == self.COLORS["light_square"] else "#fff",
                        font=("Helvetica", 10),
                        anchor=tk.W
                    )
                
                if row == 7:
                    self.canvas.create_text(
                        col * self.SQUARE_SIZE + self.SQUARE_SIZE - 10,
                        self.BOARD_HEIGHT - 5,
                        text=chr(97 + col),
                        fill="#333" if color == self.COLORS["light_square"] else "#fff",
                        font=("Helvetica", 10),
                        anchor=tk.SE
                    )
    
    def draw_pieces(self):
        """Draw the chess pieces on the board"""
        self.canvas.delete("piece")
        for row in range(self.BOARD_SIZE):
            for col in range(self.BOARD_SIZE):
                piece = self.board[row][col]
                if piece:
                    self.draw_piece(row, col, piece)
    
    def draw_piece(self, row, col, piece):
        """Draw a single chess piece"""
        x = col * self.SQUARE_SIZE + self.SQUARE_SIZE // 2
        y = row * self.SQUARE_SIZE + self.SQUARE_SIZE // 2
        
        piece_key = f"{piece['color']}_{piece['type']}"
        
        # Always use text representation for pieces
        symbol = self.get_piece_symbol(piece)
        color = "white" if piece["color"] == "white" else "black"
        
        self.canvas.create_text(
            x, y,
            text=symbol,
            fill=color,
            font=("Helvetica", 36, "bold"),
            tags=("piece", f"piece_{row}_{col}")
        )
    
    def get_piece_symbol(self, piece):
        """Get Unicode symbol for a chess piece"""
        symbols = {
            "white_king": "♔", "white_queen": "♕", "white_rook": "♖",
            "white_bishop": "♗", "white_knight": "♘", "white_pawn": "♙",
            "black_king": "♚", "black_queen": "♛", "black_rook": "♜",
            "black_bishop": "♝", "black_knight": "♞", "black_pawn": "♟"
        }
        piece_key = f"{piece['color']}_{piece['type']}"
        return symbols.get(piece_key, "?")
    
    def highlight_square(self, row, col, color):
        """Highlight a square on the board"""
        self.canvas.create_rectangle(
            col * self.SQUARE_SIZE, row * self.SQUARE_SIZE,
            (col + 1) * self.SQUARE_SIZE, (row + 1) * self.SQUARE_SIZE,
            fill=color, outline="",
            tags="highlight"
        )
    
    def on_square_click(self, event):
        """Handle click on a chess square"""
        if self.game_over:
            return
            
        # Convert click coordinates to board position
        col = event.x // self.SQUARE_SIZE
        row = event.y // self.SQUARE_SIZE
        
        # Check if position is valid
        if not (0 <= row < self.BOARD_SIZE and 0 <= col < self.BOARD_SIZE):
            return
        
        # If a piece is already selected
        if self.selected_piece:
            selected_row, selected_col = self.selected_piece
            
            # If clicking on the same piece, deselect it
            if row == selected_row and col == selected_col:
                self.selected_piece = None
                self.draw_board()
                self.draw_pieces()
                return
            
            # If clicking on a valid move, make the move
            if self.is_valid_move(selected_row, selected_col, row, col):
                self.make_move(selected_row, selected_col, row, col)
                self.selected_piece = None
                
                # Check for game over conditions
                if self.is_checkmate():
                    self.game_over = True
                    winner = "White" if self.current_player == "black" else "Black"
                    self.status_var.set(f"Checkmate! {winner} wins")
                    messagebox.showinfo("Game Over", f"Checkmate! {winner} wins")
                elif self.is_stalemate():
                    self.game_over = True
                    self.status_var.set("Stalemate! The game is a draw")
                    messagebox.showinfo("Game Over", "Stalemate! The game is a draw")
                else:
                    # Switch player
                    self.current_player = "black" if self.current_player == "white" else "white"
                    self.status_var.set(f"{self.current_player.capitalize()}'s turn")
                    
                    # Check for check
                    if self.is_in_check(self.current_player):
                        self.status_var.set(f"{self.current_player.capitalize()} is in check!")
                
                # Redraw the board
                self.draw_board()
                self.draw_pieces()
                return
        
        # If no piece is selected or invalid move, try to select a piece
        piece = self.board[row][col]
        if piece and piece["color"] == self.current_player:
            self.selected_piece = (row, col)
            
            # Highlight the selected piece
            self.draw_board()
            self.highlight_square(row, col, self.COLORS["selected"])
            
            # Highlight possible moves
            for r in range(self.BOARD_SIZE):
                for c in range(self.BOARD_SIZE):
                    if self.is_valid_move(row, col, r, c):
                        self.highlight_square(r, c, self.COLORS["possible_move"])
            
            self.draw_pieces()
    
    def is_valid_move(self, from_row, from_col, to_row, to_col):
        """Check if a move is valid"""
        # Placeholder for move validation logic
        # In a real chess game, this would be much more complex
        
        # Basic validation: can't move to a square with your own piece
        piece = self.board[from_row][from_col]
        target = self.board[to_row][to_col]
        
        if target and target["color"] == piece["color"]:
            return False
        
        # For this simplified version, we'll just allow any move that follows
        # basic piece movement patterns
        piece_type = piece["type"]
        
        # Calculate move deltas
        row_diff = to_row - from_row
        col_diff = to_col - from_col
        
        # Pawn movement
        if piece_type == "pawn":
            # Direction depends on color
            direction = 1 if piece["color"] == "black" else -1
            
            # Forward move (no capture)
            if col_diff == 0 and not target:
                # Single square forward
                if row_diff == direction:
                    return True
                
                # Double square forward from starting position
                if (from_row == 1 and piece["color"] == "black" and row_diff == 2) or \
                   (from_row == 6 and piece["color"] == "white" and row_diff == -2):
                    # Check if the path is clear
                    middle_row = from_row + direction
                    if not self.board[middle_row][from_col]:
                        return True
            
            # Diagonal capture
            if abs(col_diff) == 1 and row_diff == direction and target:
                return True
        
        # Rook movement (horizontal and vertical)
        elif piece_type == "rook":
            if row_diff == 0 or col_diff == 0:
                # Check if path is clear
                return self.is_path_clear(from_row, from_col, to_row, to_col)
        
        # Bishop movement (diagonal)
        elif piece_type == "bishop":
            if abs(row_diff) == abs(col_diff):
                # Check if path is clear
                return self.is_path_clear(from_row, from_col, to_row, to_col)
        
        # Queen movement (horizontal, vertical, and diagonal)
        elif piece_type == "queen":
            if row_diff == 0 or col_diff == 0 or abs(row_diff) == abs(col_diff):
                # Check if path is clear
                return self.is_path_clear(from_row, from_col, to_row, to_col)
        
        # Knight movement (L-shape)
        elif piece_type == "knight":
            return (abs(row_diff) == 2 and abs(col_diff) == 1) or \
                   (abs(row_diff) == 1 and abs(col_diff) == 2)
        
        # King movement (one square in any direction)
        elif piece_type == "king":
            return abs(row_diff) <= 1 and abs(col_diff) <= 1
        
        return False
    
    def is_path_clear(self, from_row, from_col, to_row, to_col):
        """Check if the path between two squares is clear"""
        row_step = 0 if from_row == to_row else (1 if to_row > from_row else -1)
        col_step = 0 if from_col == to_col else (1 if to_col > from_col else -1)
        
        row, col = from_row + row_step, from_col + col_step
        while (row, col) != (to_row, to_col):
            if self.board[row][col]:
                return False
            row += row_step
            col += col_step
        
        return True
    
    def make_move(self, from_row, from_col, to_row, to_col):
        """Make a chess move"""
        piece = self.board[from_row][from_col]
        
        # Update king position if moving a king
        if piece["type"] == "king":
            if piece["color"] == "white":
                self.white_king_pos = (to_row, to_col)
            else:
                self.black_king_pos = (to_row, to_col)
        
        # Move the piece
        self.board[to_row][to_col] = piece
        self.board[from_row][from_col] = None
        
        # Pawn promotion (simplified - always promote to queen)
        if piece["type"] == "pawn":
            if (piece["color"] == "white" and to_row == 0) or \
               (piece["color"] == "black" and to_row == 7):
                self.board[to_row][to_col] = {"type": "queen", "color": piece["color"]}
    
    def is_in_check(self, color):
        """Check if the given color's king is in check"""
        # Find king position
        king_pos = self.white_king_pos if color == "white" else self.black_king_pos
        king_row, king_col = king_pos
        
        # Check if any opponent piece can capture the king
        opponent_color = "black" if color == "white" else "white"
        for row in range(self.BOARD_SIZE):
            for col in range(self.BOARD_SIZE):
                piece = self.board[row][col]
                if piece and piece["color"] == opponent_color:
                    if self.is_valid_move(row, col, king_row, king_col):
                        return True
        
        return False
    
    def is_checkmate(self):
        """Check if the current player is in checkmate"""
        # If not in check, can't be checkmate
        if not self.is_in_check(self.current_player):
            return False
        
        # Check if any move can get out of check
        return self.no_legal_moves()
    
    def is_stalemate(self):
        """Check if the current player is in stalemate"""
        # If in check, can't be stalemate
        if self.is_in_check(self.current_player):
            return False
        
        # Check if there are no legal moves
        return self.no_legal_moves()
    
    def no_legal_moves(self):
        """Check if the current player has no legal moves"""
        for from_row in range(self.BOARD_SIZE):
            for from_col in range(self.BOARD_SIZE):
                piece = self.board[from_row][from_col]
                if piece and piece["color"] == self.current_player:
                    for to_row in range(self.BOARD_SIZE):
                        for to_col in range(self.BOARD_SIZE):
                            if self.is_valid_move(from_row, from_col, to_row, to_col):
                                # Make the move temporarily
                                original_board = [row[:] for row in self.board]
                                original_white_king = self.white_king_pos
                                original_black_king = self.black_king_pos
                                
                                self.make_move(from_row, from_col, to_row, to_col)
                                
                                # Check if still in check
                                still_in_check = self.is_in_check(self.current_player)
                                
                                # Undo the move
                                self.board = original_board
                                self.white_king_pos = original_white_king
                                self.black_king_pos = original_black_king
                                
                                if not still_in_check:
                                    return False
        
        return True
    
    def restart_game(self):
        """Reset the game to initial state"""
        self.board = self.create_initial_board()
        self.selected_piece = None
        self.current_player = "white"
        self.white_king_pos = (7, 4)
        self.black_king_pos = (0, 4)
        self.game_over = False
        self.status_var.set("White's turn")
        
        # Redraw the board
        self.draw_board()
        self.draw_pieces()
    
    def exit_game(self):
        """Exit the game and return to the main menu"""
        if self.standalone:
            self.master.quit()
        else:
            self.master.destroy()

def start_game():
    """Function to start the game from the main menu"""
    game_window = tk.Toplevel()
    game_window.title("Chess")
    game_window.geometry("700x700")
    game_window.configure(bg="#f0f0f0")
    
    # Try to set icon
    try:
        game_window.iconphoto(True, tk.PhotoImage(file=os.path.join("assets", "icons", "chess_icon.png")))
    except:
        pass
    
    # Create the game instance
    game = ChessGame(game_window)
    
    # Make the window modal without using grab_set
    game_window.transient(game_window.master)
    game_window.focus_set()
    
    # Update the window to ensure it's fully created
    game_window.update()
    
    return game

if __name__ == "__main__":
    # Create necessary directories if they don't exist
    os.makedirs(os.path.join("assets", "images", "chess"), exist_ok=True)
    
    # Run the game in standalone mode
    game = ChessGame()
    game.master.mainloop()
