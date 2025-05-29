#!/usr/bin/env python3
# Snake Game Implementation

import tkinter as tk
import random
import time
import os
import math

class SnakeGame:
    def __init__(self, master=None):
        # If no master window is provided, create our own
        self.standalone = master is None
        if self.standalone:
            self.master = tk.Tk()
            self.master.title("Snake Game")
            self.master.geometry("600x650")
        else:
            self.master = master
            
        # Game constants
        self.WIDTH = 600
        self.HEIGHT = 600
        self.GRID_SIZE = 20
        self.GRID_WIDTH = self.WIDTH // self.GRID_SIZE
        self.GRID_HEIGHT = self.HEIGHT // self.GRID_SIZE
        self.GAME_SPEED = 100  # milliseconds
        
        # Generate random snake colors each time
        self.COLORS = {
            "background": "#a8e6cf",  # Light green background
            "snake_head": self.random_green_color(dark=True),  # Random dark green head
            "snake_body": self.random_green_color(),  # Random green body
            "snake_pattern": self.random_green_color(dark=True),  # Random dark green pattern
            "border": "#007200",  # Dark green border
            "text": "#333333"  # Dark text
        }
        
        # Food items with emojis and colors
        self.FOOD_ITEMS = [
            {"emoji": "🍎", "color": "#ff0000", "points": 10},  # Apple
            {"emoji": "🍌", "color": "#ffcc00", "points": 15},  # Banana
            {"emoji": "🍒", "color": "#990000", "points": 20},  # Cherry
            {"emoji": "🍇", "color": "#6f2da8", "points": 25},  # Grapes
            {"emoji": "🍉", "color": "#ff6666", "points": 30},  # Watermelon
        ]
        
        # Game state
        self.snake = [(self.GRID_WIDTH // 2, self.GRID_HEIGHT // 2)]
        self.direction = "Right"
        self.next_direction = "Right"
        self.food = self.create_food()
        self.score = 0
        self.game_over = False
        self.paused = False
        
        # Create UI elements
        self.create_widgets()
        
        # Bind keyboard events
        self.master.bind("<KeyPress>", self.on_key_press)
        
        # Start the game loop
        self.update()
    
    def create_widgets(self):
        # Create a frame for the game
        self.game_frame = tk.Frame(self.master)
        self.game_frame.pack(padx=10, pady=10)
        
        # Create canvas for drawing the game
        self.canvas = tk.Canvas(
            self.game_frame, 
            width=self.WIDTH, 
            height=self.HEIGHT,
            bg=self.COLORS["background"]
        )
        self.canvas.pack()
        
        # Create score label
        self.score_var = tk.StringVar()
        self.score_var.set("Score: 0")
        self.score_label = tk.Label(
            self.master,
            textvariable=self.score_var,
            font=("Helvetica", 16, "bold"),
            bg=self.master["bg"],
            fg=self.COLORS["text"]
        )
        self.score_label.pack(pady=5)
        
        # Create buttons frame
        self.buttons_frame = tk.Frame(self.master, bg=self.master["bg"])
        self.buttons_frame.pack(pady=5)
        
        # Create restart button
        self.restart_button = tk.Button(
            self.buttons_frame,
            text="Restart",
            command=self.restart_game,
            bg="#3498db",
            fg="white",
            font=("Helvetica", 10, "bold"),
            relief=tk.FLAT,
            padx=20
        )
        self.restart_button.pack(side=tk.LEFT, padx=5)
        
        # Create pause button
        self.pause_var = tk.StringVar()
        self.pause_var.set("Pause")
        self.pause_button = tk.Button(
            self.buttons_frame,
            textvariable=self.pause_var,
            command=self.toggle_pause,
            bg="#f39c12",
            fg="white",
            font=("Helvetica", 10, "bold"),
            relief=tk.FLAT,
            padx=20
        )
        self.pause_button.pack(side=tk.LEFT, padx=5)
        
        # Create exit button
        self.exit_button = tk.Button(
            self.buttons_frame,
            text="Exit",
            command=self.exit_game,
            bg="#e74c3c",
            fg="white",
            font=("Helvetica", 10, "bold"),
            relief=tk.FLAT,
            padx=20
        )
        self.exit_button.pack(side=tk.LEFT, padx=5)
        
        # Draw the initial game state
        self.draw_background()
        self.draw_snake()
        self.draw_food()
    
    def draw_background(self):
        """Draw a grass-like background with border"""
        # Clear canvas
        self.canvas.delete("all")
        
        # Draw grass pattern
        for row in range(self.GRID_HEIGHT):
            for col in range(self.GRID_WIDTH):
                x = col * self.GRID_SIZE
                y = row * self.GRID_SIZE
                
                # Alternate slightly different shades of green for a grass effect
                if (row + col) % 2 == 0:
                    color = self.COLORS["background"]
                else:
                    # Slightly darker shade
                    color = "#98d6bf"
                
                self.canvas.create_rectangle(
                    x, y, x + self.GRID_SIZE, y + self.GRID_SIZE,
                    fill=color, outline="",
                    tags="background"
                )
        
        # Draw border
        self.canvas.create_rectangle(
            0, 0, self.WIDTH, self.HEIGHT,
            outline=self.COLORS["border"], width=4,
            tags="border"
        )
    
    def draw_snake(self):
        """Draw the snake on the canvas"""
        # Clear previous snake
        self.canvas.delete("snake")
        
        # Draw snake body segments first (so head appears on top)
        for i, (x, y) in enumerate(self.snake[1:], 1):
            # Calculate segment color - alternate slightly for a pattern effect
            if i % 2 == 0:
                fill_color = self.COLORS["snake_body"]
            else:
                fill_color = self.COLORS["snake_pattern"]
            
            # Draw rounded rectangle for body segment
            segment_size = self.GRID_SIZE - 2
            self.canvas.create_oval(
                x * self.GRID_SIZE + 1, 
                y * self.GRID_SIZE + 1,
                (x + 1) * self.GRID_SIZE - 1, 
                (y + 1) * self.GRID_SIZE - 1,
                fill=fill_color, outline=self.COLORS["snake_pattern"],
                width=1, tags="snake"
            )
            
            # Add pattern to body segments
            if i > 1:  # Skip the segment right after the head
                center_x = x * self.GRID_SIZE + self.GRID_SIZE // 2
                center_y = y * self.GRID_SIZE + self.GRID_SIZE // 2
                pattern_size = self.GRID_SIZE // 5
                
                # Small circle pattern on each segment
                self.canvas.create_oval(
                    center_x - pattern_size, center_y - pattern_size,
                    center_x + pattern_size, center_y + pattern_size,
                    fill=self.COLORS["snake_pattern"], outline="",
                    tags="snake"
                )
        
        # Draw snake head
        head_x, head_y = self.snake[0]
        
        # Draw head as a rounded rectangle
        self.canvas.create_oval(
            head_x * self.GRID_SIZE, 
            head_y * self.GRID_SIZE,
            (head_x + 1) * self.GRID_SIZE, 
            (head_y + 1) * self.GRID_SIZE,
            fill=self.COLORS["snake_head"], outline=self.COLORS["snake_pattern"],
            width=2, tags="snake"
        )
        
        # Add eyes to the head
        eye_size = self.GRID_SIZE // 5
        
        # Position eyes based on direction
        if self.direction == "Right":
            eye1_x, eye1_y = head_x * self.GRID_SIZE + self.GRID_SIZE * 3/4, head_y * self.GRID_SIZE + self.GRID_SIZE * 1/3
            eye2_x, eye2_y = head_x * self.GRID_SIZE + self.GRID_SIZE * 3/4, head_y * self.GRID_SIZE + self.GRID_SIZE * 2/3
        elif self.direction == "Left":
            eye1_x, eye1_y = head_x * self.GRID_SIZE + self.GRID_SIZE * 1/4, head_y * self.GRID_SIZE + self.GRID_SIZE * 1/3
            eye2_x, eye2_y = head_x * self.GRID_SIZE + self.GRID_SIZE * 1/4, head_y * self.GRID_SIZE + self.GRID_SIZE * 2/3
        elif self.direction == "Up":
            eye1_x, eye1_y = head_x * self.GRID_SIZE + self.GRID_SIZE * 1/3, head_y * self.GRID_SIZE + self.GRID_SIZE * 1/4
            eye2_x, eye2_y = head_x * self.GRID_SIZE + self.GRID_SIZE * 2/3, head_y * self.GRID_SIZE + self.GRID_SIZE * 1/4
        else:  # Down
            eye1_x, eye1_y = head_x * self.GRID_SIZE + self.GRID_SIZE * 1/3, head_y * self.GRID_SIZE + self.GRID_SIZE * 3/4
            eye2_x, eye2_y = head_x * self.GRID_SIZE + self.GRID_SIZE * 2/3, head_y * self.GRID_SIZE + self.GRID_SIZE * 3/4
        
        # Draw eyes
        self.canvas.create_oval(
            eye1_x - eye_size, eye1_y - eye_size,
            eye1_x + eye_size, eye1_y + eye_size,
            fill="white", outline="black",
            width=1, tags="snake"
        )
        self.canvas.create_oval(
            eye2_x - eye_size, eye2_y - eye_size,
            eye2_x + eye_size, eye2_y + eye_size,
            fill="white", outline="black",
            width=1, tags="snake"
        )
        
        # Add pupils
        pupil_size = eye_size // 2
        self.canvas.create_oval(
            eye1_x - pupil_size, eye1_y - pupil_size,
            eye1_x + pupil_size, eye1_y + pupil_size,
            fill="black", tags="snake"
        )
        self.canvas.create_oval(
            eye2_x - pupil_size, eye2_y - pupil_size,
            eye2_x + pupil_size, eye2_y + pupil_size,
            fill="black", tags="snake"
        )
    
    def draw_food(self):
        """Draw the food on the canvas"""
        self.canvas.delete("food")
        x, y = self.food["position"]
        food_item = self.food["item"]
        
        # Draw a circle background for the food
        self.canvas.create_oval(
            x * self.GRID_SIZE + 2, 
            y * self.GRID_SIZE + 2,
            (x + 1) * self.GRID_SIZE - 2, 
            (y + 1) * self.GRID_SIZE - 2,
            fill=food_item["color"], outline="",
            tags="food"
        )
        
        # Draw food emoji
        self.canvas.create_text(
            x * self.GRID_SIZE + self.GRID_SIZE // 2,
            y * self.GRID_SIZE + self.GRID_SIZE // 2,
            text=food_item["emoji"],
            font=("TkDefaultFont", 12),
            tags="food"
        )
    
    def create_food(self):
        """Create food at a random position that's not occupied by the snake"""
        while True:
            x = random.randint(0, self.GRID_WIDTH - 1)
            y = random.randint(0, self.GRID_HEIGHT - 1)
            if (x, y) not in self.snake:
                # Select a random food item
                food_item = random.choice(self.FOOD_ITEMS)
                return {"position": (x, y), "item": food_item}
    
    def move_snake(self):
        """Move the snake in the current direction"""
        if self.game_over or self.paused:
            return
        
        # Update direction
        self.direction = self.next_direction
        
        # Get current head position
        head_x, head_y = self.snake[0]
        
        # Calculate new head position based on direction
        if self.direction == "Up":
            new_head = (head_x, head_y - 1)
        elif self.direction == "Down":
            new_head = (head_x, head_y + 1)
        elif self.direction == "Left":
            new_head = (head_x - 1, head_y)
        elif self.direction == "Right":
            new_head = (head_x + 1, head_y)
        
        # Check for collisions
        if (
            new_head[0] < 0 or new_head[0] >= self.GRID_WIDTH or
            new_head[1] < 0 or new_head[1] >= self.GRID_HEIGHT or
            new_head in self.snake
        ):
            self.game_over = True
            self.show_game_over()
            return
        
        # Add new head to the snake
        self.snake.insert(0, new_head)
        
        # Check if food is eaten
        if new_head == self.food["position"]:
            # Increase score
            self.score += self.food["item"]["points"]
            self.score_var.set(f"Score: {self.score}")
            
            # Create new food
            self.food = self.create_food()
            self.draw_food()
            
            # Speed up slightly as snake grows
            if len(self.snake) % 5 == 0 and self.GAME_SPEED > 50:
                self.GAME_SPEED -= 5
        else:
            # Remove tail if no food was eaten
            self.snake.pop()
    
    def show_game_over(self):
        """Display game over message"""
        # Create semi-transparent overlay
        self.canvas.create_rectangle(
            50, self.HEIGHT // 2 - 100,
            self.WIDTH - 50, self.HEIGHT // 2 + 100,
            fill="#000000", outline="#ffffff",
            width=2, stipple="gray50"
        )
        
        self.canvas.create_text(
            self.WIDTH // 2, self.HEIGHT // 2 - 50,
            text="GAME OVER",
            font=("Helvetica", 30, "bold"),
            fill="#e74c3c"
        )
        self.canvas.create_text(
            self.WIDTH // 2, self.HEIGHT // 2,
            text=f"Score: {self.score}",
            font=("Helvetica", 20),
            fill="#ffffff"
        )
        self.canvas.create_text(
            self.WIDTH // 2, self.HEIGHT // 2 + 50,
            text="Press R to restart",
            font=("Helvetica", 16),
            fill="#ffffff"
        )
    
    def on_key_press(self, event):
        """Handle keyboard input"""
        key = event.keysym
        
        # Game control keys
        if key == "r" or key == "R":
            self.restart_game()
        elif key == "p" or key == "P":
            self.toggle_pause()
        elif key == "Escape":
            self.exit_game()
        
        # Direction keys - prevent 180-degree turns
        if self.direction != "Down" and (key == "Up" or key == "w"):
            self.next_direction = "Up"
        elif self.direction != "Up" and (key == "Down" or key == "s"):
            self.next_direction = "Down"
        elif self.direction != "Right" and (key == "Left" or key == "a"):
            self.next_direction = "Left"
        elif self.direction != "Left" and (key == "Right" or key == "d"):
            self.next_direction = "Right"
    
    def update(self):
        """Main game loop"""
        if not self.game_over and not self.paused:
            self.move_snake()
            self.draw_background()
            self.draw_snake()
            self.draw_food()
        
        # Schedule the next update
        self.master.after(self.GAME_SPEED, self.update)
    
    def random_green_color(self, dark=False):
        """Generate a random green color"""
        if dark:
            # Darker green shades
            r = random.randint(0, 60)
            g = random.randint(100, 180)
            b = random.randint(0, 60)
        else:
            # Lighter green shades
            r = random.randint(30, 120)
            g = random.randint(160, 240)
            b = random.randint(30, 120)
        
        # Convert to hex color
        return f"#{r:02x}{g:02x}{b:02x}"
    
    def restart_game(self):
        """Reset the game to initial state"""
        self.snake = [(self.GRID_WIDTH // 2, self.GRID_HEIGHT // 2)]
        self.direction = "Right"
        self.next_direction = "Right"
        self.food = self.create_food()
        self.score = 0
        self.score_var.set("Score: 0")
        self.game_over = False
        self.paused = False
        self.pause_var.set("Pause")
        self.GAME_SPEED = 100  # Reset speed
        
        # Generate new random colors for the snake
        self.COLORS["snake_head"] = self.random_green_color(dark=True)
        self.COLORS["snake_body"] = self.random_green_color()
        self.COLORS["snake_pattern"] = self.random_green_color(dark=True)
        
        # Clear canvas and redraw
        self.draw_background()
        self.draw_snake()
        self.draw_food()
    
    def toggle_pause(self):
        """Pause or resume the game"""
        if self.game_over:
            return
            
        self.paused = not self.paused
        if self.paused:
            self.pause_var.set("Resume")
            
            # Create semi-transparent overlay
            self.canvas.create_rectangle(
                50, self.HEIGHT // 2 - 50,
                self.WIDTH - 50, self.HEIGHT // 2 + 50,
                fill="#000000", outline="#ffffff",
                width=2, stipple="gray50",
                tags="pause"
            )
            
            self.canvas.create_text(
                self.WIDTH // 2, self.HEIGHT // 2,
                text="PAUSED",
                font=("Helvetica", 30, "bold"),
                fill="#3498db",
                tags="pause"
            )
        else:
            self.pause_var.set("Pause")
            self.canvas.delete("pause")
    
    def exit_game(self):
        """Exit the game and return to the main menu"""
        if self.standalone:
            self.master.quit()
        else:
            self.master.destroy()

def start_game():
    """Function to start the game from the main menu"""
    game_window = tk.Toplevel()
    game_window.title("Snake Game")
    game_window.geometry("600x650")
    game_window.configure(bg="#f0f0f0")
    game_window.resizable(False, False)
    
    # Try to set icon
    try:
        game_window.iconphoto(True, tk.PhotoImage(file=os.path.join("assets", "icons", "snake_icon.png")))
    except:
        pass
    
    # Create the game instance
    game = SnakeGame(game_window)
    
    # Make the window modal - without using grab_set which can cause issues
    game_window.transient(game_window.master)
    game_window.focus_set()
    
    # Update the window to ensure it's fully created before returning
    game_window.update()
    
    return game

if __name__ == "__main__":
    # Run the game in standalone mode
    game = SnakeGame()
    game.master.mainloop()
