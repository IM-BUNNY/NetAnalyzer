"""
Configuration file for Ancient Indian Chess
Customize game settings, visuals, and AI behavior here
"""

# ==================== DISPLAY SETTINGS ====================

# Window dimensions
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
WINDOW_TITLE = "Ancient Indian Chess"

# Graphics quality
ENABLE_MSAA = True  # Multi-sample anti-aliasing (4x)
MSAA_SAMPLES = 4
ENABLE_VSYNC = True  # Vertical sync (limits FPS to monitor refresh rate)

# Target frame rate (if vsync disabled)
TARGET_FPS = 60

# ==================== COLOR SCHEME ====================

# Board colors (RGB, 0-1 range)
# Indian-inspired palette: sandstone and terracotta
COLOR_LIGHT_TILE = (0.95, 0.87, 0.73)  # Light sandstone
COLOR_DARK_TILE = (0.65, 0.45, 0.35)   # Terracotta/clay

# Alternative color schemes (uncomment to use)
# Classic:
# COLOR_LIGHT_TILE = (0.93, 0.93, 0.82)  # Cream
# COLOR_DARK_TILE = (0.55, 0.45, 0.36)   # Brown

# Modern:
# COLOR_LIGHT_TILE = (0.9, 0.9, 0.9)     # Light gray
# COLOR_DARK_TILE = (0.3, 0.3, 0.35)     # Dark gray

# Marble:
# COLOR_LIGHT_TILE = (0.95, 0.95, 0.98)  # White marble
# COLOR_DARK_TILE = (0.15, 0.15, 0.18)   # Black marble

# Piece colors
COLOR_WHITE_PIECE = (0.95, 0.95, 0.9)  # Ivory/bone white
COLOR_BLACK_PIECE = (0.2, 0.15, 0.1)   # Ebony/dark wood

# Highlight colors (RGBA)
COLOR_HIGHLIGHT_LEGAL = (0.3, 0.7, 0.3, 0.5)    # Green - legal moves
COLOR_HIGHLIGHT_SELECT = (0.9, 0.7, 0.2, 0.6)   # Gold - selected piece
COLOR_HIGHLIGHT_HOVER = (0.5, 0.5, 0.8, 0.3)    # Blue - hovered square
COLOR_HIGHLIGHT_LAST = (0.8, 0.5, 0.2, 0.4)     # Orange - last move

# Background
BACKGROUND_COLOR = (0.15, 0.15, 0.2, 1.0)  # Dark blue-gray

# ==================== CAMERA SETTINGS ====================

# Initial camera position
CAMERA_DISTANCE_INITIAL = 15.0     # Distance from board center
CAMERA_ANGLE_H_INITIAL = 45.0      # Horizontal angle (degrees)
CAMERA_ANGLE_V_INITIAL = 30.0      # Vertical angle (degrees)

# Camera limits
CAMERA_DISTANCE_MIN = 8.0          # Minimum zoom
CAMERA_DISTANCE_MAX = 25.0         # Maximum zoom
CAMERA_ANGLE_V_MIN = -89.0         # Don't flip upside down
CAMERA_ANGLE_V_MAX = 89.0

# Camera sensitivity
CAMERA_ROTATE_SENSITIVITY = 0.5    # Mouse rotation speed
CAMERA_ZOOM_SENSITIVITY = 0.5      # Scroll zoom speed

# ==================== LIGHTING SETTINGS ====================

# Light properties (RGBA, 0-1 range)
LIGHT_AMBIENT = (0.3, 0.3, 0.3, 1.0)      # Ambient light (fills shadows)
LIGHT_DIFFUSE = (0.8, 0.8, 0.7, 1.0)      # Diffuse light (main illumination)
LIGHT_SPECULAR = (0.5, 0.5, 0.5, 1.0)     # Specular highlights (shininess)

# Light position (X, Y, Z, W)
# W=1 for positional light, W=0 for directional
LIGHT_POSITION = (5.0, 10.0, 5.0, 1.0)

# Material properties
MATERIAL_SPECULAR = (0.5, 0.5, 0.5, 1.0)
MATERIAL_SHININESS = 32.0  # Higher = sharper highlights (0-128)

