"""
3D Renderer using OpenGL
Handles board, pieces, lighting, and camera
"""

import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *
import math

class Renderer:
    """OpenGL 3D renderer for chess game"""
    
    def __init__(self, width, height):
        self.width = width
        self.height = height
        
        # Colors (Indian-inspired palette)
        self.color_light_tile = (0.95, 0.87, 0.73)  # Sandstone
        self.color_dark_tile = (0.65, 0.45, 0.35)   # Terracotta
        self.color_white_piece = (0.95, 0.95, 0.9)  # Ivory
        self.color_black_piece = (0.2, 0.15, 0.1)   # Ebony
        self.color_highlight = (0.3, 0.7, 0.3, 0.5)  # Green highlight
        self.color_select = (0.9, 0.7, 0.2, 0.6)    # Golden select
        self.color_hover = (0.5, 0.5, 0.8, 0.3)     # Blue hover
        
        self.setup_opengl()
    
    def setup_opengl(self):
        """Initialize OpenGL settings"""
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glEnable(GL_MULTISAMPLE)
        
        # Simple shading without legacy lighting
        glShadeModel(GL_SMOOTH)
        glEnable(GL_COLOR_MATERIAL)
        
        # Background color
        glClearColor(0.15, 0.15, 0.2, 1.0)
    
    def resize(self, width, height):
        """Handle window resize"""
        self.width = width
        self.height = height
        glViewport(0, 0, width, height)
    
    def setup_camera(self, distance, angle_h, angle_v):
        """Setup camera view"""
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, self.width / max(self.height, 1), 0.1, 100.0)
        
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        
        # Calculate camera position from spherical coordinates
        angle_h_rad = math.radians(angle_h)
        angle_v_rad = math.radians(angle_v)
        
        cam_x = distance * math.cos(angle_v_rad) * math.sin(angle_h_rad)
        cam_y = distance * math.sin(angle_v_rad)
        cam_z = distance * math.cos(angle_v_rad) * math.cos(angle_h_rad)
        
        gluLookAt(cam_x, cam_y, cam_z,  # Camera position
                  0, 0, 0,                # Look at center
                  0, 1, 0)                # Up vector
    
    def apply_simple_lighting(self, base_color, normal=(0, 1, 0)):
        """Apply simple directional lighting simulation"""
        # Simple lighting direction from top-right
        light_dir = np.array([0.5, 0.8, 0.3])
        light_dir = light_dir / np.linalg.norm(light_dir)
        
        # Calculate simple diffuse lighting
        normal_vec = np.array(normal)
        normal_vec = normal_vec / np.linalg.norm(normal_vec)
        
        diffuse = max(0.0, np.dot(normal_vec, light_dir))
        
        # Ambient + diffuse
        ambient = 0.4
        lighting_factor = ambient + (1.0 - ambient) * diffuse
        
        # Apply to color
        lit_color = tuple(min(1.0, c * lighting_factor) for c in base_color[:3])
        
        if len(base_color) > 3:
            return lit_color + (base_color[3],)
        return lit_color
    
    def render(self, engine, distance, angle_h, angle_v, 
               selected_square, legal_moves, hovered_square):
        """Render the complete scene"""
        self.setup_camera(distance, angle_h, angle_v)
        
        # Render board
        self.render_board(selected_square, legal_moves, hovered_square, engine.last_move)
        
        # Render pieces
        self.render_pieces(engine.board)
    
    def render_board(self, selected, legal_moves, hovered, last_move):
        """Render the chess board"""
        glPushMatrix()
        glTranslatef(-3.5, -0.5, -3.5)
        
        for row in range(8):
            for col in range(8):
                glPushMatrix()
                glTranslatef(col, 0, row)
                
                # Determine tile color
                is_light = (row + col) % 2 == 0
                base_color = self.color_light_tile if is_light else self.color_dark_tile
                
                # Highlight selected square
                if selected and selected == (row, col):
                    self.draw_tile(self.color_select, 0.05)
                # Highlight legal move squares
                elif (row, col) in legal_moves:
                    self.draw_tile(self.color_highlight, 0.03)
                # Highlight hovered square
                elif hovered and hovered == (row, col):
                    self.draw_tile(self.color_hover, 0.02)
                # Highlight last move
                elif last_move and (row, col) in last_move:
                    highlight = list(base_color) + [0.8]
                    self.draw_tile(highlight, 0.01)
                    self.draw_tile(base_color, 0.0)
                else:
                    self.draw_tile(base_color, 0.0)
                
                glPopMatrix()
        
        glPopMatrix()
    
    def draw_tile(self, color, height):
        """Draw a single board tile"""
        # Apply lighting to color
        lit_color = self.apply_simple_lighting(color, normal=(0, 1, 0))
        glColor4f(*lit_color) if len(color) > 3 else glColor3f(*lit_color)
        
        glBegin(GL_QUADS)
        glVertex3f(0, height, 0)
        glVertex3f(1, height, 0)
        glVertex3f(1, height, 1)
        glVertex3f(0, height, 1)
        glEnd()
        
        # Add small border for depth
        if height == 0:
            dark_color = (color[0] * 0.7, color[1] * 0.7, color[2] * 0.7)
            glColor3f(*dark_color)
            glBegin(GL_QUADS)
            # Front
            glVertex3f(0, -0.1, 1)
            glVertex3f(1, -0.1, 1)
            glVertex3f(1, 0, 1)
            glVertex3f(0, 0, 1)
            # Back
            glVertex3f(0, 0, 0)
            glVertex3f(1, 0, 0)
            glVertex3f(1, -0.1, 0)
            glVertex3f(0, -0.1, 0)
            # Left
            glVertex3f(0, 0, 0)
            glVertex3f(0, -0.1, 0)
            glVertex3f(0, -0.1, 1)
            glVertex3f(0, 0, 1)
            # Right
            glVertex3f(1, 0, 1)
            glVertex3f(1, -0.1, 1)
            glVertex3f(1, -0.1, 0)
            glVertex3f(1, 0, 0)
            glEnd()
    
    def render_pieces(self, board):
        """Render all chess pieces"""
        glPushMatrix()
        glTranslatef(-3.5, 0, -3.5)
        
        for row in range(8):
            for col in range(8):
                piece = board[row][col]
                if piece:
                    glPushMatrix()
                    glTranslatef(col + 0.5, 0, row + 0.5)
                    
                    color = self.color_white_piece if piece.color == 'white' else self.color_black_piece
                    self.draw_piece(piece, color)
                    
                    glPopMatrix()
        
        glPopMatrix()
    
    def draw_piece(self, piece, color):
        """Draw a single piece with distinctive shape"""
        # Apply lighting to piece color
        lit_color = self.apply_simple_lighting(color)
        glColor3f(*lit_color)
        
        from engine import Padati, Ratha, Ashva, Gaja, Mantri, Raja
        
        if isinstance(piece, Padati):
            # Pawn: Small sphere on cylinder
            self.draw_cylinder(0.15, 0.4, 12)
            glTranslatef(0, 0.4, 0)
            self.draw_sphere(0.2, 12, 12)
        
        elif isinstance(piece, Ratha):
            # Rook: Castle tower
            self.draw_cylinder(0.25, 0.6, 12)
            glTranslatef(0, 0.6, 0)
            self.draw_cylinder(0.3, 0.2, 12)
            glTranslatef(0, 0.2, 0)
            # Crenellations
            for angle in range(0, 360, 90):
                glPushMatrix()
                glRotatef(angle, 0, 1, 0)
                glTranslatef(0.25, 0, 0)
                self.draw_cube(0.1, 0.15, 0.1)
                glPopMatrix()
        
        elif isinstance(piece, Ashva):
            # Knight: Horse head approximation
            self.draw_cylinder(0.2, 0.3, 12)
            glTranslatef(0, 0.3, 0)
            glRotatef(45, 1, 0, 0)
            self.draw_cylinder(0.15, 0.4, 12)
            glTranslatef(0, 0.4, 0)
            self.draw_sphere(0.18, 12, 12)
        
        elif isinstance(piece, Gaja):
            # Bishop: Pointed hat
            self.draw_cylinder(0.22, 0.4, 12)
            glTranslatef(0, 0.4, 0)
            self.draw_cone(0.25, 0.5, 12)
            glTranslatef(0, 0.5, 0)
            self.draw_sphere(0.1, 8, 8)
        
        elif isinstance(piece, Mantri):
            # Queen: Crown with spikes
            self.draw_cylinder(0.25, 0.5, 12)
            glTranslatef(0, 0.5, 0)
            self.draw_cylinder(0.28, 0.15, 12)
            glTranslatef(0, 0.15, 0)
            # Crown spikes
            for angle in range(0, 360, 45):
                glPushMatrix()
                glRotatef(angle, 0, 1, 0)
                glTranslatef(0.25, 0, 0)
                self.draw_cone(0.08, 0.3, 8)
                glPopMatrix()
        
        elif isinstance(piece, Raja):
            # King: Cross on top
            self.draw_cylinder(0.27, 0.5, 12)
            glTranslatef(0, 0.5, 0)
            self.draw_cylinder(0.3, 0.1, 12)
            glTranslatef(0, 0.1, 0)
            self.draw_sphere(0.25, 12, 12)
            glTranslatef(0, 0.25, 0)
            # Cross
            self.draw_cube(0.05, 0.25, 0.05)
            glTranslatef(0, 0.1, 0)
            self.draw_cube(0.2, 0.05, 0.05)
    
    def draw_sphere(self, radius, slices, stacks):
        """Draw a sphere using GLU"""
        quad = gluNewQuadric()
        gluSphere(quad, radius, slices, stacks)
        gluDeleteQuadric(quad)
    
    def draw_cylinder(self, radius, height, slices):
        """Draw a cylinder"""
        quad = gluNewQuadric()
        gluCylinder(quad, radius, radius, height, slices, 1)
        gluDeleteQuadric(quad)
    
    def draw_cone(self, radius, height, slices):
        """Draw a cone"""
        quad = gluNewQuadric()
        gluCylinder(quad, radius, 0, height, slices, 1)
        gluDeleteQuadric(quad)
    
    def draw_cube(self, width, height, depth):
        """Draw a cube"""
        glPushMatrix()
        glScalef(width, height, depth)
        glTranslatef(-0.5, 0, -0.5)
        
        glBegin(GL_QUADS)
        # Front
        glVertex3f(0, 0, 1)
        glVertex3f(1, 0, 1)
        glVertex3f(1, 1, 1)
        glVertex3f(0, 1, 1)
        # Back
        glVertex3f(0, 1, 0)
        glVertex3f(1, 1, 0)
        glVertex3f(1, 0, 0)
        glVertex3f(0, 0, 0)
        # Top
        glVertex3f(0, 1, 0)
        glVertex3f(0, 1, 1)
        glVertex3f(1, 1, 1)
        glVertex3f(1, 1, 0)
        # Bottom
        glVertex3f(0, 0, 0)
        glVertex3f(1, 0, 0)
        glVertex3f(1, 0, 1)
        glVertex3f(0, 0, 1)
        # Left
        glVertex3f(0, 0, 0)
        glVertex3f(0, 0, 1)
        glVertex3f(0, 1, 1)
        glVertex3f(0, 1, 0)
        # Right
        glVertex3f(1, 0, 1)
        glVertex3f(1, 0, 0)
        glVertex3f(1, 1, 0)
        glVertex3f(1, 1, 1)
        glEnd()
        
        glPopMatrix()
    
    def pick_square(self, mouse_x, mouse_y, distance, angle_h, angle_v):
        """Convert mouse coordinates to board square using ray casting"""
        # Convert mouse coords to normalized device coordinates
        x_ndc = (2.0 * mouse_x) / self.width - 1.0
        y_ndc = 1.0 - (2.0 * mouse_y) / self.height
        
        # Get projection and view matrices
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, self.width / max(self.height, 1), 0.1, 100.0)
        proj_matrix = glGetDoublev(GL_PROJECTION_MATRIX)
        
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        angle_h_rad = math.radians(angle_h)
        angle_v_rad = math.radians(angle_v)
        cam_x = distance * math.cos(angle_v_rad) * math.sin(angle_h_rad)
        cam_y = distance * math.sin(angle_v_rad)
        cam_z = distance * math.cos(angle_v_rad) * math.cos(angle_h_rad)
        gluLookAt(cam_x, cam_y, cam_z, 0, 0, 0, 0, 1, 0)
        view_matrix = glGetDoublev(GL_MODELVIEW_MATRIX)
        
        # Unproject to get ray
        viewport = glGetIntegerv(GL_VIEWPORT)
        
        try:
            near = gluUnProject(mouse_x, self.height - mouse_y, 0.0, 
                               view_matrix, proj_matrix, viewport)
            far = gluUnProject(mouse_x, self.height - mouse_y, 1.0,
                              view_matrix, proj_matrix, viewport)
            
            # Ray direction
            ray_dir = np.array([far[0] - near[0], far[1] - near[1], far[2] - near[2]])
            ray_dir = ray_dir / np.linalg.norm(ray_dir)
            ray_origin = np.array(near)
            
            # Intersect with y=0 plane
            if abs(ray_dir[1]) > 0.001:
                t = -ray_origin[1] / ray_dir[1]
                if t > 0:
                    intersect = ray_origin + t * ray_dir
                    
                    # Convert to board coordinates
                    board_x = intersect[0] + 3.5
                    board_z = intersect[2] + 3.5
                    
                    col = int(board_x)
                    row = int(board_z)
                    
                    if 0 <= row < 8 and 0 <= col < 8:
                        return (row, col)
        except:
            pass
        
        return None