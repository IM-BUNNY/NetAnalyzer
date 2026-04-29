"""
UI overlay for displaying game information
Uses OpenGL immediate mode for simple text rendering
"""

from OpenGL.GL import *
from OpenGL.GLU import *
import glfw

class UI:
    """Simple UI overlay for game info"""
    
    def __init__(self, width, height):
        self.width = width
        self.height = height
    
    def resize(self, width, height):
        """Handle window resize"""
        self.width = width
        self.height = height
    
    def render(self, engine, ai_thinking):
        """Render UI overlay"""
        # Switch to 2D orthographic projection
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        glOrtho(0, self.width, self.height, 0, -1, 1)
        
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()
        
        # Disable depth test and lighting for UI
        glDisable(GL_DEPTH_TEST)
        glDisable(GL_LIGHTING)
        
        # Semi-transparent background panels
        self.draw_panel(10, 10, 300, 150, (0.1, 0.1, 0.15, 0.8))
        self.draw_panel(self.width - 310, 10, 300, 200, (0.1, 0.1, 0.15, 0.8))
        
        # Game info
        y_offset = 30
        self.draw_text(f"Turn: {engine.current_player.capitalize()}", 20, y_offset)
        y_offset += 25
        
        if engine.is_in_check(engine.current_player):
            self.draw_text("CHECK!", 20, y_offset, color=(1, 0.3, 0.3))
            y_offset += 25
        
        if ai_thinking:
            self.draw_text("AI Thinking...", 20, y_offset, color=(0.3, 0.8, 1))
            y_offset += 25
        
        # Material score
        material = engine.get_material_score()
        self.draw_text(f"Material: {'+' if material >= 0 else ''}{material}", 
                      20, y_offset)
        y_offset += 25
        
        self.draw_text(f"Moves: {len(engine.move_history)}", 20, y_offset)
        
        # Captured pieces
        y_offset = 30
        self.draw_text("Captured by White:", self.width - 290, y_offset)
        y_offset += 25
        
        captured_str = ""
        for piece in engine.captured_pieces['white']:
            captured_str += piece.symbol + " "
            if len(captured_str) > 25:
                self.draw_text(captured_str, self.width - 290, y_offset)
                y_offset += 20
                captured_str = ""
        if captured_str:
            self.draw_text(captured_str, self.width - 290, y_offset)
            y_offset += 25
        
        y_offset += 10
        self.draw_text("Captured by Black:", self.width - 290, y_offset)
        y_offset += 25
        
        captured_str = ""
        for piece in engine.captured_pieces['black']:
            captured_str += piece.symbol + " "
            if len(captured_str) > 25:
                self.draw_text(captured_str, self.width - 290, y_offset)
                y_offset += 20
                captured_str = ""
        if captured_str:
            self.draw_text(captured_str, self.width - 290, y_offset)
        
        # Controls hint at bottom
        self.draw_panel(10, self.height - 130, 400, 120, (0.1, 0.1, 0.15, 0.8))
        y_offset = self.height - 110
        self.draw_text("Controls:", 20, y_offset, scale=0.8)
        y_offset += 20
        self.draw_text("Click: Select/Move", 20, y_offset, scale=0.7)
        y_offset += 18
        self.draw_text("Right-drag: Rotate camera", 20, y_offset, scale=0.7)
        y_offset += 18
        self.draw_text("Scroll: Zoom", 20, y_offset, scale=0.7)
        y_offset += 18
        self.draw_text("U: Undo  R: Redo  N: New game", 20, y_offset, scale=0.7)
        
        # Restore 3D state
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHTING)
        
        glPopMatrix()
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)
    
    def draw_panel(self, x, y, width, height, color):
        """Draw a colored panel"""
        glColor4f(*color)
        glBegin(GL_QUADS)
        glVertex2f(x, y)
        glVertex2f(x + width, y)
        glVertex2f(x + width, y + height)
        glVertex2f(x, y + height)
        glEnd()
        
        # Border
        glColor3f(0.3, 0.3, 0.4)
        glLineWidth(2)
        glBegin(GL_LINE_LOOP)
        glVertex2f(x, y)
        glVertex2f(x + width, y)
        glVertex2f(x + width, y + height)
        glVertex2f(x, y + height)
        glEnd()
    
    def draw_text(self, text, x, y, color=(1, 1, 1), scale=1.0):
        """Draw text using simple line rendering"""
        # Note: This is a simplified version. For production, use bitmap fonts
        # or FreeType. Here we just show the text position with a dot.
        glColor3f(*color)
        glPointSize(4 * scale)
        glBegin(GL_POINTS)
        glVertex2f(x, y)
        glEnd()
        
        # Draw actual text (simplified - just positions for now)
        # In a real implementation, you'd render each character
        char_width = 8 * scale
        char_x = x
        
        for char in text:
            # Skip actual character rendering for simplicity
            # In production, use GLUT fonts or texture-based fonts
            char_x += char_width
        
        # For now, render text using simple stroke lines
        self.render_stroke_text(text, x, y, scale, color)
    
    def render_stroke_text(self, text, x, y, scale, color):
        """Render text using simple stroke lines (very basic)"""
        glColor3f(*color)
        glLineWidth(1.5)
        
        char_width = 10 * scale
        char_height = 15 * scale
        
        for i, char in enumerate(text):
            cx = x + i * char_width
            cy = y
            
            # Very simplified character rendering
            # Just render a few basic shapes for common characters
            if char.isalpha() or char.isdigit():
                glBegin(GL_LINE_LOOP)
                glVertex2f(cx, cy)
                glVertex2f(cx + char_width * 0.7, cy)
                glVertex2f(cx + char_width * 0.7, cy + char_height)
                glVertex2f(cx, cy + char_height)
                glEnd()
            elif char == ':':
                glBegin(GL_POINTS)
                glVertex2f(cx + char_width * 0.3, cy + char_height * 0.3)
                glVertex2f(cx + char_width * 0.3, cy + char_height * 0.7)
                glEnd()
            elif char == '+':
                glBegin(GL_LINES)
                glVertex2f(cx, cy + char_height * 0.5)
                glVertex2f(cx + char_width * 0.6, cy + char_height * 0.5)
                glVertex2f(cx + char_width * 0.3, cy + char_height * 0.2)
                glVertex2f(cx + char_width * 0.3, cy + char_height * 0.8)
                glEnd()
            elif char == '-':
                glBegin(GL_LINES)
                glVertex2f(cx, cy + char_height * 0.5)
                glVertex2f(cx + char_width * 0.6, cy + char_height * 0.5)
                glEnd()
            elif char == '!':
                glBegin(GL_LINES)
                glVertex2f(cx + char_width * 0.3, cy)
                glVertex2f(cx + char_width * 0.3, cy + char_height * 0.6)
                glEnd()
                glBegin(GL_POINTS)
                glVertex2f(cx + char_width * 0.3, cy + char_height * 0.8)
                glEnd()
