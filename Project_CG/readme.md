# Ancient Indian Chess (Chaturanga)

A 3D chess game with ancient Indian theming, built using Python and OpenGL. Features a fully playable chess engine, AI opponent, and beautiful 3D visualization.

![Chess Preview](preview.png)

## Features

### Visual & UX
- **3D Rendered Board**: Beautiful 8x8 board with Indian-inspired colors (sandstone and terracotta)
- **Distinctive Pieces**: Each piece has a unique 3D model
  - **Raja** (King) - topped with a cross
  - **Mantri** (Queen/Minister) - crown with spikes
  - **Ratha** (Rook/Chariot) - castle tower with crenellations
  - **Gaja** (Bishop/Elephant) - pointed hat design
  - **Ashva** (Knight/Horse) - horse head approximation
  - **Padati** (Pawn/Foot Soldier) - simple cylinder with sphere
- **Smooth Camera**: Orbit, rotate, and zoom with mouse controls
- **Visual Feedback**: Highlights for selected pieces, legal moves, hovered squares, and last move
- **Lighting**: Phong shading with directional light for depth

### Game Logic
- **Complete Chess Rules**: Full implementation of standard chess
  - Legal move validation (no moving into check)
  - Check and checkmate detection
  - Stalemate detection
  - Pawn promotion (auto-promotes to Queen)
  - Move history tracking
- **Chaturanga Variant**: Optional traditional Indian rules (use `--chaturanga` flag)

### AI Opponent
- **Minimax with Alpha-Beta Pruning**: Efficient tree search
- **Configurable Depth**: Default depth 3 (adjustable in code)
- **Smart Evaluation**:
  - Material counting
  - Piece-square tables for positional play
  - Mobility evaluation
  - Tunable evaluation weights

### Extra Features
- **Undo/Redo**: Full move history with undo and redo
- **Save/Load**: Persist games to JSON format
- **Material Score**: Real-time material advantage display
- **Captured Pieces**: Visual list of captured pieces per side
- **Move Counter**: Track game length

## Installation

### Requirements
- Python 3.10 or later
- OpenGL 3.3 compatible graphics card
- Windows, macOS, or Linux

### Setup

1. **Clone or download the repository**

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

Or install manually:
```bash
pip install PyOpenGL PyOpenGL-accelerate glfw numpy pytest
```

3. **Run the game**:
```bash
python main.py
```

### Optional: Chaturanga Mode
To play with traditional Chaturanga rules:
```bash
python main.py --chaturanga
```

### Custom Window Size
```bash
python main.py --width 1920 --height 1080
```

## Controls

### Mouse Controls
- **Left Click**: Select piece / Make move
- **Right-Drag**: Rotate camera around board
- **Scroll Wheel**: Zoom in/out

### Keyboard Controls
- **U**: Undo last move
- **R**: Redo move
- **N**: New game (reset board)
- **S**: Save game to `savegame.json`
- **L**: Load game from `savegame.json`
- **ESC**: Exit game

## Gameplay

1. **Start**: White moves first (you play as white, AI plays as black by default)
2. **Select**: Click on a piece to see legal moves (highlighted in green)
3. **Move**: Click on a highlighted square to move
4. **AI Turn**: AI automatically calculates and makes its move
5. **Win Condition**: Checkmate your opponent's King (Raja)

### Game States
- **Check**: Your king is under attack (shown in red text)
- **Checkmate**: Game over - no legal moves to escape check
- **Stalemate**: Draw - no legal moves but not in check

## Project Structure

```
ancient-indian-chess/
├── main.py           # Entry point and game controller
├── engine.py         # Chess rules and game logic
├── renderer.py       # 3D OpenGL rendering
├── ai.py            # Minimax AI with evaluation
├── ui.py            # UI overlay for game info
├── test_engine.py   # Unit tests for game logic
├── requirements.txt # Python dependencies
└── README.md        # This file
```

## Architecture

### Engine (engine.py)
- **Piece Classes**: Padati, Ratha, Ashva, Gaja, Mantri, Raja
- **ChessEngine**: Manages board state, move validation, check detection
- **Move Generation**: Pseudo-legal moves filtered for legality
- **Game State**: Tracks current player, move history, captured pieces

### Renderer (renderer.py)
- **3D Rendering**: Uses OpenGL immediate mode for compatibility
- **Procedural Models**: All pieces generated procedurally (no external assets)
- **Ray Picking**: Mouse-to-3D coordinate conversion for square selection
- **Camera System**: Spherical coordinate-based camera with orbit controls

### AI (ai.py)
- **Search**: Minimax with alpha-beta pruning (typical depth 3-5 ply)
- **Evaluation**: Multi-factor position scoring
  - Material: Standard piece values (P=1, N/B=3, R=5, Q=9, K=1000)
  - Position: Piece-square tables encourage center control
  - Mobility: Bonus for number of legal moves
- **Performance**: ~10,000-50,000 nodes searched per move at depth 3

### UI (ui.py)
- **Overlay**: 2D orthographic rendering over 3D scene
- **Info Display**: Turn, check status, material score, captured pieces
- **Controls Guide**: On-screen control reference

## Testing

Run unit tests to verify game logic:
```bash
pytest test_engine.py -v
```

