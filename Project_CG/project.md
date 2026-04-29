# Ancient Indian Chess - Complete Project Structure

## 📁 Project Files Overview

```
ancient-indian-chess/
│
├── main.py                 # Main entry point and game controller (500 lines)
├── engine.py               # Chess game logic and rules (650 lines)
├── renderer.py             # 3D OpenGL rendering system (450 lines)
├── ai.py                   # Minimax AI with evaluation (350 lines)
├── ui.py                   # UI overlay and information display (200 lines)
├── config.py               # Centralized configuration (350 lines)
│
├── test_engine.py          # Pytest unit tests (400 lines)
├── requirements.txt        # Python dependencies
├── setup.py                # Package installation script
│
├── README.md               # Complete documentation (500 lines)
├── QUICKSTART.md           # Quick start guide
└── PROJECT_STRUCTURE.md    # This file
```

**Total Code: ~2,900 lines** of well-documented Python

---

## 🎯 Core Components

### 1. main.py - Game Controller
**Purpose**: Orchestrates all subsystems and handles game loop

**Key Classes**:
- `ChessGame`: Main game controller
  - Window management (GLFW)
  - Input handling (mouse, keyboard)
  - Camera controls
  - Game state coordination
  - AI move execution

**Key Features**:
- Command-line argument parsing
- Camera system (orbit, rotate, zoom)
- Mouse picking (ray casting)
- Square selection and move execution
- Save/load game state

**Dependencies**: `glfw`, `OpenGL`, `engine`, `renderer`, `ai`, `ui`

---

### 2. engine.py - Chess Logic
**Purpose**: Implements complete chess rules and game state

**Key Classes**:
- `Piece`: Base class for all pieces
- `Padati` (Pawn): Foot soldier
- `Ratha` (Rook): Chariot
- `Ashva` (Knight): Horse
- `Gaja` (Bishop): Elephant
- `Mantri` (Queen): Minister/Advisor
- `Raja` (King): King
- `ChessEngine`: Game state manager

**Key Features**:
- Move generation (pseudo-legal + legal filtering)
- Check/checkmate/stalemate detection
- Move validation (prevents moving into check)
- Pawn promotion
- Move history (undo/redo)
- Captured piece tracking
- Material score calculation
- Save/load to JSON

**Algorithm Highlights**:
- Legal move filtering prevents self-check
- Temporary move execution for validation
- Board state cloning for safety

**Dependencies**: `json`, `copy`

---

### 3. renderer.py - 3D Graphics
**Purpose**: Renders chess board and pieces using OpenGL

**Key Classes**:
- `Renderer`: Main rendering system

**Key Features**:
- **Board Rendering**:
  - Alternating tile colors
  - Highlight overlays (selected, legal, hover, last move)
  - Depth and borders for visual appeal
  
- **Piece Rendering**:
  - Procedural 3D models (no external assets)
  - Distinctive shapes for each piece type
  - Color differentiation (white/black)
  
- **Lighting System**:
  - Phong shading model
  - Directional light
  - Ambient, diffuse, specular components
  
- **Camera System**:
  - Spherical coordinates (distance, azimuth, elevation)
  - Perspective projection
  - Mouse picking with ray casting

**Rendering Pipeline**:
1. Setup camera (view + projection matrices)
2. Render board with highlights
3. Render all pieces at positions
4. Apply lighting calculations

**Technical Details**:
- Uses OpenGL immediate mode (compatibility)
- GLU quadrics for spheres, cylinders, cones
- Manual quad/cube rendering
- Ray-plane intersection for picking

**Dependencies**: `OpenGL`, `numpy`, `math`

---

### 4. ai.py - Artificial Intelligence
**Purpose**: Provides computer opponent using minimax search

**Key Classes**:
- `ChessAI`: AI opponent

**Key Features**:
- **Search Algorithm**:
  - Minimax with alpha-beta pruning
  - Configurable depth (default 3)
  - Move ordering (random for variety)
  - Node counting for performance metrics
  
- **Evaluation Function**:
  - Material counting (weighted)
  - Piece-square tables (positional bonuses)
  - Mobility evaluation (legal move count)
  - Tunable weights
  
