# Quick Start Guide

Get up and running with Ancient Indian Chess in under 5 minutes!

## 1. Prerequisites Check

Ensure you have Python 3.10 or later:
```bash
python --version
```

If you need to install Python, download from [python.org](https://www.python.org/downloads/)

## 2. Installation

### Option A: Quick Install (Recommended)
```bash
# Clone or download the project
cd ancient-indian-chess

# Install dependencies
pip install -r requirements.txt

# Run the game
python main.py
```

### Option B: Virtual Environment (Cleaner)
```bash
# Create virtual environment
python -m venv venv

# Activate it
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the game
python main.py
```

### Option C: Install as Package
```bash
pip install -e .
indian-chess
```

## 3. First Game

Once the game window opens:

1. **Select a piece**: Click on any white piece
   - Legal moves will highlight in **green**
   - Selected piece shows **golden** highlight

2. **Make a move**: Click on a green square
   - Piece moves automatically
   - AI (black) will think and respond

3. **Camera controls**: 
   - Right-click and drag to rotate
   - Scroll to zoom in/out

4. **Game info**: Check top panels for:
   - Current turn
   - Material score
   - Captured pieces

## 4. Basic Controls Reference

| Action | Control |
|--------|---------|
| Select/Move | Left Click |
| Rotate Camera | Right-drag |
| Zoom | Mouse Wheel |
| Undo | U key |
| Redo | R key |
| New Game | N key |
| Save Game | S key |
| Load Game | L key |
| Quit | ESC key |

## 5. Common First-Time Issues

### Game won't start?
```bash
# Check OpenGL support
python -c "import OpenGL; print('OpenGL OK')"

# If that fails, update your graphics drivers
```

### Graphics look weird?
- Update your graphics drivers
- Try running with lower resolution:
  ```bash
  python main.py --width 1024 --height 768
  ```

### AI too slow?
The AI is thinking! At depth 3, it searches 10,000-50,000 positions per move.
- To speed up: Edit `ai.py`, line 19, change `depth=3` to `depth=2`

### AI too easy?
- To make harder: Edit `ai.py`, line 19, change `depth=3` to `depth=4`
- Warning: Depth 4 is much slower (5-15 seconds per move)

## 6. Your First Strategies

### Opening Principles
1. **Control the center**: Move pawns to e4/d4
2. **Develop pieces**: Get Knights and Bishops out
3. **Protect the King**: Keep Raja safe

### Piece Values (for captures)
- **Padati** (Pawn): 1 point
- **Ashva** (Knight): 3 points
- **Gaja** (Bishop): 3 points
- **Ratha** (Rook): 5 points
- **Mantri** (Queen): 9 points
- **Raja** (King): Priceless!

### Watch For
- **Check**: Your king is under attack (red warning)
- **Discovered attacks**: Moving one piece exposes another's attack
- **Pins**: Can't move a piece without exposing your king

## 7. Testing Your Installation

Run the test suite to verify everything works:
```bash
pytest test_engine.py -v
```

Expected output:
```
test_engine.py::TestChessEngine::test_initial_board_setup PASSED
test_engine.py::TestChessEngine::test_pawn_moves PASSED
test_engine.py::TestChessEngine::test_rook_moves PASSED
... (more tests)

====== 17 passed in 0.5s ======
```

## 8. Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Try Chaturanga mode: `python main.py --chaturanga`
- Customize AI difficulty in `ai.py`
- Check out the source code to understand the implementation

## 9. Getting Help

If you encounter issues:

1. Check the [Troubleshooting section](README.md#troubleshooting) in README
2. Verify your Python version: `python --version` (need 3.10+)
3. Update packages: `pip install --upgrade -r requirements.txt`
4. Check graphics drivers are up to date

## 10. Enjoy!

You're all set! Start playing and enjoy this beautiful blend of ancient Indian chess heritage and modern 3D graphics.

**Pro tip**: Press `U` frequently to undo and try different moves - it's a great way to learn!

---

**Need more help?** See the full [README.md](README.md) for comprehensive documentation.
