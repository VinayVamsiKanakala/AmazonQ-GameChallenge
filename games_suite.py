#!/usr/bin/env python3
# Main launcher for the games suite

import tkinter as tk
from tkinter import ttk, messagebox
import os
import sys  
import importlib
import random
import time
from PIL import Image, ImageTk
import math

class GamesSuite(tk.Tk):
    def __init__(self):
        super().__init__()
        
        # Configure the main window
        self.title("Offline Games")
        self.geometry("1024x768")
        self.minsize(800, 600)
        self.configure(bg="#121212")  # Dark background as fallback
        
        # Set app icon if available
        try:
            self.iconphoto(True, tk.PhotoImage(file="assets/icons/app_icon.png"))
        except:
            pass
        
        # Animation variables
        self.animation_items = {}
        self.animation_active = False
        
        # Create the main canvas that will contain everything
        self.canvas = tk.Canvas(self, highlightthickness=0, bg="#121212")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Load background images
        self.bg_images = self.load_background_images()
        
        # Set random background
        self.set_random_background()
        
        # Create widgets
        self.create_widgets()
        
        # Start floating animation
        self.start_floating_animation()
        
        # Bind resize event
        self.bind("<Configure>", self.on_resize)
    
    def load_background_images(self):
        """Load all background images from assets/backgrounds folder"""
        bg_images = []
        
        # Try to load from Q-Games/backgrounds first
        bg_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "backgrounds")
        
        # If that doesn't exist, try assets/backgrounds
        if not os.path.exists(bg_dir):
            bg_dir = os.path.join("assets", "backgrounds")
        
        if os.path.exists(bg_dir):
            for file in os.listdir(bg_dir):
                if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                    try:
                        img_path = os.path.join(bg_dir, file)
                        img = Image.open(img_path)
                        bg_images.append(img)
                        # Removed print statement to hide loading info
                    except Exception as e:
                        # Silently continue if an image fails to load
                        pass
        
        # If no images found, create a default gradient background
        if not bg_images:
            print("No background images found, creating default night sky background")
            # Create a dark blue gradient for night sky effect
            img = Image.new('RGB', (1920, 1080))
            pixels = img.load()
            
            for i in range(img.size[0]):
                for j in range(img.size[1]):
                    # Create gradient from dark blue to black
                    r = int(0 + (i/img.size[0]) * 20)
                    g = int(0 + (i/img.size[0]) * 30)
                    b = int(30 + (j/img.size[1]) * 50)
                    pixels[i, j] = (r, g, b)
            
            # Add some "stars"
            for _ in range(1000):
                x = random.randint(0, img.size[0]-1)
                y = random.randint(0, img.size[1]-1)
                brightness = random.randint(180, 255)
                pixels[x, y] = (brightness, brightness, brightness)
            
            bg_images.append(img)
        
        return bg_images
    
    def set_random_background(self):
        """Set a random background image"""
        if not self.bg_images:
            return
            
        # Choose random background
        bg_img = random.choice(self.bg_images)
        
        # Resize to fit window
        resized_img = self.resize_image(bg_img)
        
        # Convert to PhotoImage
        self.bg_photo = ImageTk.PhotoImage(resized_img)
        
        # Update canvas background
        self.canvas.delete("background")
        self.canvas.create_image(0, 0, image=self.bg_photo, anchor=tk.NW, tags="background")
        
        # Make sure background is at the bottom
        self.canvas.tag_lower("background")
    
    def resize_image(self, img):
        """Resize image to fit the window"""
        window_width = self.winfo_width()
        window_height = self.winfo_height()
        
        # Use at least 800x600 for initial sizing
        if window_width < 100:
            window_width = 1024
        if window_height < 100:
            window_height = 768
            
        # Resize image maintaining aspect ratio and covering the whole window
        img_width, img_height = img.size
        ratio = max(window_width/img_width, window_height/img_height)
        new_size = (int(img_width*ratio), int(img_height*ratio))
        
        resized_img = img.resize(new_size, Image.LANCZOS)
        
        # Crop to window size
        left = (resized_img.width - window_width) // 2
        top = (resized_img.height - window_height) // 2
        right = left + window_width
        bottom = top + window_height
        
        # Make sure we don't try to crop outside the image bounds
        left = max(0, left)
        top = max(0, top)
        right = min(resized_img.width, right)
        bottom = min(resized_img.height, bottom)
        
        cropped_img = resized_img.crop((left, top, right, bottom))
        return cropped_img
    
    def on_resize(self, event):
        """Handle window resize event"""
        # Only process if it's a main window resize, not a child widget
        if event.widget == self:
            # Throttle resize events
            self.after_cancel(self.after_id) if hasattr(self, 'after_id') else None
            self.after_id = self.after(100, self.delayed_resize)
    
    def delayed_resize(self):
        """Delayed resize handler to avoid too many updates"""
        self.set_random_background()
        self.update_layout()
    
    def update_layout(self):
        """Update the layout of all elements based on window size"""
        # Get current window dimensions
        window_width = self.winfo_width()
        window_height = self.winfo_height()
        
        # Update title position
        self.canvas.coords(self.title_text, window_width // 2, 50)
        
        # Update game grid
        self.update_game_grid()
        
        # Update footer position
        self.canvas.coords(self.footer_text, window_width // 2, window_height - 25)
    
    def update_game_grid(self):
        """Update the game grid layout"""
        # Get current window dimensions
        window_width = self.winfo_width()
        window_height = self.winfo_height()
        
        # Calculate grid dimensions
        grid_width = window_width - 100  # 50px padding on each side
        grid_height = window_height - 150  # 100px for header, 50px for footer
        
        # Calculate item dimensions
        cols = 3
        rows = 2
        item_width = grid_width // cols
        item_height = grid_height // rows
        
        # Position each game button
        for i, game_id in enumerate(self.game_buttons):
            row = i // cols
            col = i % cols
            
            # Calculate position
            x = 50 + col * item_width + item_width // 2
            y = 100 + row * item_height + item_height // 2
            
            # Get button coordinates
            x1, y1, x2, y2 = self.canvas.coords(game_id)
            button_width = x2 - x1
            button_height = y2 - y1
            
            # Update button position
            new_x1 = x - button_width/2
            new_y1 = y - button_height/2
            new_x2 = x + button_width/2
            new_y2 = y + button_height/2
            self.canvas.coords(game_id, new_x1, new_y1, new_x2, new_y2)
            
            # Update shadow position
            shadow_id = self.game_shadows[i]
            shadow_width = button_width + 10
            shadow_height = button_height + 10
            self.canvas.coords(shadow_id, 
                              new_x1 - 5, new_y1 - 5, 
                              new_x2 + 5, new_y2 + 5)
            
            # Update icon position
            icon_id = self.game_icons[i]
            self.canvas.coords(icon_id, x, y)
            
            # Update text position
            text_id = self.game_texts[i]
            self.canvas.coords(text_id, x, y + 60)
            
            # Store position for animation
            self.animation_items[game_id] = {'x': x, 'y': y, 'phase': i * 0.5}
    
    def start_floating_animation(self):
        """Start the floating animation for game buttons"""
        self.animation_active = True
        self.animate_floating()
    
    def animate_floating(self):
        """Animate the floating effect for game buttons"""
        if not self.animation_active:
            return
            
        current_time = time.time()
        
        # Animate each game button
        for i, game_id in enumerate(self.game_buttons):
            if game_id in self.animation_items:
                item = self.animation_items[game_id]
                
                # Calculate floating offset using sine wave
                offset_y = math.sin(current_time * 1.5 + item['phase']) * 5
                
                # Get current button coordinates
                x1, y1, x2, y2 = self.canvas.coords(game_id)
                button_width = x2 - x1
                button_height = y2 - y1
                
                # Calculate new position
                x = item['x']
                y = item['y'] + offset_y
                
                # Update button position
                new_x1 = x - button_width/2
                new_y1 = y - button_height/2
                new_x2 = x + button_width/2
                new_y2 = y + button_height/2
                self.canvas.coords(game_id, new_x1, new_y1, new_x2, new_y2)
                
                # Update shadow position
                shadow_id = self.game_shadows[i]
                self.canvas.coords(shadow_id, 
                                  new_x1 - 5, new_y1 - 5, 
                                  new_x2 + 5, new_y2 + 5)
                
                # Update icon position
                icon_id = self.game_icons[i]
                self.canvas.coords(icon_id, x, y)
                
                # Update text position
                text_id = self.game_texts[i]
                self.canvas.coords(text_id, x, y + 60)
        
        # Schedule next animation frame
        self.after(33, self.animate_floating)  # ~30 FPS
    
    def create_widgets(self):
        """Create all UI widgets"""
        # Store IDs of created elements for later repositioning
        self.game_buttons = []
        self.game_shadows = []
        self.game_icons = []
        self.game_texts = []
        
        # Create title with Garamond italic font
        self.title_text = self.canvas.create_text(
            self.winfo_width() // 2, 50,
            text="Offline Games",
            font=("Garamond", 36, "italic"),
            fill="white",
            tags="title"
        )
        
        # Create game buttons
        self.create_game_button("Snake", "snake", 0)
        self.create_game_button("Chess", "chess", 1)
        self.create_game_button("Carrom", "carrom", 2)
        self.create_game_button("Puzzle", "puzzle", 3)
        self.create_game_button("Memory", "cards", 4)
        self.create_game_button("Coming Soon!", "", 5, disabled=True)
        
        # Create footer text with Garamond italic font
        self.footer_text = self.canvas.create_text(
            self.winfo_width() // 2, self.winfo_height() - 25,
            text="© 2025 Q Games Suite | © AWS Limited",
            font=("Garamond", 12, "italic"),
            fill="white",
            tags="footer_text"
        )
    
    def create_game_button(self, game_name, module_name, index, disabled=False):
        """Create a game button on the canvas"""
        # Calculate initial position (will be updated in update_layout)
        x = 100
        y = 100
        
        # Create shadow first (so it's behind the button) - very subtle shadow
        shadow_size = 40
        shadow_id = self.canvas.create_oval(
            x - shadow_size + 5, y - shadow_size + 5,
            x + shadow_size + 5, y + shadow_size + 5,
            fill="#222222", outline="",
            tags=f"shadow_{module_name}"
        )
        self.game_shadows.append(shadow_id)
        
        # Create invisible button area for click detection
        button_size = 50
        button_id = self.canvas.create_oval(
            x - button_size, y - button_size,
            x + button_size, y + button_size,
            fill="", outline="",
            width=0, tags=f"button_{module_name}"
        )
        self.game_buttons.append(button_id)
        
        # Create game icon - larger and more prominent
        icon_text = "🎮"
        if module_name == "snake":
            icon_text = "🐍"
        elif module_name == "chess":
            icon_text = "♟️"
        elif module_name == "carrom":
            icon_text = "🎯"
        elif module_name == "puzzle":
            icon_text = "🧩"
        elif module_name == "cards":
            icon_text = "🃏"
        elif module_name == "":
            icon_text = "🚧"
            
        icon_id = self.canvas.create_text(
            x, y,
            text=icon_text,
            font=("Helvetica", 48),  # Larger font size
            fill="white",
            tags=f"icon_{module_name}"
        )
        self.game_icons.append(icon_id)
        
        # Create game name with Garamond italic font
        text_id = self.canvas.create_text(
            x, y + 60,  # Moved down to accommodate larger icon
            text=game_name,
            font=("Garamond", 16, "italic"),  # Slightly larger font
            fill="white",
            tags=f"text_{module_name}"
        )
        self.game_texts.append(text_id)
        
        # Bind click events if not disabled
        if not disabled:
            self.canvas.tag_bind(button_id, "<Button-1>", lambda e, m=module_name: self.launch_game(m))
            self.canvas.tag_bind(icon_id, "<Button-1>", lambda e, m=module_name: self.launch_game(m))
            self.canvas.tag_bind(text_id, "<Button-1>", lambda e, m=module_name: self.launch_game(m))
            
            # Hover effects
            self.canvas.tag_bind(button_id, "<Enter>", lambda e, b=button_id, i=index: self.on_button_hover(b, i, True))
            self.canvas.tag_bind(button_id, "<Leave>", lambda e, b=button_id, i=index: self.on_button_hover(b, i, False))
            self.canvas.tag_bind(icon_id, "<Enter>", lambda e, b=button_id, i=index: self.on_button_hover(b, i, True))
            self.canvas.tag_bind(icon_id, "<Leave>", lambda e, b=button_id, i=index: self.on_button_hover(b, i, False))
            self.canvas.tag_bind(text_id, "<Enter>", lambda e, b=button_id, i=index: self.on_button_hover(b, i, True))
            self.canvas.tag_bind(text_id, "<Leave>", lambda e, b=button_id, i=index: self.on_button_hover(b, i, False))
    
    def get_icon_color(self, module_name, disabled=False, lighter=False):
        """Get color for game icon based on game type"""
        if disabled:
            return "#555555" if not lighter else "#666666"
            
        colors = {
            "snake": "#4CAF50",  # Green
            "chess": "#9C27B0",  # Purple
            "carrom": "#FF9800",  # Orange
            "puzzle": "#2196F3",  # Blue
            "cards": "#F44336",  # Red
            "": "#607D8B"  # Blue Grey
        }
        
        base_color = colors.get(module_name, "#3F51B5")  # Default to Indigo
        
        if lighter:
            # Make a lighter version of the color for 3D effect
            r = int(base_color[1:3], 16)
            g = int(base_color[3:5], 16)
            b = int(base_color[5:7], 16)
            
            # Lighten the color
            r = min(255, int(r * 1.2))
            g = min(255, int(g * 1.2))
            b = min(255, int(b * 1.2))
            
            return f"#{r:02x}{g:02x}{b:02x}"
        
        return base_color
    
    def on_button_hover(self, button_id, index, is_hover):
        """Handle button hover effect"""
        shadow_id = self.game_shadows[index]
        icon_id = self.game_icons[index]
        text_id = self.game_texts[index]
        
        if is_hover:
            # Make shadow slightly more visible
            self.canvas.itemconfig(shadow_id, fill="#333333")
            
            # Make icon and text glow
            self.canvas.itemconfig(icon_id, font=("Helvetica", 52))
            self.canvas.itemconfig(text_id, fill="#ffffff", font=("Garamond", 18, "italic"))
            
            # Scale up button and shadow (animate)
            self.animate_button_scale(button_id, shadow_id, index, 1.1, 10)
        else:
            # Return to normal
            self.canvas.itemconfig(shadow_id, fill="#222222")
            
            # Return to normal size
            self.canvas.itemconfig(icon_id, font=("Helvetica", 48))
            self.canvas.itemconfig(text_id, fill="#ffffff", font=("Garamond", 16, "italic"))
            
            # Scale down button and shadow (animate)
            self.animate_button_scale(button_id, shadow_id, index, 1.0, 10)
    
    def animate_button_scale(self, button_id, shadow_id, index, target_scale, steps):
        """Animate button scaling for smooth hover effect"""
        # Get current button coordinates
        x1, y1, x2, y2 = self.canvas.coords(button_id)
        current_width = x2 - x1
        current_height = y2 - y1
        
        # Calculate center point
        center_x = (x1 + x2) / 2
        center_y = (y1 + y2) / 2
        
        # Get current shadow coordinates
        sx1, sy1, sx2, sy2 = self.canvas.coords(shadow_id)
        shadow_width = sx2 - sx1
        shadow_height = sy2 - sy1
        
        # Calculate target dimensions
        base_size = 120  # Base button size (diameter)
        target_width = base_size * target_scale
        target_height = base_size * target_scale
        
        shadow_base_size = 130  # Base shadow size (diameter)
        shadow_target_width = shadow_base_size * target_scale
        shadow_target_height = shadow_base_size * target_scale
        
        # Calculate step sizes
        width_step = (target_width - current_width) / steps
        height_step = (target_height - current_height) / steps
        
        shadow_width_step = (shadow_target_width - shadow_width) / steps
        shadow_height_step = (shadow_target_height - shadow_height) / steps
        
        # Perform animation
        self._animate_scale_step(button_id, shadow_id, index, center_x, center_y, 
                               current_width, current_height, shadow_width, shadow_height,
                               width_step, height_step, shadow_width_step, shadow_height_step, 
                               steps, 0)
    
    def _animate_scale_step(self, button_id, shadow_id, index, center_x, center_y, 
                          current_width, current_height, shadow_width, shadow_height,
                          width_step, height_step, shadow_width_step, shadow_height_step, 
                          total_steps, current_step):
        """Execute one step of the scale animation"""
        if current_step >= total_steps:
            return
            
        # Calculate new dimensions
        new_width = current_width + width_step
        new_height = current_height + height_step
        
        new_shadow_width = shadow_width + shadow_width_step
        new_shadow_height = shadow_height + shadow_height_step
        
        # Calculate new coordinates
        new_x1 = center_x - new_width / 2
        new_y1 = center_y - new_height / 2
        new_x2 = center_x + new_width / 2
        new_y2 = center_y + new_height / 2
        
        new_sx1 = center_x - new_shadow_width / 2
        new_sy1 = center_y - new_shadow_height / 2
        new_sx2 = center_x + new_shadow_width / 2
        new_sy2 = center_y + new_shadow_height / 2
        
        # Update button and shadow
        self.canvas.coords(button_id, new_x1, new_y1, new_x2, new_y2)
        self.canvas.coords(shadow_id, new_sx1, new_sy1, new_sx2, new_sy2)
        
        # Update icon and text positions
        icon_id = self.game_icons[index]
        text_id = self.game_texts[index]
        
        self.canvas.coords(icon_id, center_x, center_y)
        self.canvas.coords(text_id, center_x, center_y + 60)
        
        # Schedule next step
        self.after(10, lambda: self._animate_scale_step(
            button_id, shadow_id, index, center_x, center_y,
            new_width, new_height, new_shadow_width, new_shadow_height,
            width_step, height_step, shadow_width_step, shadow_height_step,
            total_steps, current_step + 1
        ))
    
    def launch_game(self, module_name):
        """Launch a game module"""
        if not module_name:
            messagebox.showinfo("Coming Soon", "This game is coming soon! Stay tuned for updates.")
            return
            
        try:
            # Add games directory to path if not already there
            games_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "games")
            if games_dir not in sys.path:
                sys.path.append(games_dir)
            
            # Import the game module
            game_module = importlib.import_module(f"games.{module_name}")
            
            # Hide the main window
            self.withdraw()
            
            # Start the game
            game = game_module.start_game()
            
            # Show the main window again when the game is closed
            self.deiconify()
            
            # Set a new random background when returning
            self.set_random_background()
            
        except ImportError as e:
            print(f"Error importing game module: {e}")
            messagebox.showerror("Game Not Available", f"The {module_name} game is not yet implemented.")
        except Exception as e:
            print(f"Error launching game: {e}")
            messagebox.showerror("Error", f"An error occurred while launching the game: {e}")

if __name__ == "__main__":
    # Create necessary directories if they don't exist
    os.makedirs("assets/icons", exist_ok=True)
    os.makedirs("assets/sounds", exist_ok=True)
    os.makedirs("assets/images", exist_ok=True)
    os.makedirs("assets/backgrounds", exist_ok=True)
    os.makedirs("games", exist_ok=True)
    
    # Check if PIL is installed
    try:
        from PIL import Image, ImageTk
    except ImportError:
        print("PIL/Pillow is required for this application.")
        print("Please install it using: pip install pillow")
        sys.exit(1)
    
    app = GamesSuite()
    app.mainloop()