- **Piece-Square Tables**:
  - Encourages center control
  - Rewards piece development
  - King safety (different for middlegame)
  - Separate tables per piece type

**Performance**:
- Depth 2: ~1,000 nodes, <0.1s
- Depth 3: ~10,000 nodes, 0.5-2s
- Depth 4: ~100,000 nodes, 5-15s
- Depth 5: ~1,000,000 nodes, 1-5min

**Algorithm Complexity**:
- Time: O(b^d) where b=branching factor (~30-35), d=depth
- Space: O(d) for recursion stack
- Alpha-beta pruning reduces effective branching significantly

**Dependencies**: `engine`, `random`

---

### 5. ui.py - User Interface
**Purpose**: Displays game information as 2D overlay

**Key Classes**:
- `UI`: UI overlay renderer

**Key Features**:
- Semi-transparent panels
- Game state display:
  - Current turn
  - Check warning
  - AI thinking indicator
  - Material score
  - Move count
- Captured pieces list (per side)
- Control hints
- Simple stroke text rendering

**Rendering**:
- Switches to orthographic 2D projection
- Disables depth testing and lighting
- Renders over 3D scene
- Restores 3D state after

**Note**: Text rendering is simplified (production would use bitmap fonts or FreeType)

**Dependencies**: `OpenGL`, `glfw`

---

### 6. config.py - Configuration
**Purpose**: Centralized configuration for easy customization

**Configuration Categories**:

1. **Display Settings**:
   - Window size, MSAA, V-sync, FPS target

2. **Color Scheme**:
   - Board colors (with presets)
   - Piece colors
   - Highlight colors
   - Background

3. **Camera Settings**:
   - Initial position
   - Zoom/angle limits
   - Sensitivity controls

4. **Lighting**:
   - Light properties (ambient, diffuse, specular)
   - Light position
   - Material properties

5. **AI Settings**:
   - Search depth
   - Evaluation weights
   - Behavior options

6. **Game Rules**:
   - Rule variant selection
   - Optional rules (castling, en passant)

7. **Animation** (TODO):
   - Duration, easing

8. **UI**:
   - Panel transparency
   - Display toggles

9. **Paths**:
   - Save files, assets (future)

**Special Features**:
- Configuration validation
- Preset loading (easy, hard, classic, modern, etc.)
- Test mode for verification

---

### 7. test_engine.py - Unit Tests
**Purpose**: Comprehensive test suite for game logic

**Test Classes**:
- `TestChessEngine`: Engine functionality tests
- `TestPieces`: Individual piece movement tests

**Test Coverage**:
1. **Board Setup**: Initial position correctness
2. **Move Generation**: Pawn, rook, knight moves
3. **Check Detection**: Is king under attack?
4. **Checkmate Detection**: No legal moves + in check
5. **Stalemate Detection**: No legal moves + not in check
6. **Move Execution**: Piece movement and state updates
7. **Captures**: Piece capture and tracking
8. **Undo/Redo**: Move history functionality
9. **Pawn Promotion**: Auto-promotion to queen
10. **Pinned Pieces**: Legal moves respect pins
11. **Material Score**: Correct score calculation
12. **Individual Pieces**: Each piece type's moves

**Running Tests**:
```bash
pytest test_engine.py -v
```

**Dependencies**: `pytest`, `engine`

---

## 🔄 Data Flow

### Game Loop Flow
```
main.py (ChessGame.run)
    ↓
1. Update AI (if AI's turn)
    ↓
2. Clear screen
    ↓
3. Render 3D scene (renderer.py)
    ↓
4. Render UI overlay (ui.py)
    ↓
5. Swap buffers, poll events
    ↓
Loop back to 1
```

### Move Execution Flow
```
User clicks square
    ↓
main.py: Mouse callback
    ↓
renderer.py: Pick square (ray cast)
    ↓
main.py: Handle square click
    ↓
engine.py: Get legal moves
    ↓
User clicks legal move
    ↓
engine.py: Make move
    ↓
Check for checkmate/stalemate
    ↓
If AI turn:
    ai.py: Get best move (minimax)
    ↓
    engine.py: Make AI move
```

