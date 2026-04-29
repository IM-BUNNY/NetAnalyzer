"""
Ancient Indian Chess (Chaturanga) - Main Entry Point
A 3D chess game with Indian theming using OpenGL
"""

import sys
import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

from engine import ChessEngine
from renderer import Renderer
from ui import UI
from ai import ChessAI

class ChessGame:
    """Main game controller that coordinates all subsystems"""
    
    def __init__(self, width=1280, height=720, use_chaturanga=False):
        self.width = width
        self.height = height
        self.use_chaturanga = use_chaturanga
        
        # Initialize GLFW
        if not glfw.init():
            sys.exit(1)
        
        # Window hints for OpenGL 3.3 core profile
        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
        glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL_TRUE)
        glfw.window_hint(glfw.SAMPLES, 4)  # 4x MSAA
        
        # Create window
        self.window = glfw.create_window(width, height, "Ancient Indian Chess", None, None)
        if not self.window:
            glfw.terminate()
            sys.exit(1)
        
        glfw.make_context_current(self.window)
        glfw.swap_interval(1)  # V-sync
        
        # Initialize subsystems
        self.engine = ChessEngine(use_chaturanga=use_chaturanga)
        self.renderer = Renderer(width, height)
        self.ui = UI(width, height)
        self.ai = ChessAI(depth=3)
        
        # Game state
        self.selected_square = None
        self.legal_moves = []
        self.hovered_square = None
        self.animating = False
        self.animation_start = None
        self.animation_duration = 0.3
        self.ai_thinking = False
        self.play_against_ai = True
        
        # Camera state
        self.camera_distance = 15.0
        self.camera_angle_h = 45.0
        self.camera_angle_v = 30.0
        self.camera_dragging = False
        self.last_mouse_pos = (0, 0)
        
        # Setup callbacks
        self.setup_callbacks()
        
        print("Ancient Indian Chess initialized")
        print(f"Mode: {'Chaturanga' if use_chaturanga else 'Standard Chess'}")
        print("Controls:")
        print("  Mouse: Click to select/move pieces")
        print("  Right-drag: Rotate camera")
        print("  Scroll: Zoom")
        print("  U: Undo move")
        print("  R: Redo move")
        print("  N: New game")
        print("  S: Save game")
        print("  L: Load game")
        print("  ESC: Exit")
    
    def setup_callbacks(self):
        """Setup GLFW input callbacks"""
        glfw.set_mouse_button_callback(self.window, self.mouse_button_callback)
        glfw.set_cursor_pos_callback(self.window, self.mouse_move_callback)
        glfw.set_scroll_callback(self.window, self.scroll_callback)
        glfw.set_key_callback(self.window, self.key_callback)
        glfw.set_framebuffer_size_callback(self.window, self.resize_callback)
    
    def mouse_button_callback(self, window, button, action, mods):
        """Handle mouse button events"""
        if button == glfw.MOUSE_BUTTON_RIGHT:
            if action == glfw.PRESS:
                self.camera_dragging = True
                self.last_mouse_pos = glfw.get_cursor_pos(window)
            elif action == glfw.RELEASE:
                self.camera_dragging = False
        
        elif button == glfw.MOUSE_BUTTON_LEFT and action == glfw.PRESS:
            if self.animating or self.ai_thinking:
                return
            
            x, y = glfw.get_cursor_pos(window)
            square = self.renderer.pick_square(x, y, self.camera_distance, 
                                               self.camera_angle_h, self.camera_angle_v)
            
            if square:
                self.handle_square_click(square)
    
    def mouse_move_callback(self, window, xpos, ypos):
        """Handle mouse movement"""
        if self.camera_dragging:
            dx = xpos - self.last_mouse_pos[0]
            dy = ypos - self.last_mouse_pos[1]
            self.camera_angle_h += dx * 0.5
            self.camera_angle_v = max(-89, min(89, self.camera_angle_v - dy * 0.5))
            self.last_mouse_pos = (xpos, ypos)
        else:
            # Update hovered square for highlighting
            square = self.renderer.pick_square(xpos, ypos, self.camera_distance,
                                               self.camera_angle_h, self.camera_angle_v)
            self.hovered_square = square
    
    def scroll_callback(self, window, xoffset, yoffset):
        """Handle mouse scroll for zoom"""
        self.camera_distance = max(8, min(25, self.camera_distance - yoffset * 0.5))
    
    def key_callback(self, window, key, scancode, action, mods):
        """Handle keyboard input"""
        if action != glfw.PRESS:
            return
        
        if key == glfw.KEY_ESCAPE:
            glfw.set_window_should_close(window, True)
        elif key == glfw.KEY_U:
            self.engine.undo_move()
            self.selected_square = None
            self.legal_moves = []
        elif key == glfw.KEY_R:
            self.engine.redo_move()
        elif key == glfw.KEY_N:
            self.engine.reset()
            self.selected_square = None
            self.legal_moves = []
        elif key == glfw.KEY_S:
            self.engine.save_game("savegame.json")
            print("Game saved to savegame.json")
        elif key == glfw.KEY_L:
            if self.engine.load_game("savegame.json"):
                print("Game loaded from savegame.json")
                self.selected_square = None
                self.legal_moves = []
    
    def resize_callback(self, window, width, height):
        """Handle window resize"""
        self.width = width
        self.height = height
        self.renderer.resize(width, height)
        self.ui.resize(width, height)
    
    def handle_square_click(self, square):
        """Process square selection/move"""
        row, col = square
        piece = self.engine.board[row][col]
        
        # If a piece is selected, try to move
        if self.selected_square:
            move = (self.selected_square, square)
            if move in self.legal_moves:
                # Execute move with animation
                self.engine.make_move(move)
                self.selected_square = None
                self.legal_moves = []
                
                # Check for game over
                if self.engine.is_checkmate():
                    winner = "Black" if self.engine.current_player == 'white' else "White"
                    print(f"Checkmate! {winner} wins!")
                elif self.engine.is_stalemate():
                    print("Stalemate! Game is a draw.")
                
                # AI move if playing against AI
                if self.play_against_ai and not self.engine.is_game_over():
                    self.ai_thinking = True
            else:
                # Invalid move, reselect or deselect
                if piece and piece.color == self.engine.current_player:
                    self.selected_square = square
                    self.legal_moves = self.engine.get_legal_moves(square)
                else:
                    self.selected_square = None
                    self.legal_moves = []
        else:
            # Select piece if it belongs to current player
            if piece and piece.color == self.engine.current_player:
                self.selected_square = square
                self.legal_moves = self.engine.get_legal_moves(square)
    
    def update_ai(self):
        """Process AI move"""
        if self.ai_thinking:
            move = self.ai.get_best_move(self.engine)
            if move:
                self.engine.make_move(move)
                
                if self.engine.is_checkmate():
                    winner = "Black" if self.engine.current_player == 'white' else "White"
                    print(f"Checkmate! {winner} wins!")
                elif self.engine.is_stalemate():
                    print("Stalemate! Game is a draw.")
            
            self.ai_thinking = False
    
    def run(self):
        """Main game loop"""
        while not glfw.window_should_close(self.window):
            # Update AI if needed
            self.update_ai()
            
            # Clear screen
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            
            # Render 3D scene
            self.renderer.render(
                self.engine,
                self.camera_distance,
                self.camera_angle_h,
                self.camera_angle_v,
                self.selected_square,
                self.legal_moves,
                self.hovered_square
            )
            
            # Render UI overlay
            self.ui.render(self.engine, self.ai_thinking)
            
            # Swap buffers and poll events
            glfw.swap_buffers(self.window)
            glfw.poll_events()
        
        self.cleanup()
    
    def cleanup(self):
        """Clean up resources"""
        glfw.terminate()

def main():
    """Entry point"""
    import argparse
    parser = argparse.ArgumentParser(description="Ancient Indian Chess Game")
    parser.add_argument('--chaturanga', action='store_true', 
                       help='Use Chaturanga rules instead of standard chess')
    parser.add_argument('--width', type=int, default=1280, help='Window width')
    parser.add_argument('--height', type=int, default=720, help='Window height')
    args = parser.parse_args()
    
    game = ChessGame(width=args.width, height=args.height, 
                    use_chaturanga=args.chaturanga)
    game.run()

if __name__ == "__main__":
    main()
