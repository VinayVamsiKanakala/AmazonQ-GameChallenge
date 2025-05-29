#!/usr/bin/env python3
# Memory Match Card Game Implementation

import tkinter as tk
import random
import os
import time

class MemoryGame:
    def __init__(self, master=None):
        # If no master window is provided, create our own
        self.standalone = master is None
        if self.standalone:
            self.master = tk.Tk()
            self.master.title("Memory Match")
            self.master.geometry("800x700")
        else:
            self.master = master
        
        # Game constants
        self.ROWS = 4
        self.COLS = 5
        self.CARD_WIDTH = 120
        self.CARD_HEIGHT = 150
        self.BOARD_WIDTH = self.COLS * (self.CARD_WIDTH + 10)
        self.BOARD_HEIGHT = self.ROWS * (self.CARD_HEIGHT + 10)
        self.COLORS = {
            "background": "#f0f0f0",
            "card_back": "#3498db",
            "card_front": "white",
            "matched": "#2ecc71"
        }
        
        # Card symbols (emojis for simplicity)
        self.symbols = [
            "🐶", "🐱", "🐭", "🐹", "🐰", "🦊", "🐻", "🐼", "🐨", "🦁"
        ]
        
        # Game state
        self.cards = []
        self.flipped = []
        self.matched = []
        self.moves = 0
        self.start_time = None
        self.game_over = False
        self.timer_running = False
        self.can_flip = True  # Flag to prevent rapid clicking
        
        # Create UI elements
        self.create_widgets()
        
        # Initialize the game
        self.new_game()
    
    def create_widgets(self):
        # Create a frame for the game
        self.game_frame = tk.Frame(self.master)
        self.game_frame.pack(padx=10, pady=10)
        
        # Create canvas for drawing the cards
        self.canvas = tk.Canvas(
            self.game_frame, 
            width=self.BOARD_WIDTH, 
            height=self.BOARD_HEIGHT,
            bg=self.COLORS["background"]
        )
        self.canvas.pack()
        
        # Bind click event
        self.canvas.bind("<Button-1>", self.on_card_click)
        
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
        """Start a new memory match game"""
        # Reset game state
        self.moves = 0
        self.moves_var.set("Moves: 0")
        self.flipped = []
        self.matched = []
        self.game_over = False
        self.can_flip = True
        
        # Create and shuffle cards
        self.create_cards()
        
        # Reset timer
        self.start_time = time.time()
        self.timer_running = True
        self.update_timer()
        
        # Draw the cards
        self.draw_cards()
    
    def create_cards(self):
        """Create and shuffle the cards"""
        # Create pairs of cards
        num_pairs = (self.ROWS * self.COLS) // 2
        symbols = self.symbols[:num_pairs] * 2
        random.shuffle(symbols)
        
        # Create card objects
        self.cards = []
        index = 0
        for row in range(self.ROWS):
            for col in range(self.COLS):
                x = col * (self.CARD_WIDTH + 10) + 5
                y = row * (self.CARD_HEIGHT + 10) + 5
                
                card = {
                    "id": index,
                    "symbol": symbols[index],
                    "row": row,
                    "col": col,
                    "x": x,
                    "y": y,
                    "rect_id": None,
                    "text_id": None
                }
                
                self.cards.append(card)
                index += 1
    
    def draw_cards(self):
        """Draw all cards on the canvas"""
        self.canvas.delete("all")
        
        for card in self.cards:
            # Draw card back or front based on state
            if card["id"] in self.flipped or card["id"] in self.matched:
                # Card is flipped or matched
                fill_color = self.COLORS["matched"] if card["id"] in self.matched else self.COLORS["card_front"]
                
                # Draw card front
                card["rect_id"] = self.canvas.create_rectangle(
                    card["x"], card["y"],
                    card["x"] + self.CARD_WIDTH, card["y"] + self.CARD_HEIGHT,
                    fill=fill_color, outline="#ddd",
                    width=2, tags=f"card_{card['id']}"
                )
                
                # Draw symbol
                card["text_id"] = self.canvas.create_text(
                    card["x"] + self.CARD_WIDTH // 2,
                    card["y"] + self.CARD_HEIGHT // 2,
                    text=card["symbol"],
                    font=("Helvetica", 36),
                    tags=f"symbol_{card['id']}"
                )
            else:
                # Card is face down
                card["rect_id"] = self.canvas.create_rectangle(
                    card["x"], card["y"],
                    card["x"] + self.CARD_WIDTH, card["y"] + self.CARD_HEIGHT,
                    fill=self.COLORS["card_back"], outline="#ddd",
                    width=2, tags=f"card_{card['id']}"
                )
                
                # Draw card back design (simple pattern)
                for i in range(5):
                    self.canvas.create_line(
                        card["x"] + 20, card["y"] + 20 + i * 25,
                        card["x"] + self.CARD_WIDTH - 20, card["y"] + 20 + i * 25,
                        fill="white", width=2,
                        tags=f"card_{card['id']}"
                    )
    
    def on_card_click(self, event):
        """Handle click on a card"""
        if self.game_over or not self.can_flip:
            return
        
        # Find which card was clicked
        for card in self.cards:
            if (card["x"] <= event.x <= card["x"] + self.CARD_WIDTH and
                card["y"] <= event.y <= card["y"] + self.CARD_HEIGHT):
                
                # Can't flip already matched or flipped cards
                if card["id"] in self.matched or card["id"] in self.flipped:
                    return
                
                # Can't flip more than 2 cards at once
                if len(self.flipped) >= 2:
                    return
                
                # Flip the card
                self.flip_card(card["id"])
                
                # Check for match if 2 cards are flipped
                if len(self.flipped) == 2:
                    self.moves += 1
                    self.moves_var.set(f"Moves: {self.moves}")
                    self.check_match()
                
                break
    
    def flip_card(self, card_id):
        """Flip a card to show its symbol"""
        self.flipped.append(card_id)
        self.draw_cards()
    
    def check_match(self):
        """Check if the two flipped cards match"""
        # Prevent further card flips during animation
        self.can_flip = False
        
        # Get the two flipped cards
        card1 = next(card for card in self.cards if card["id"] == self.flipped[0])
        card2 = next(card for card in self.cards if card["id"] == self.flipped[1])
        
        # Schedule the check after a short delay
        self.master.after(1000, lambda: self.process_match(card1, card2))
    
    def process_match(self, card1, card2):
        """Process the result of a card match check"""
        if card1["symbol"] == card2["symbol"]:
            # Cards match
            self.matched.extend(self.flipped)
            
            # Check if all cards are matched
            if len(self.matched) == len(self.cards):
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
                    text=f"You Win! Moves: {self.moves}",
                    fill="white",
                    font=("Helvetica", 24, "bold")
                )
        
        # Reset flipped cards
        self.flipped = []
        
        # Redraw cards
        self.draw_cards()
        
        # Allow flipping cards again
        self.can_flip = True
    
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
    game_window.title("Memory Match")
    game_window.geometry("800x700")
    game_window.configure(bg="#f0f0f0")
    game_window.resizable(False, False)
    
    # Try to set icon
    try:
        game_window.iconphoto(True, tk.PhotoImage(file=os.path.join("assets", "icons", "cards_icon.png")))
    except:
        pass
    
    # Create the game instance
    game = MemoryGame(game_window)
    
    # Make the window modal without using grab_set
    game_window.transient(game_window.master)
    game_window.focus_set()
    
    # Update the window to ensure it's fully created
    game_window.update()
    
    return game

if __name__ == "__main__":
    # Run the game in standalone mode
    game = MemoryGame()
    game.master.mainloop()