### AI Decision Flow
```
ai.py: get_best_move
    ↓
Generate all legal moves
    ↓
For each move:
    Make move temporarily
    ↓
    minimax (depth-1, -beta, -alpha)
        ↓
        [Recursively search move tree]
        ↓
        evaluate(position)
            ↓
            Material + Position + Mobility
    ↓
    Undo temporary move
    ↓
    Update best move if score improved
    ↓
Return best move found
```

---

## 🎨 Rendering Pipeline

### 3D Rendering Steps
```
1. Setup Projection Matrix
   - Perspective with FOV=45°
   - Aspect ratio from window size
   
2. Setup View Matrix
   - Camera position (spherical coords)
   - Look at board center
   - Up vector (0, 1, 0)
   
3. Render Board
   For each tile:
     - Calculate position
     - Determine base color
     - Apply highlights if needed
     - Render tile quad + borders
   
4. Render Pieces
   For each piece:
     - Translate to position
     - Set color (white/black)
     - Draw piece model
       (cylinder, sphere, cone, cube primitives)
   
5. Render UI (2D overlay)
   - Switch to orthographic projection
   - Disable depth test
   - Render panels and text
   - Restore 3D state
```

---

## 🧮 Key Algorithms

### 1. Ray Picking (Mouse → Board Square)
```python
# Convert mouse to NDC
x_ndc = (2 * mouse_x) / width - 1
y_ndc = 1 - (2 * mouse_y) / height

# Unproject near and far points
near_point = unproject(mouse_x, mouse_y, 0.0)
far_point = unproject(mouse_x, mouse_y, 1.0)

# Calculate ray
ray_dir = normalize(far - near)
ray_origin = near

# Intersect with y=0 plane
t = -ray_origin.y / ray_dir.y
intersect = ray_origin + t * ray_dir

# Convert to board coords
col = int(intersect.x + 3.5)
row = int(intersect.z + 3.5)
```

### 2. Legal Move Generation
```python
def get_legal_moves(position):
    piece = board[position]
    pseudo_legal = piece.get_moves(board)
    
    legal = []
    for move in pseudo_legal:
        # Make move temporarily
        make_temp_move(move)
        
        # Check if king is in check
        if not is_in_check(piece.color):
            legal.append(move)
        
        # Undo temp move
        undo_temp_move(move)
    
    return legal
```

### 3. Minimax with Alpha-Beta
```python
def minimax(depth, alpha, beta, maximizing):
    if depth == 0:
        return evaluate(position)
    
    if maximizing:
        max_eval = -infinity
        for move in legal_moves:
            make_move(move)
            eval = minimax(depth-1, alpha, beta, False)
            undo_move(move)
            
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break  # Beta cutoff
        return max_eval
    else:
        # Minimizing player (similar)
```

### 4. Evaluation Function
```python
def evaluate(position):
    score = 0
    
    # Material
    for piece in all_pieces:
        value = piece.value
        position_bonus = piece_square_table[piece.pos]
        
        if piece.color == AI_COLOR:
            score += value + position_bonus
        else:
            score -= value + position_bonus
    
    # Mobility
    ai_moves = count_legal_moves(AI_COLOR)
    player_moves = count_legal_moves(PLAYER_COLOR)
    score += (ai_moves - player_moves) * MOBILITY_WEIGHT
    
    return score
```

---

## 🔧 Extension Points

### Adding New Features

1. **Castling**:
   - Modify `Raja.get_moves()` to check castling conditions
   - Verify king and rook haven't moved
   - Check squares between are empty and not under attack
   - Execute as two-piece move

2. **En Passant**:
   - Track last move in engine
   - Check if last move was two-square pawn advance
   - Allow diagonal capture of passing pawn
   - Remove captured pawn after move

3. **Animation**:
   - Add `AnimationSystem` class
   - Interpolate piece positions over time
   - Use easing functions for smooth motion
   - Block input during animation

4. **Sound**:
   - Add `pygame.mixer` for audio
   - Load sound files (move.wav, capture.wav, check.wav)
   - Play sounds on corresponding events
   - Volume controls in config

5. **Network Play**:
   - Add socket-based communication
   - Serialize moves as JSON
   - Handle turn synchronization
   - Add connection UI

6. **Opening Book**:
   - Load common opening moves from file
   - Search book before minimax
   - Return book move if found
   - Improves early game play

---

