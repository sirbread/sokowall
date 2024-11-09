# sokowall

**WINDOWS ONLY. Sorry to my Linux users!** sokowall, to put it very simply, is sokoban, but your desktop wallpaper is the game. 
Uses the Tkinter and Pillow library to generate the game grid and set the wallpaper.

## Instructions

1. **Start the Game:**
   - Simply run `sokowall.py` to start the game.
   - The control window should pop up automatically.
   - Minimize everything (win + d) once you hit run to see the wallpaper, or your game. Then, bring up the tkinter window.
   - **NOTICE:** Your wallpaper **will get overwritten,** so be careful and download a copy of your wallpaper if you want to keep it. 

2. **Gameplay:**
   - Player: Green box
   - Boxes: Blue boxes
   - Targets: Yellow boxes
   - Borders/Walls/Blockades: Gray boxes
   - Use the arrow buttons in the control window to move the chracter (green) OR WASD/arrow keys:
     - **Left Arrow (←)**: Move the character left.
     - **Up Arrow (↑)**: Move the character up.
     - **Down Arrow (↓)**: Move the character down.
     - **Right Arrow (→)**: Move the character right.
   - The game will generate boxes (blue), targets (yellow), and borders (gray, will generate 1 every win) on the grid.

## Requirements
- Python 3.x
- Pillow==9.5.0
- Tkinter

## Known Issues
- After one game is won, the screen doesn't update properly. You must move the character to update to the new layout, although generated border blocks still update normally. (After a win, you will see a new border block, just more the character to get to the new layout)