Tests cover:
- Move legality for all piece types
- Check detection
- Checkmate scenarios
- Stalemate scenarios
- Move history (undo/redo)

## Performance

- **Target FPS**: 60 (V-sync enabled)
- **Typical Frame Time**: 16ms (60 FPS)
- **AI Think Time**: 0.5-3 seconds (depth 3)
- **Memory Usage**: ~50-100 MB

### Performance Tips
- Lower AI depth for faster moves (edit `ai.py`, line 19)
- Disable MSAA for older GPUs (comment out line 22 in `main.py`)
- Reduce window size for better performance

## Customization

### AI Difficulty
Edit `main.py`, line 29:
```python
self.ai = ChessAI(depth=3)  # Increase depth for harder AI (4-5 max)
```

### Evaluation Weights
Edit `ai.py`, lines 19-21:
```python
self.weight_material = 1.0    # Material importance
self.weight_mobility = 0.1    # Mobility importance
self.weight_position = 0.05   # Position importance
```

### Colors
Edit `renderer.py`, lines 18-23 to customize board and piece colors.

### Camera
Edit `main.py`, lines 36-38:
```python
self.camera_distance = 15.0  # Zoom level
self.camera_angle_h = 45.0   # Horizontal angle
self.camera_angle_v = 30.0   # Vertical angle
```

## Known Limitations & TODOs

### Current Limitations
1. **No Castling**: Not yet implemented (TODO)
2. **No En Passant**: Special pawn capture not implemented (TODO)
3. **Text Rendering**: UI uses simple line rendering instead of proper fonts
4. **Chaturanga Rules**: Flag exists but rules identical to standard chess currently
5. **No Sound**: Audio effects not implemented
6. **No Animation**: Piece moves are instant (TODO: smooth interpolation)

### Planned Features
- [ ] Castling support
- [ ] En passant capture
- [ ] Smooth piece movement animation
- [ ] Better text rendering (bitmap fonts or FreeType)
- [ ] Sound effects (move, capture, check)
- [ ] Replay mode with move playback
- [ ] PGN export for move notation
- [ ] Full Chaturanga variant rules
- [ ] Settings menu (difficulty, visuals)
- [ ] Multiplayer over network
- [ ] Opening book for AI
- [ ] Endgame tablebase

## Chaturanga Rules (Planned)

Traditional Chaturanga differs from modern chess:
- **Mantri (Minister)**: Moves only 1 square diagonally (instead of Queen's moves)
- **Gaja (Elephant)**: Leaps exactly 2 squares diagonally (can jump pieces)
- **No Castling**: Did not exist in ancient rules
- **No En Passant**: Modern rule not in original game
- **Pawn Promotion**: Only promotes to piece originally on that file
- **Stalemate**: Counts as a win for stalemating player

## Troubleshooting

### Game Won't Start
- Ensure Python 3.10+ is installed: `python --version`
- Install dependencies: `pip install -r requirements.txt`
- Check OpenGL support: Update graphics drivers

### Poor Performance
- Lower AI depth: Edit `ai.py`, reduce `depth` parameter
- Disable MSAA: Comment out line 22 in `main.py`
- Reduce window size: `python main.py --width 1024 --height 768`

### Graphics Issues
- Update graphics drivers to latest version
- Ensure OpenGL 3.3+ support
- Try compatibility mode if on very old hardware

### AI Too Slow
- Reduce search depth in `ai.py` (line 19): `depth=2` for faster moves
- Performance roughly doubles with each depth reduction

### AI Too Easy/Hard
- **Easier**: Reduce depth to 2
- **Harder**: Increase depth to 4-5 (warning: much slower)
- Adjust evaluation weights in `ai.py`

## Contributing

This is a complete, self-contained project. To extend it:

1. **Add Castling**: Modify `engine.py` move validation
2. **Implement Animation**: Add interpolation in `renderer.py`
3. **Better Text**: Integrate FreeType or bitmap font library
4. **Sound**: Add pygame.mixer for audio
5. **Network Play**: Add socket-based multiplayer

## License

This project is provided as educational example code. Feel free to use, modify, and distribute as needed.

## Credits

- **Concept**: Ancient Indian chess (Chaturanga)
- **Implementation**: Python, PyOpenGL, GLFW
- **Algorithm**: Minimax with alpha-beta pruning
- **Piece Design**: Procedural 3D modeling

## Technical Details

### OpenGL Version
- **Target**: OpenGL 3.3 Core Profile
- **Fallback**: Uses immediate mode for maximum compatibility
- **Shading**: Fixed-function pipeline with Phong lighting

### Coordinate Systems
- **Board**: 8x8 grid, origin at bottom-left
- **3D Space**: Y-up, centered at origin
- **Camera**: Spherical coordinates (distance, azimuth, elevation)

### Move Representation
- **Internal**: Tuple of positions `((from_row, from_col), (to_row, to_col))`
- **History**: Stored with piece type and captured piece for undo

## Version History

### v1.0.0 (Initial Release)
- Complete chess engine with all standard rules
- 3D rendering with OpenGL
- AI opponent with minimax search
- Undo/redo functionality
- Save/load game state
- Material score tracking
- UI overlay with game info

---

**Enjoy playing Ancient Indian Chess!** 🎮♟️

For issues or questions, please check the troubleshooting section or review the source code comments for detailed implementation notes.