## 📊 Performance Characteristics

### Rendering Performance
- **Target**: 60 FPS (16.7ms per frame)
- **Typical**: 100-300 FPS (3-10ms per frame)
- **Bottlenecks**:
  - Piece complexity (slices/stacks)
  - MSAA overhead
  - UI rendering (text)

### AI Performance
| Depth | Nodes | Time | Strength |
|-------|-------|------|----------|
| 1 | ~35 | <0.01s | Beginner |
| 2 | ~1,000 | 0.05s | Easy |
| 3 | ~30,000 | 1s | Medium |
| 4 | ~1M | 10s | Hard |
| 5 | ~30M | 5min | Expert |

### Memory Usage
- **Base**: ~50 MB (Python runtime)
- **Board**: ~1 KB (64 piece references)
- **History**: ~100 bytes per move
- **Textures**: 0 (procedural rendering)
- **Total**: 50-100 MB typical

---

## 🐛 Known Issues & TODOs

### Critical TODOs
- [ ] Implement castling
- [ ] Implement en passant
- [ ] Add move animation
- [ ] Improve text rendering

### Enhancement TODOs
- [ ] Add sound effects
- [ ] Implement replay mode
- [ ] Add move notation (algebraic)
- [ ] Export to PGN format
- [ ] Full Chaturanga rules
- [ ] Settings menu UI
- [ ] Time controls (chess clock)
- [ ] Hints system
- [ ] Puzzle mode

### Performance TODOs
- [ ] Use VBOs for board rendering
- [ ] Shader-based rendering
- [ ] Frustum culling (minor gain)
- [ ] AI iterative deepening
- [ ] AI transposition table
- [ ] AI move ordering heuristics

---

## 📚 Code Style & Conventions

### Python Style
- Follows PEP 8
- 4-space indentation
- Max line length: 100 chars
- Docstrings for all classes/functions

### Naming Conventions
- Classes: `PascalCase`
- Functions: `snake_case`
- Constants: `UPPER_SNAKE_CASE`
- Private: `_leading_underscore`

### Comments
- Function docstrings explain purpose, parameters, returns
- Inline comments for complex algorithms
- Section headers for code organization

---

## 🎓 Learning Resources

### Understanding the Code

**Start here**:
1. Read `QUICKSTART.md`
2. Run the game and explore
3. Read `main.py` - see how pieces fit together
4. Read `engine.py` - understand chess logic
5. Experiment with `config.py` settings

**Deep dives**:
- **3D Graphics**: Study `renderer.py`, learn OpenGL
- **AI**: Study `ai.py`, learn minimax algorithm
- **Chess**: Study `engine.py`, learn chess rules

### External Resources
- **OpenGL**: learnopengl.com
- **Chess AI**: chessprogramming.org
- **Minimax**: Wikipedia, Stanford CS course notes
- **Python**: python.org documentation

---

## 🤝 Contributing Guidelines

### How to Contribute

1. **Bug Fixes**:
   - Test the fix thoroughly
   - Add test case if applicable
   - Update comments if needed

2. **New Features**:
   - Discuss design first (comment/issue)
   - Follow existing code style
   - Add tests for new functionality
   - Update README with feature docs

3. **Performance**:
   - Profile before optimizing
   - Benchmark improvements
   - Don't sacrifice readability

### Code Review Checklist
- [ ] Code follows style guide
- [ ] Functions have docstrings
- [ ] Complex logic has comments
- [ ] Tests pass (`pytest test_engine.py`)
- [ ] No new warnings/errors
- [ ] README updated if needed

---

## 📄 License & Credits

### License
Educational/example code - free to use, modify, distribute

### Credits
- **Concept**: Ancient Indian chess (Chaturanga)
- **Implementation**: Python + PyOpenGL + GLFW
- **Algorithms**: Minimax, alpha-beta, piece-square tables
- **Design**: Procedural 3D modeling

### Inspiration
- Traditional Chaturanga game
- Modern chess engines (Stockfish, etc.)
- 3D chess visualizations

---

**Happy coding! ♟️**

This project demonstrates:
- Game engine architecture
- 3D graphics programming
- AI search algorithms
- Software engineering best practices

Feel free to use this as a learning resource or starting point for your own chess game!
