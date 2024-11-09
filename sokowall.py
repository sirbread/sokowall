import os
import ctypes
import tkinter as tk
from PIL import Image, ImageDraw
from random import randint, sample

DISPLAY_WIDTH = 1920
DISPLAY_HEIGHT = 1040
WALLPAPER_PATH = os.path.join(os.path.expanduser('~'), 'Pictures', 'sokoban_wallpaper.png')

GRID_COLUMNS, GRID_ROWS = 8, 8  
GRID_SIZE = min(DISPLAY_WIDTH // GRID_COLUMNS, DISPLAY_HEIGHT // GRID_ROWS)
GRID_START_X = (DISPLAY_WIDTH - (GRID_COLUMNS * GRID_SIZE)) // 2
GRID_START_Y = (DISPLAY_HEIGHT - (GRID_ROWS * GRID_SIZE)) // 2

DIRECTION_MAP = {'up': (0, -1), 'down': (0, 1), 'left': (-1, 0), 'right': (1, 0)}

class SokobanGame:
    def __init__(self):
        self.win_count = 0  
        self.blocks_to_add = 0  
        self.walls = self.generate_walls()  
        self.targets, self.boxes, self.player = self.generate_level()  
        self.running = True

    def generate_walls(self):
        return [(0, i) for i in range(GRID_ROWS)] + [(GRID_COLUMNS - 1, i) for i in range(GRID_ROWS)] + \
               [(i, 0) for i in range(GRID_COLUMNS)] + [(i, GRID_ROWS - 1) for i in range(GRID_COLUMNS)]

    def check_win(self):
        if all(box in self.targets for box in self.boxes):
            self.win_count += 1  
            print(f"Congratulations! You've completed the level! Total Wins: {self.win_count}")
            self.blocks_to_add = self.win_count  
            self.refresh_level()

    def refresh_level(self):
        self.walls = self.generate_walls()  
        self.add_random_walls(self.blocks_to_add)  
        self.blocks_to_add += 1  
        self.targets, self.boxes, self.player = self.generate_level()  
        self.draw()

    def draw(self):
        image = Image.new('RGB', (DISPLAY_WIDTH, DISPLAY_HEIGHT), (0, 0, 0))
        draw = ImageDraw.Draw(image)

        for wx, wy in self.walls:
            top_left = (GRID_START_X + wx * GRID_SIZE, GRID_START_Y + wy * GRID_SIZE)
            bottom_right = (top_left[0] + GRID_SIZE, top_left[1] + GRID_SIZE)
            draw.rectangle([top_left, bottom_right], fill=(128, 128, 128))  

        for tx, ty in self.targets:
            top_left = (GRID_START_X + tx * GRID_SIZE, GRID_START_Y + ty * GRID_SIZE)
            bottom_right = (top_left[0] + GRID_SIZE, top_left[1] + GRID_SIZE)
            draw.rectangle([top_left, bottom_right], fill=(255, 255, 0))  

        for bx, by in self.boxes:
            top_left = (GRID_START_X + bx * GRID_SIZE, GRID_START_Y + by * GRID_SIZE)
            bottom_right = (top_left[0] + GRID_SIZE, top_left[1] + GRID_SIZE)
            draw.rectangle([top_left, bottom_right], fill=(0, 0, 255))  

        px, py = self.player
        top_left = (GRID_START_X + px * GRID_SIZE, GRID_START_Y + py * GRID_SIZE)
        bottom_right = (top_left[0] + GRID_SIZE, top_left[1] + GRID_SIZE)
        draw.rectangle([top_left, bottom_right], fill=(0, 255, 0))  

        wallpaper_path = os.path.join(os.path.expanduser('~'), 'Pictures', 'sokoban_wallpaper.png')
        image.save(wallpaper_path, format='PNG')
        self.set_wallpaper(wallpaper_path)

    def set_wallpaper(self, path):
        if os.name == 'nt':
            ctypes.windll.user32.SystemParametersInfoW(20, 0, path, 0)

    def get_adjacent_positions(self):
        adjacent_positions = set()
        for wx, wy in self.walls:
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                x, y = wx + dx, wy + dy
                if 0 <= x < GRID_COLUMNS and 0 <= y < GRID_ROWS and (x, y) not in self.walls:
                    adjacent_positions.add((x, y))
        return adjacent_positions

    def generate_level(self):
        open_positions = [(x, y) for x in range(1, GRID_COLUMNS - 1) for y in range(1, GRID_ROWS - 1)
                          if (x, y) not in self.walls]

        adjacent_positions_for_targets = self.get_adjacent_positions()

        open_positions_for_boxes = [(x, y) for x, y in open_positions if 1 < x < GRID_COLUMNS - 2 and 1 < y < GRID_ROWS - 2]

        valid_adjacent_for_targets = list(adjacent_positions_for_targets)
        targets = sample(valid_adjacent_for_targets, 2)

        valid_open_positions_for_boxes = [pos for pos in open_positions_for_boxes if pos not in targets]
        boxes = sample(valid_open_positions_for_boxes, 2)

        player = sample([pos for pos in open_positions_for_boxes if pos not in targets and pos not in boxes], 1)[0]

        return targets, boxes, player

    def move(self, direction):
        if not self.running:
            return

        dx, dy = DIRECTION_MAP[direction]
        px, py = self.player
        new_player = (px + dx, py + dy)

        if new_player in self.walls:
            return

        if new_player in self.boxes:
            new_box = (new_player[0] + dx, new_player[1] + dy)

            if new_box in self.walls or new_box in self.boxes:
                return

            self.boxes.remove(new_player)
            self.boxes.append(new_box)

        self.player = new_player
        self.check_win()
        self.draw()

    def add_random_walls(self, num_blocks):
        for _ in range(num_blocks):
            empty_spaces = [(x, y) for x in range(1, GRID_COLUMNS - 1) for y in range(1, GRID_ROWS - 1)
                            if (x, y) not in self.walls and (x, y) not in self.boxes and (x, y) not in self.targets]

            if empty_spaces:
                new_wall = sample(empty_spaces, 1)[0]
                self.walls.append(new_wall)
                print(f"New wall placed at {new_wall}")

        self.draw()

    def redo(self):
        """Redo the level by regenerating positions."""
        self.targets, self.boxes, self.player = self.generate_level()
        self.draw()

def create_controls():
    root = tk.Tk()
    root.title("Sokoban Game")

    game = SokobanGame()

    controls = tk.Frame(root, padx=20, pady=20)
    controls.pack(side=tk.LEFT)

    button_style = {
        'width': 5,
        'height': 2,
        'font': ('Arial', 14, 'bold')
    }

    up_button = tk.Button(controls, text="↑", command=lambda: game.move("up"), **button_style)
    left_button = tk.Button(controls, text="←", command=lambda: game.move("left"), **button_style)
    right_button = tk.Button(controls, text="→", command=lambda: game.move("right"), **button_style)
    down_button = tk.Button(controls, text="↓", command=lambda: game.move("down"), **button_style)
    redo_button = tk.Button(controls, text="↺", command=game.redo, **button_style) 

    up_button.grid(row=0, column=1, pady=5)
    left_button.grid(row=1, column=0, padx=5)
    redo_button.grid(row=1, column=1)  
    right_button.grid(row=1, column=2, padx=5)
    down_button.grid(row=2, column=1, pady=5)

    def handle_keypress(event):
        key_mappings = {
            'Up': 'up',
            'Down': 'down',
            'Left': 'left',
            'Right': 'right',
            'w': 'up',
            's': 'down',
            'a': 'left',
            'd': 'right'
        }
        if event.keysym in key_mappings:
            game.move(key_mappings[event.keysym])

    root.bind('<KeyPress>', handle_keypress)

    game.draw()

    root.mainloop()

if __name__ == "__main__":
    create_controls()
