#!/usr/bin/env python3
# Simple Carrom Game Implementation

import tkinter as tk
from tkinter import messagebox
import math
import random

class CarromGame:
    def __init__(self, master=None):
        """Initialize the Carrom game"""
        self.master = master or tk.Tk()
        self.master.title("Carrom Game")
        self.master.geometry("800x850")
        self.master.resizable(False, False)
        
        # Game constants
        self.BOARD_SIZE = 600
        self.BOARD_MARGIN = 100
        self.POCKET_RADIUS = 30
        self.STRIKER_RADIUS = 20
        self.COIN_RADIUS = 15
        self.WHITE_COINS = 9
        self.BLACK_COINS = 9
        self.RED_COINS = 1
        
        # Game state variables
        self.game_over = False
        self.turn = "Player 1"
        self.player1_score = 0
        self.player2_score = 0
        self.striker_position = 400  # X position on the bottom side
        self.striker_angle = 90  # Angle in degrees (90 = straight up)
        self.striker_power = 50  # Power percentage
        self.moving_pieces = []  # List of pieces currently in motion
        self.selected_piece = None
        self.game_phase = "positioning"  # positioning, aiming, power, moving
        
        # Create the UI
        self.create_widgets()
        
        # Initialize the game
        self.setup_game()
        
        # Start the game loop
        self.update_game()
    
    def create_widgets(self):
        """Create all UI elements"""
        # Main frame
        self.main_frame = tk.Frame(self.master, bg="#f0f0f0")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Game canvas
        self.canvas = tk.Canvas(
            self.main_frame, 
            width=self.BOARD_SIZE + 2*self.BOARD_MARGIN,
            height=self.BOARD_SIZE + 2*self.BOARD_MARGIN,
            bg="#f0f0f0"
        )
        self.canvas.pack(pady=10)
        
        # Control frame
        self.control_frame = tk.Frame(self.main_frame, bg="#f0f0f0")
        self.control_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # Player info and controls
        self.info_frame = tk.Frame(self.control_frame, bg="#f0f0f0")
        self.info_frame.pack(side=tk.LEFT, fill=tk.Y)
        
        self.player_label = tk.Label(
            self.info_frame, 
            text=f"Turn: {self.turn}", 
            font=("Arial", 14, "bold"),
            bg="#f0f0f0"
        )
        self.player_label.pack(anchor=tk.W, pady=5)
        
        self.score_label = tk.Label(
            self.info_frame, 
            text=f"Score - Player 1: {self.player1_score} | Player 2: {self.player2_score}", 
            font=("Arial", 12),
            bg="#f0f0f0"
        )
        self.score_label.pack(anchor=tk.W, pady=5)
        
        # Power control
        self.power_frame = tk.Frame(self.control_frame, bg="#f0f0f0")
        self.power_frame.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.power_label = tk.Label(
            self.power_frame, 
            text="Power:", 
            font=("Arial", 12),
            bg="#f0f0f0"
        )
        self.power_label.pack(side=tk.LEFT, padx=5)
        
        self.power_scale = tk.Scale(
            self.power_frame,
            from_=10,
            to=100,
            orient=tk.HORIZONTAL,
            length=200,
            bg="#f0f0f0",
            command=self.set_power
        )
        self.power_scale.set(50)
        self.power_scale.pack(side=tk.LEFT, padx=5)
        
        # Bind canvas events
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        self.canvas.bind("<Motion>", self.on_canvas_move)
        
        # Create a restart button
        self.restart_button = tk.Button(
            self.control_frame,
            text="Restart Game",
            command=self.restart_game,
            font=("Arial", 12),
            bg="#4CAF50",
            fg="white",
            padx=10
        )
        self.restart_button.pack(side=tk.RIGHT, padx=20)
    
    def setup_game(self):
        """Initialize the game state and pieces"""
        # Initialize pieces
        self.coins = []
        self.striker = None
        
        # Place coins in the center
        self.place_initial_coins()
        
        # Create the striker
        self.create_striker()
        
        # Draw everything
        self.draw_board()
    
    def place_initial_coins(self):
        """Place the coins in their initial positions"""
        center_x = self.BOARD_SIZE // 2
        center_y = self.BOARD_SIZE // 2
        
        # Place the red coin in the center
        self.coins.append({
            'type': 'red',
            'x': center_x,
            'y': center_y,
            'vx': 0,
            'vy': 0,
            'radius': self.COIN_RADIUS
        })
        
        # Place black and white coins in a circle around the center
        coin_types = ['black'] * self.BLACK_COINS + ['white'] * self.WHITE_COINS
        random.shuffle(coin_types)
        
        radius = 40  # Distance from center
        for i, coin_type in enumerate(coin_types):
            angle = 2 * math.pi * i / len(coin_types)
            x = center_x + radius * math.cos(angle)
            y = center_y + radius * math.sin(angle)
            
            self.coins.append({
                'type': coin_type,
                'x': x,
                'y': y,
                'vx': 0,
                'vy': 0,
                'radius': self.COIN_RADIUS
            })
    
    def create_striker(self):
        """Create the striker piece"""
        self.striker = {
            'type': 'striker',
            'x': self.striker_position,
            'y': self.BOARD_SIZE - 100,  # Bottom side of the board
            'vx': 0,
            'vy': 0,
            'radius': self.STRIKER_RADIUS
        }
    
    def draw_board(self):
        """Draw the complete game board and all pieces"""
        # Clear the canvas
        self.canvas.delete("all")
        
        # Draw the board (simple version without images)
        # Outer border
        self.canvas.create_rectangle(
            self.BOARD_MARGIN, self.BOARD_MARGIN,
            self.BOARD_MARGIN + self.BOARD_SIZE, self.BOARD_MARGIN + self.BOARD_SIZE,
            fill="#C19A6B", outline="#8B4513", width=20
        )
        
        # Inner playing area
        inner_margin = 50
        self.canvas.create_rectangle(
            self.BOARD_MARGIN + inner_margin, self.BOARD_MARGIN + inner_margin,
            self.BOARD_MARGIN + self.BOARD_SIZE - inner_margin, 
            self.BOARD_MARGIN + self.BOARD_SIZE - inner_margin,
            fill="#E8C19A", outline="#8B4513", width=2
        )
        
        # Draw corner pockets
        pocket_positions = [
            (self.BOARD_MARGIN + inner_margin, self.BOARD_MARGIN + inner_margin),  # Top-left
            (self.BOARD_MARGIN + self.BOARD_SIZE - inner_margin, self.BOARD_MARGIN + inner_margin),  # Top-right
            (self.BOARD_MARGIN + inner_margin, self.BOARD_MARGIN + self.BOARD_SIZE - inner_margin),  # Bottom-left
            (self.BOARD_MARGIN + self.BOARD_SIZE - inner_margin, self.BOARD_MARGIN + self.BOARD_SIZE - inner_margin)  # Bottom-right
        ]
        
        for x, y in pocket_positions:
            self.canvas.create_oval(
                x - self.POCKET_RADIUS, y - self.POCKET_RADIUS,
                x + self.POCKET_RADIUS, y + self.POCKET_RADIUS,
                fill="#4A2511", outline=""
            )
        
        # Draw center circle
        center_x = self.BOARD_MARGIN + self.BOARD_SIZE // 2
        center_y = self.BOARD_MARGIN + self.BOARD_SIZE // 2
        self.canvas.create_oval(
            center_x - 50, center_y - 50,
            center_x + 50, center_y + 50,
            outline="#8B4513", width=2
        )
        
        # Draw striker line
        striker_line_y = self.BOARD_MARGIN + self.BOARD_SIZE - inner_margin - 50
        self.canvas.create_line(
            self.BOARD_MARGIN + inner_margin, striker_line_y,
            self.BOARD_MARGIN + self.BOARD_SIZE - inner_margin, striker_line_y,
            fill="#8B4513", width=2
        )
        
        # Draw all coins
        for coin in self.coins:
            self.draw_coin(coin)
        
        # Draw the striker
        if self.striker:
            self.draw_striker()
        
        # Draw the aiming line if in aiming phase
        if self.game_phase == "aiming" and self.striker:
            self.draw_aiming_line()
    
    def draw_coin(self, coin):
        """Draw a single coin on the canvas"""
        x = self.BOARD_MARGIN + coin['x']
        y = self.BOARD_MARGIN + coin['y']
        radius = coin['radius']
        
        if coin['type'] == 'white':
            color = '#FFFFFF'
            outline = '#000000'
        elif coin['type'] == 'black':
            color = '#000000'
            outline = '#FFFFFF'
        else:  # red
            color = '#FF0000'
            outline = '#FFFFFF'
        
        self.canvas.create_oval(
            x - radius, y - radius,
            x + radius, y + radius,
            fill=color,
            outline=outline,
            width=2
        )
    
    def draw_striker(self):
        """Draw the striker on the canvas"""
        x = self.BOARD_MARGIN + self.striker['x']
        y = self.BOARD_MARGIN + self.striker['y']
        radius = self.striker['radius']
        
        self.canvas.create_oval(
            x - radius, y - radius,
            x + radius, y + radius,
            fill='#1E90FF',
            outline='#000000',
            width=2
        )
    
    def draw_aiming_line(self):
        """Draw the aiming line from the striker"""
        if not self.striker:
            return
            
        x = self.BOARD_MARGIN + self.striker['x']
        y = self.BOARD_MARGIN + self.striker['y']
        
        # Calculate end point based on angle
        angle_rad = math.radians(self.striker_angle)
        line_length = 100
        end_x = x + line_length * math.cos(angle_rad)
        end_y = y - line_length * math.sin(angle_rad)  # Subtract because canvas y increases downward
        
        # Draw the line
        self.canvas.create_line(
            x, y, end_x, end_y,
            fill='#1E90FF',
            width=2,
            dash=(5, 3)
        )
    
    def on_canvas_click(self, event):
        """Handle canvas click events"""
        if self.game_over:
            return
            
        # Convert to board coordinates
        board_x = event.x - self.BOARD_MARGIN
        board_y = event.y - self.BOARD_MARGIN
        
        if self.game_phase == "positioning":
            # Check if click is on the striker line
            if abs(board_y - (self.BOARD_SIZE - 100)) < 20:
                # Update striker position
                self.striker['x'] = board_x
                # Constrain to valid range
                self.striker['x'] = max(100, min(self.BOARD_SIZE - 100, self.striker['x']))
                self.draw_board()
                self.game_phase = "aiming"
                
        elif self.game_phase == "aiming":
            # Calculate angle from striker to click point
            dx = board_x - self.striker['x']
            dy = self.striker['y'] - board_y  # Invert y because canvas y increases downward
            self.striker_angle = math.degrees(math.atan2(dy, dx))
            self.draw_board()
            self.game_phase = "power"
            
        elif self.game_phase == "power":
            # Use the power from the scale and shoot
            self.shoot_striker()
            self.game_phase = "moving"
    
    def on_canvas_move(self, event):
        """Handle mouse movement over the canvas"""
        if self.game_over or self.game_phase != "aiming":
            return
            
        # Convert to board coordinates
        board_x = event.x - self.BOARD_MARGIN
        board_y = event.y - self.BOARD_MARGIN
        
        # Calculate angle from striker to mouse position
        dx = board_x - self.striker['x']
        dy = self.striker['y'] - board_y  # Invert y because canvas y increases downward
        self.striker_angle = math.degrees(math.atan2(dy, dx))
        
        # Redraw the board with the new aiming line
        self.draw_board()
    
    def set_power(self, value):
        """Set the striker power"""
        self.striker_power = int(value)
    
    def shoot_striker(self):
        """Shoot the striker with the current angle and power"""
        if not self.striker:
            return
            
        # Calculate velocity components based on angle and power
        angle_rad = math.radians(self.striker_angle)
        speed = self.striker_power / 10  # Scale power to a reasonable speed
        
        self.striker['vx'] = speed * math.cos(angle_rad)
        self.striker['vy'] = -speed * math.sin(angle_rad)  # Negative because canvas y increases downward
        
        # Add striker to moving pieces
        self.moving_pieces = [self.striker] + self.coins
    
    def update_game(self):
        """Main game loop update function"""
        if self.game_phase == "moving":
            # Update positions of all moving pieces
            self.update_physics()
            
            # Check if all pieces have stopped moving
            if all(abs(piece['vx']) < 0.1 and abs(piece['vy']) < 0.1 for piece in self.moving_pieces):
                self.moving_pieces = []
                self.game_phase = "positioning"
                
                # Check for pocketed pieces
                self.check_pocketed_pieces()
                
                # Check for game over
                if self.check_game_over():
                    self.game_over = True
                    self.show_game_over()
                else:
                    # Switch turns
                    self.turn = "Player 2" if self.turn == "Player 1" else "Player 1"
                    self.player_label.config(text=f"Turn: {self.turn}")
                    
                    # Reset the striker
                    self.create_striker()
        
        # Redraw the board
        self.draw_board()
        
        # Schedule the next update
        self.master.after(16, self.update_game)  # ~60 FPS
    
    def update_physics(self):
        """Update the physics for all moving pieces"""
        # Apply friction to all pieces
        friction = 0.98
        for piece in self.moving_pieces:
            piece['vx'] *= friction
            piece['vy'] *= friction
            
            # Update position
            piece['x'] += piece['vx']
            piece['y'] += piece['vy']
            
            # Handle collisions with walls
            self.handle_wall_collisions(piece)
        
        # Handle collisions between pieces
        self.handle_piece_collisions()
    
    def handle_wall_collisions(self, piece):
        """Handle collisions with the walls"""
        # Get board boundaries
        min_x = 50 + piece['radius']
        max_x = self.BOARD_SIZE - 50 - piece['radius']
        min_y = 50 + piece['radius']
        max_y = self.BOARD_SIZE - 50 - piece['radius']
        
        # Bounce off walls with some energy loss
        bounce_factor = 0.8
        
        if piece['x'] < min_x:
            piece['x'] = min_x
            piece['vx'] = -piece['vx'] * bounce_factor
        elif piece['x'] > max_x:
            piece['x'] = max_x
            piece['vx'] = -piece['vx'] * bounce_factor
            
        if piece['y'] < min_y:
            piece['y'] = min_y
            piece['vy'] = -piece['vy'] * bounce_factor
        elif piece['y'] > max_y:
            piece['y'] = max_y
            piece['vy'] = -piece['vy'] * bounce_factor
    
    def handle_piece_collisions(self):
        """Handle collisions between pieces"""
        for i in range(len(self.moving_pieces)):
            for j in range(i + 1, len(self.moving_pieces)):
                piece1 = self.moving_pieces[i]
                piece2 = self.moving_pieces[j]
                
                # Calculate distance between centers
                dx = piece2['x'] - piece1['x']
                dy = piece2['y'] - piece1['y']
                distance = math.sqrt(dx*dx + dy*dy)
                
                # Check for collision
                min_distance = piece1['radius'] + piece2['radius']
                if distance < min_distance:
                    # Collision detected - calculate collision response
                    
                    # Normalize collision vector
                    if distance == 0:  # Avoid division by zero
                        nx, ny = 1, 0
                    else:
                        nx, ny = dx/distance, dy/distance
                    
                    # Relative velocity
                    dvx = piece2['vx'] - piece1['vx']
                    dvy = piece2['vy'] - piece1['vy']
                    
                    # Velocity along collision normal
                    vn = dvx*nx + dvy*ny
                    
                    # Don't collide if objects are moving away from each other
                    if vn > 0:
                        continue
                    
                    # Collision impulse
                    impulse = -(1 + 0.8) * vn  # 0.8 is restitution coefficient
                    impulse /= 2  # Equal mass assumption
                    
                    # Apply impulse
                    piece1['vx'] -= impulse * nx
                    piece1['vy'] -= impulse * ny
                    piece2['vx'] += impulse * nx
                    piece2['vy'] += impulse * ny
                    
                    # Separate the pieces to avoid sticking
                    overlap = min_distance - distance
                    piece1['x'] -= overlap * nx / 2
                    piece1['y'] -= overlap * ny / 2
                    piece2['x'] += overlap * nx / 2
                    piece2['y'] += overlap * ny / 2
    
    def check_pocketed_pieces(self):
        """Check if any pieces have been pocketed"""
        # Define pocket positions
        pockets = [
            (50, 50),  # Top-left
            (self.BOARD_SIZE - 50, 50),  # Top-right
            (50, self.BOARD_SIZE - 50),  # Bottom-left
            (self.BOARD_SIZE - 50, self.BOARD_SIZE - 50)  # Bottom-right
        ]
        
        # Check each piece against each pocket
        pocketed_coins = []
        for coin in self.coins:
            for pocket_x, pocket_y in pockets:
                dx = coin['x'] - pocket_x
                dy = coin['y'] - pocket_y
                distance = math.sqrt(dx*dx + dy*dy)
                
                if distance < self.POCKET_RADIUS:
                    pocketed_coins.append(coin)
                    
                    # Award points
                    if self.turn == "Player 1":
                        if coin['type'] == 'white':
                            self.player1_score += 1
                        elif coin['type'] == 'black':
                            self.player1_score += 1
                        elif coin['type'] == 'red':
                            self.player1_score += 3
                    else:  # Player 2
                        if coin['type'] == 'white':
                            self.player2_score += 1
                        elif coin['type'] == 'black':
                            self.player2_score += 1
                        elif coin['type'] == 'red':
                            self.player2_score += 3
                    
                    break  # No need to check other pockets
        
        # Remove pocketed coins
        for coin in pocketed_coins:
            self.coins.remove(coin)
        
        # Check if striker was pocketed
        for pocket_x, pocket_y in pockets:
            if self.striker:
                dx = self.striker['x'] - pocket_x
                dy = self.striker['y'] - pocket_y
                distance = math.sqrt(dx*dx + dy*dy)
                
                if distance < self.POCKET_RADIUS:
                    # Penalty for pocketing the striker
                    if self.turn == "Player 1":
                        self.player1_score = max(0, self.player1_score - 1)
                    else:
                        self.player2_score = max(0, self.player2_score - 1)
                    
                    self.striker = None
                    break
        
        # Update score display
        self.score_label.config(text=f"Score - Player 1: {self.player1_score} | Player 2: {self.player2_score}")
    
    def check_game_over(self):
        """Check if the game is over"""
        # Game is over if all coins are pocketed
        if not self.coins:
            return True
        
        # Game is over if one player reaches 21 points
        if self.player1_score >= 21 or self.player2_score >= 21:
            return True
        
        return False
    
    def show_game_over(self):
        """Show game over message"""
        winner = "Player 1" if self.player1_score > self.player2_score else "Player 2"
        if self.player1_score == self.player2_score:
            winner = "It's a tie!"
        else:
            winner = f"{winner} wins!"
        
        messagebox.showinfo("Game Over", f"Game Over!\n{winner}\n\nFinal Score:\nPlayer 1: {self.player1_score}\nPlayer 2: {self.player2_score}")
    
    def restart_game(self):
        """Restart the game"""
        self.game_over = False
        self.turn = "Player 1"
        self.player1_score = 0
        self.player2_score = 0
        self.game_phase = "positioning"
        
        # Reset the board
        self.coins = []
        self.striker = None
        self.moving_pieces = []
        
        # Place coins and striker
        self.place_initial_coins()
        self.create_striker()
        
        # Update UI
        self.player_label.config(text=f"Turn: {self.turn}")
        self.score_label.config(text=f"Score - Player 1: {self.player1_score} | Player 2: {self.player2_score}")
        self.power_scale.set(50)

def start_game():
    """Start the Carrom game"""
    game = CarromGame()
    return game

if __name__ == "__main__":
    game = start_game()
    game.master.mainloop()