# ==================== AI SETTINGS ====================

# AI difficulty (search depth)
AI_DEPTH = 3  # Recommended: 2=Easy, 3=Medium, 4=Hard, 5+=Very Hard/Slow

# Evaluation function weights
AI_WEIGHT_MATERIAL = 1.0     # Piece value importance
AI_WEIGHT_MOBILITY = 0.1     # Number of legal moves
AI_WEIGHT_POSITION = 0.05    # Piece-square table bonus

# AI behavior
AI_ENABLED = True            # Play against AI
AI_PLAYS_AS = 'black'       # 'white' or 'black'
AI_MOVE_DELAY = 0.0         # Seconds to wait before AI moves (0 = instant)

# Performance tuning
AI_USE_ALPHA_BETA = True    # Alpha-beta pruning (faster, same quality)
AI_MAX_NODES = 100000       # Max nodes to search (safety limit)

# ==================== GAME RULES ====================

# Rule variant
USE_CHATURANGA_RULES = False  # True for ancient Indian rules, False for standard chess

# Optional rules (for standard chess)
ENABLE_CASTLING = False       # TODO: Not yet implemented
ENABLE_EN_PASSANT = False     # TODO: Not yet implemented
ENABLE_PAWN_PROMOTION = True  # Auto-promote to Queen

# ==================== ANIMATION SETTINGS ====================

# Piece movement animation
ENABLE_ANIMATION = False      # TODO: Smooth piece movement (not implemented)
ANIMATION_DURATION = 0.3     # Seconds for piece to move
ANIMATION_EASING = 'ease-out'  # 'linear', 'ease-in', 'ease-out', 'ease-in-out'

# ==================== UI SETTINGS ====================

# UI panel transparency (0-1)
UI_PANEL_ALPHA = 0.8

# Text rendering
UI_TEXT_SCALE = 1.0          # Overall text size multiplier

# Display options
SHOW_COORDINATES = False      # Show board coordinates (a-h, 1-8)
SHOW_MOVE_HISTORY = True     # Show list of moves
SHOW_MATERIAL_SCORE = True   # Show material advantage
SHOW_CAPTURED_PIECES = True  # Show captured piece list
SHOW_FPS = False             # Show frame rate

# ==================== SOUND SETTINGS ====================

# Audio (not yet implemented)
ENABLE_SOUND = False
SOUND_VOLUME_MASTER = 0.7
SOUND_VOLUME_MOVE = 0.5
SOUND_VOLUME_CAPTURE = 0.6
SOUND_VOLUME_CHECK = 0.8

# ==================== FILE PATHS ====================

# Save/load
DEFAULT_SAVE_FILE = "savegame.json"
AUTO_SAVE = False            # Auto-save after each move
AUTO_SAVE_FILE = "autosave.json"

# Asset paths (if using external assets)
TEXTURE_PATH = "assets/textures/"
MODEL_PATH = "assets/models/"
SOUND_PATH = "assets/sounds/"

# ==================== DEBUG SETTINGS ====================

# Debug options
DEBUG_MODE = False           # Extra logging and debug info
DEBUG_SHOW_LEGAL_MOVES = False  # Always show legal moves
DEBUG_SHOW_AI_EVAL = True    # Print AI evaluation scores
DEBUG_SHOW_NODES = True      # Print nodes searched

# Performance monitoring
PROFILE_RENDERING = False    # Time rendering operations
PROFILE_AI = False          # Time AI search

# ==================== PIECE MODELS ====================

# Piece geometry detail (number of slices/segments)
PIECE_DETAIL_LOW = 8         # Fast but blocky
PIECE_DETAIL_MEDIUM = 12     # Balanced (default)
PIECE_DETAIL_HIGH = 20       # Smooth but slower

PIECE_DETAIL = PIECE_DETAIL_MEDIUM

# Piece scale factors
PIECE_SCALE_PAWN = 1.0
PIECE_SCALE_ROOK = 1.0
PIECE_SCALE_KNIGHT = 1.0
PIECE_SCALE_BISHOP = 1.0
PIECE_SCALE_QUEEN = 1.0
PIECE_SCALE_KING = 1.0

