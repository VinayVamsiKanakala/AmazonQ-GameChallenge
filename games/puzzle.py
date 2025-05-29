#!/usr/bin/env python3
# Sliding Puzzle Game Implementation

import tkinter as tk
import random
import os
import time

class PuzzleGame:
    def __init__(self, master=None):
        # If no master window is provided, create our own
        self.standalone = master is None
        if self.standalone:
            self.master = tk.Tk()
            self.master.title("Sliding Puzzle")
            self.master.geometry("600x700")
        else:
            self.master = master
        
        # Game constants
        self.GRID_SIZE = 4  # 4x4 puzzle
        self.TILE_SIZE = 100
        self.BOARD_WIDTH = self.GRID_SIZE * self.TILE_SIZE
        self.BOARD_HEIGHT = self.GRID_SIZE * self.TILE_SIZE
        self.COLORS = {
            "background": "#f0f0f0",
            "tile": "#3498db",
            "tile_text": "white",
            "empty": "#f0f0f0",
            "solved": "#2ecc71"
        }
        
        # Game state
        self.board = []
        self.empty_cell = (self.GRID_SIZE - 1, self.GRID_SIZE - 1)  # Bottom right
        self.moves = 0
        self.start_time = None
        self.game_over = False
        self.timer_running = False
        
        # Create UI elements
        self.create_widgets()
        
        # Initialize the game
        self.new_game()
    
    def create_widgets(self):
        # Create a frame for the game
        self.game_frame = tk.Frame(self.master)
        self.game_frame.pack(padx=10, pady=10)
        
        # Create canvas for drawing the puzzle
        self.canvas = tk.Canvas(
            self.game_frame, 
            width=self.BOARD_WIDTH, 
            height=self.BOARD_HEIGHT,
            bg=self.COLORS["background"]
        )
        self.canvas.pack()
        
        # Bind click event
        self.canvas.bind("<Button-1>", self.on_tile_click)
        
        # Create info frame
        self.info_frame = tk.Frame(self.master, bg=self.master["bg"])
        self.info_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Create moves label
        self.moves_var = tk.StringVar()
        self.moves_var.set("Moves: 0")
        self.moves_label = tk.Label(
            self.info_frame,
            textvariable=self.moves_var,
            font=("Helvetica", 14),
            bg=self.master["bg"]
        )
        self.moves_label.pack(side=tk.LEFT, padx=10)
        
        # Create timer label
        self.timer_var = tk.StringVar()
        self.timer_var.set("Time: 00:00")
        self.timer_label = tk.Label(
            self.info_frame,
            textvariable=self.timer_var,
            font=("Helvetica", 14),
            bg=self.master["bg"]
        )
        self.timer_label.pack(side=tk.RIGHT, padx=10)
        
        # Create buttons frame
        self.buttons_frame = tk.Frame(self.master, bg=self.master["bg"])
        self.buttons_frame.pack(pady=10)
        
        # Create new game button
        self.new_game_button = tk.Button(
            self.buttons_frame,
            text="New Game",
            command=self.new_game,
            bg="#3498db",
            fg="white",
            font=("Helvetica", 10),
            relief=tk.FLAT,
            padx=20
        )
        self.new_game_button.pack(side=tk.LEFT, padx=5)
        
        # Create solve button
        self.solve_button = tk.Button(
            self.buttons_frame,
            text="Solve",
            command=self.solve_puzzle,
            bg="#2ecc71",
            fg="white",
            font=("Helvetica", 10),
            relief=tk.FLAT,
            padx=20
        )
        self.solve_button.pack(side=tk.LEFT, padx=5)
        
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
    
    def new_game(self):
        """Start a new puzzle game"""
        # Reset game state
        self.moves = 0
        self.moves_var.set("Moves: 0")
        self.game_over = False
        
        # Create solved board
        self.board = []
        num = 1
        for row in range(self.GRID_SIZE):
            self.board.append([])
            for col in range(self.GRID_SIZE):
                if row == self.GRID_SIZE - 1 and col == self.GRID_SIZE - 1:
                    self.board[row].append(None)  # Empty cell
                else:
                    self.board[row].append(num)
                    num += 1
        
        # Shuffle the board
        self.shuffle_board()
        
        # Reset empty cell position
        for row in range(self.GRID_SIZE):
            for col in range(self.GRID_SIZE):
                if self.board[row][col] is None:
                    self.empty_cell = (row, col)
                    break
        
        # Reset timer
        self.start_time = time.time()
        self.timer_running = True
        self.update_timer()
        
        # Draw the board
        self.draw_board()
    
    def shuffle_board(self):
        """Shuffle the puzzle board"""
        # Make random valid moves to shuffle the board
        empty_row, empty_col = self.GRID_SIZE - 1, self.GRID_SIZE - 1
        
        # Make a large number of random moves
        for _ in range(1000):
            # Get possible moves
            possible_moves = []
            for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                new_row, new_col = empty_row + dr, empty_col + dc
                if 0 <= new_row < self.GRID_SIZE and 0 <= new_col < self.GRID_SIZE:
                    possible_moves.append((new_row, new_col))
            
            # Choose a random move
            if possible_moves:
                move_row, move_col = random.choice(possible_moves)
                
                # Swap tiles
                self.board[empty_row][empty_col] = self.board[move_row][move_col]
                self.board[move_row][move_col] = None
                
                # Update empty cell position
                empty_row, empty_col = move_row, move_col
        
        # Ensure the puzzle is solvable
        # For a 4x4 puzzle, if the number of inversions plus the row of the empty cell
        # is odd, the puzzle is unsolvable. We'll just shuffle again if it's unsolvable.
        if not self.is_solvable():
            self.shuffle_board()
    
    def is_solvable(self):
        """Check if the current board configuration is solvable"""
        # Flatten the board into a 1D array, ignoring None
        flat_board = []
        for row in self.board:
            for tile in row:
                if tile is not None:
                    flat_board.append(tile)
        
        # Count inversions
        inversions = 0
        for i in range(len(flat_board)):
            for j in range(i + 1, len(flat_board)):
                if flat_board[i] > flat_board[j]:
                    inversions += 1
        
        # Find the row of the empty cell (0-indexed)
        empty_row = 0
        for row in range(self.GRID_SIZE):
            if None in self.board[row]:
                empty_row = row
                break
        
        # For a 4x4 puzzle, if the number of inversions plus the row of the empty cell
        # is even, the puzzle is solvable
        return (inversions + empty_row) % 2 == 0
    
    def draw_board(self):
        """Draw the puzzle board"""
        self.canvas.delete("all")
        
        for row in range(self.GRID_SIZE):
            for col in range(self.GRID_SIZE):
                tile = self.board[row][col]
                if tile is not None:
                    # Draw tile
                    x1 = col * self.TILE_SIZE
                    y1 = row * self.TILE_SIZE
                    x2 = x1 + self.TILE_SIZE
                    y2 = y1 + self.TILE_SIZE
                    
                    # Use solved color if the tile is in the correct position
                    correct_position = (tile == row * self.GRID_SIZE + col + 1)
                    color = self.COLORS["solved"] if correct_position else self.COLORS["tile"]
                    
                    # Draw tile with rounded corners
                    self.canvas.create_rectangle(
                        x1 + 2, y1 + 2, x2 - 2, y2 - 2,
                        fill=color, outline="",
                        width=0, tags=f"tile_{row}_{col}"
                    )
                    
                    # Draw tile number
                    self.canvas.create_text(
                        x1 + self.TILE_SIZE // 2,
                        y1 + self.TILE_SIZE // 2,
                        text=str(tile),
                        fill=self.COLORS["tile_text"],
                        font=("Helvetica", 24, "bold"),
                        tags=f"text_{row}_{col}"
                    )
    
    def on_tile_click(self, event):
        """Handle click on a puzzle tile"""
        if self.game_over:
            return
            
        # Convert click coordinates to grid position
        col = event.x // self.TILE_SIZE
        row = event.y // self.TILE_SIZE
        
        # Check if position is valid
        if not (0 <= row < self.GRID_SIZE and 0 <= col < self.GRID_SIZE):
            return
        
        # Check if the clicked tile is adjacent to the empty cell
        empty_row, empty_col = self.empty_cell
        if (abs(row - empty_row) == 1 and col == empty_col) or \
           (abs(col - empty_col) == 1 and row == empty_row):
            # Move the tile
            self.move_tile(row, col)
            
            # Check if the puzzle is solved
            if self.is_solved():
                self.game_over = True
                self.timer_running = False
                
                # Show win message
                self.canvas.create_rectangle(
                    0, self.BOARD_HEIGHT // 2 - 50,
                    self.BOARD_WIDTH, self.BOARD_HEIGHT // 2 + 50,
                    fill="#2ecc71", outline=""
                )
                self.canvas.create_text(
                    self.BOARD_WIDTH // 2,
                    self.BOARD_HEIGHT // 2,
                    text=f"Puzzle Solved! Moves: {self.moves}",
                    fill="white",
                    font=("Helvetica", 20, "bold")
                )
    
    def move_tile(self, row, col):
        """Move a tile to the empty cell"""
        empty_row, empty_col = self.empty_cell
        
        # Swap the tile with the empty cell
        self.board[empty_row][empty_col] = self.board[row][col]
        self.board[row][col] = None
        
        # Update empty cell position
        self.empty_cell = (row, col)
        
        # Increment move counter
        self.moves += 1
        self.moves_var.set(f"Moves: {self.moves}")
        
        # Redraw the board
        self.draw_board()
    
    def is_solved(self):
        """Check if the puzzle is solved"""
        num = 1
        for row in range(self.GRID_SIZE):
            for col in range(self.GRID_SIZE):
                # Skip the last cell (should be empty)
                if row == self.GRID_SIZE - 1 and col == self.GRID_SIZE - 1:
                    if self.board[row][col] is not None:
                        return False
                else:
                    if self.board[row][col] != num:
                        return False
                    num += 1
        return True
    
    def solve_puzzle(self):
        """Solve the puzzle (reset to solved state)"""
        # Create solved board
        num = 1
        for row in range(self.GRID_SIZE):
            for col in range(self.GRID_SIZE):
                if row == self.GRID_SIZE - 1 and col == self.GRID_SIZE - 1:
                    self.board[row][col] = None  # Empty cell
                else:
                    self.board[row][col] = num
                    num += 1
        
        # Update empty cell position
        self.empty_cell = (self.GRID_SIZE - 1, self.GRID_SIZE - 1)
        
        # Update game state
        self.game_over = True
        self.timer_running = False
        
        # Redraw the board
        self.draw_board()
        
        # Show solved message
        self.canvas.create_rectangle(
            0, self.BOARD_HEIGHT // 2 - 50,
            self.BOARD_WIDTH, self.BOARD_HEIGHT // 2 + 50,
            fill="#3498db", outline=""
        )
        self.canvas.create_text(
            self.BOARD_WIDTH // 2,
            self.BOARD_HEIGHT // 2,
            text="Puzzle Solved!",
            fill="white",
            font=("Helvetica", 20, "bold")
        )
    
    def update_timer(self):
        """Update the timer display"""
        if self.timer_running:
            elapsed = int(time.time() - self.start_time)
            minutes = elapsed // 60
            seconds = elapsed % 60
            self.timer_var.set(f"Time: {minutes:02d}:{seconds:02d}")
            self.master.after(1000, self.update_timer)
    
    def exit_game(self):
        """Exit the game and return to the main menu"""
        self.timer_running = False
        if self.standalone:
            self.master.quit()
        else:
            self.master.destroy()

def start_game():
    """Function to start the game from the main menu"""
    game_window = tk.Toplevel()
    game_window.title("Sliding Puzzle")
    game_window.geometry("600x700")
    game_window.configure(bg="#f0f0f0")
    game_window.resizable(False, False)
    
    # Try to set icon
    try:
        game_window.iconphoto(True, tk.PhotoImage(file=os.path.join("assets", "icons", "puzzle_icon.png")))
    except:
        pass
    
    # Create the game instance
    game = PuzzleGame(game_window)
    
    # Make the window modal without using grab_set
    game_window.transient(game_window.master)
    game_window.focus_set()
    
    # Update the window to ensure it's fully created
    game_window.update()
    
    return game

if __name__ == "__main__":
    # Run the game in standalone mode
    game = PuzzleGame()
    game.master.mainloop()