# ==================== INPUT SETTINGS ====================

# Mouse button bindings
MOUSE_SELECT = 0             # Left button (0)
MOUSE_ROTATE = 1             # Right button (1)
MOUSE_PAN = 2                # Middle button (2)

# Keyboard shortcuts (GLFW key codes)
KEY_UNDO = 85                # U
KEY_REDO = 82                # R
KEY_NEW_GAME = 78            # N
KEY_SAVE = 83                # S
KEY_LOAD = 76                # L
KEY_QUIT = 256               # ESC

# ==================== MULTIPLAYER ====================

# Network play (not yet implemented)
ENABLE_NETWORK = False
NETWORK_PORT = 5555
NETWORK_TIMEOUT = 30.0

# ==================== VALIDATION ====================

def validate_config():
    """Validate configuration values"""
    errors = []
    
    # Check AI depth
    if not (1 <= AI_DEPTH <= 10):
        errors.append(f"AI_DEPTH must be 1-10, got {AI_DEPTH}")
    
    # Check colors are in valid range
    for color_name in ['COLOR_LIGHT_TILE', 'COLOR_DARK_TILE', 
                       'COLOR_WHITE_PIECE', 'COLOR_BLACK_PIECE']:
        color = globals()[color_name]
        if not all(0 <= c <= 1 for c in color):
            errors.append(f"{color_name} values must be 0-1")
    
    # Check camera limits
    if CAMERA_DISTANCE_MIN >= CAMERA_DISTANCE_MAX:
        errors.append("CAMERA_DISTANCE_MIN must be < CAMERA_DISTANCE_MAX")
    
    if errors:
        print("Configuration errors:")
        for error in errors:
            print(f"  - {error}")
        return False
    
    return True

# Validate on import
if __name__ != "__main__":
    if not validate_config():
        print("Warning: Configuration has errors. Using default values.")

# ==================== PRESET CONFIGURATIONS ====================

def load_preset(preset_name):
    """Load a preset configuration"""
    global AI_DEPTH, COLOR_LIGHT_TILE, COLOR_DARK_TILE
    
    presets = {
        'easy': {
            'AI_DEPTH': 2,
            'AI_WEIGHT_MOBILITY': 0.05,
        },
        'hard': {
            'AI_DEPTH': 4,
            'AI_WEIGHT_MOBILITY': 0.15,
        },
        'classic': {
            'COLOR_LIGHT_TILE': (0.93, 0.93, 0.82),
            'COLOR_DARK_TILE': (0.55, 0.45, 0.36),
        },
        'modern': {
            'COLOR_LIGHT_TILE': (0.9, 0.9, 0.9),
            'COLOR_DARK_TILE': (0.3, 0.3, 0.35),
        },
        'performance': {
            'ENABLE_MSAA': False,
            'PIECE_DETAIL': 8,
            'AI_DEPTH': 2,
        },
        'quality': {
            'ENABLE_MSAA': True,
            'PIECE_DETAIL': 20,
            'MATERIAL_SHININESS': 64.0,
        },
    }
    
    if preset_name in presets:
        for key, value in presets[preset_name].items():
            globals()[key] = value
        print(f"Loaded preset: {preset_name}")
    else:
        print(f"Unknown preset: {preset_name}")
        print(f"Available presets: {', '.join(presets.keys())}")

if __name__ == "__main__":
    # Test configuration
    print("Configuration Test")
    print("=" * 50)
    print(f"AI Depth: {AI_DEPTH}")
    print(f"Window Size: {WINDOW_WIDTH}x{WINDOW_HEIGHT}")
    print(f"MSAA Enabled: {ENABLE_MSAA}")
    print(f"Piece Detail: {PIECE_DETAIL} slices")
    print(f"Use Chaturanga Rules: {USE_CHATURANGA_RULES}")
    print("=" * 50)
    
    if validate_config():
        print("✓ Configuration is valid")
    else:
        print("✗ Configuration has errors")
