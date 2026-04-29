# Installation Guide - Ancient Indian Chess

Complete installation instructions for all platforms.

## 📋 Prerequisites

### System Requirements

**Minimum**:
- Python 3.10 or later
- OpenGL 3.3 compatible GPU
- 2 GB RAM
- 50 MB disk space

**Recommended**:
- Python 3.11+
- Modern GPU (2015 or newer)
- 4 GB RAM
- Dedicated graphics card

### Supported Platforms
- ✅ Windows 10/11
- ✅ macOS 10.15+
- ✅ Linux (Ubuntu 20.04+, Fedora 35+, etc.)

---

## 🪟 Windows Installation

### Method 1: Quick Install (Recommended)

1. **Install Python**:
   - Download from [python.org](https://www.python.org/downloads/)
   - ✅ Check "Add Python to PATH" during installation
   - Verify: `python --version` in Command Prompt

2. **Download Project**:
   ```cmd
   git clone https://github.com/yourusername/ancient-indian-chess.git
   cd ancient-indian-chess
   ```
   
   Or download ZIP and extract

3. **Install Dependencies**:
   ```cmd
   pip install -r requirements.txt
   ```

4. **Run Game**:
   ```cmd
   python main.py
   ```

### Method 2: Virtual Environment (Cleaner)

```cmd
# Create virtual environment
python -m venv venv

# Activate it
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run game
python main.py

# When done, deactivate
deactivate
```

### Windows Troubleshooting

**Problem**: `'python' is not recognized`
- **Solution**: Reinstall Python with "Add to PATH" checked
- Or add manually: System Properties → Environment Variables → Path

**Problem**: OpenGL errors
- **Solution**: Update graphics drivers
  - NVIDIA: geforce.com/drivers
  - AMD: amd.com/support
  - Intel: intel.com/content/www/us/en/download-center

**Problem**: pip install fails
- **Solution**: Upgrade pip first:
  ```cmd
  python -m pip install --upgrade pip
  ```

---

## 🍎 macOS Installation

### Method 1: Using Homebrew (Recommended)

1. **Install Homebrew** (if not installed):
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```

2. **Install Python**:
   ```bash
   brew install python@3.11
   ```

3. **Download Project**:
   ```bash
   git clone https://github.com/yourusername/ancient-indian-chess.git
   cd ancient-indian-chess
   ```

4. **Install Dependencies**:
   ```bash
   pip3 install -r requirements.txt
   ```

5. **Run Game**:
   ```bash
   python3 main.py
   ```

### Method 2: Using System Python

1. **Check Python Version**:
   ```bash
   python3 --version
   ```
   (Must be 3.10+)

2. **Create Virtual Environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

3. **Run Game**:
   ```bash
   python main.py
   ```

### macOS Troubleshooting

**Problem**: Permission denied
- **Solution**: Don't use `sudo`. Use virtual environment instead.

**Problem**: "command not found: python3"
- **Solution**: Install Python via Homebrew or python.org

**Problem**: GLFW window doesn't appear
- **Solution**: macOS requires OpenGL forward compatibility:
  - Already handled in code (line 17 of main.py)
  - If still issues, update macOS

**Problem**: Retina display issues
- **Solution**: Scale detection is automatic, but you can force resolution:
  ```bash
  python main.py --width 2560 --height 1440
  ```

---

## 🐧 Linux Installation

### Ubuntu/Debian

```bash
# Update package lists
sudo apt update

# Install Python and dependencies
sudo apt install python3 python3-pip python3-venv

# Install OpenGL libraries
sudo apt install freeglut3-dev libglfw3-dev

# Download project
git clone https://github.com/yourusername/ancient-indian-chess.git
cd ancient-indian-chess

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Python packages
pip install -r requirements.txt

# Run game
python main.py
```

### Fedora/RHEL

```bash
# Install dependencies
sudo dnf install python3 python3-pip freeglut-devel glfw-devel

# Rest same as Ubuntu
git clone https://github.com/yourusername/ancient-indian-chess.git
cd ancient-indian-chess
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
```

### Arch Linux

```bash
# Install dependencies
sudo pacman -S python python-pip glfw-x11 freeglut

# Rest same as above
git clone https://github.com/yourusername/ancient-indian-chess.git
cd ancient-indian-chess
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
```

### Linux Troubleshooting

**Problem**: ImportError for OpenGL
- **Solution**: Install system OpenGL packages:
  ```bash
  sudo apt install python3-opengl  # Ubuntu/Debian
  sudo dnf install python3-pyopengl  # Fedora
  ```

**Problem**: GLFW initialization failed
- **Solution**: Install GLFW system package:
  ```bash
  sudo apt install libglfw3 libglfw3-dev
  ```

**Problem**: Graphics driver issues
- **Solution**: Install proprietary drivers:
  ```bash
  # NVIDIA
  sudo apt install nvidia-driver-XXX
  
  # AMD
  sudo apt install firmware-amd-graphics
  ```

**Problem**: Wayland issues (Ubuntu 22.04+)
- **Solution**: Use X11 session, or set environment:
  ```bash
  export GDK_BACKEND=x11
  python main.py
  ```

---

## 🔧 Development Installation

For developers who want to modify the code:

```bash
# Clone repository
git clone https://github.com/yourusername/ancient-indian-chess.git
cd ancient-indian-chess

# Create development environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in editable mode with dev dependencies
pip install -e ".[dev]"

# Or manually:
pip install -r requirements.txt
pip install pytest pytest-cov black flake8

# Run tests
pytest test_engine.py -v

# Run with coverage
pytest --cov=. --cov-report=html

# Format code
black *.py

# Lint code
flake8 *.py --max-line-length=100
```

---

## 🧪 Verification

After installation, verify everything works:

### 1. Quick Test
```bash
python main.py
```

Expected: Game window opens with 3D chess board

### 2. Run Unit Tests
```bash
pytest test_engine.py -v
```

Expected output:
```
test_engine.py::TestChessEngine::test_initial_board_setup PASSED
test_engine.py::TestChessEngine::test_pawn_moves PASSED
... (more tests)
====== 17 passed in 0.5s ======
```

### 3. Check OpenGL
```python
python -c "from OpenGL.GL import *; print('OpenGL OK')"
```

Expected: `OpenGL OK` (no errors)

### 4. Check GLFW
```python
python -c "import glfw; print('GLFW version:', glfw.get_version_string())"
```

Expected: `GLFW version: 3.x.x`

---

## 🚀 Performance Optimization

### Low-End Systems

If game runs slowly, try these optimizations:

1. **Disable MSAA**:
   Edit `main.py`, line 22:
   ```python
   # glfw.window_hint(glfw.SAMPLES, 4)  # Comment out this line
   ```

2. **Lower Resolution**:
   ```bash
   python main.py --width 1024 --height 768
   ```

3. **Reduce AI Depth**:
   Edit `ai.py`, line 19:
   ```python
   self.depth = 2  # Change from 3 to 2
   ```

4. **Lower Piece Detail**:
   Edit `config.py`:
   ```python
   PIECE_DETAIL = PIECE_DETAIL_LOW  # 8 instead of 12
   ```

### High-End Systems

For best quality on powerful hardware:

1. **Increase MSAA**:
   Edit `main.py`, line 22:
   ```python
   glfw.window_hint(glfw.SAMPLES, 8)  # 8x instead of 4x
   ```

2. **Higher Resolution**:
   ```bash
   python main.py --width 1920 --height 1080
   # Or 4K:
   python main.py --width 3840 --height 2160
   ```

3. **Increase AI Depth**:
   Edit `ai.py`, line 19:
   ```python
   self.depth = 4  # Harder AI, but slower (5-15s per move)
   ```

4. **Higher Piece Detail**:
   Edit `config.py`:
   ```python
   PIECE_DETAIL = PIECE_DETAIL_HIGH  # 20 instead of 12
   ```

---

## 🐛 Common Issues

### Issue 1: "ModuleNotFoundError: No module named 'OpenGL'"

**Cause**: PyOpenGL not installed

**Solution**:
```bash
pip install PyOpenGL PyOpenGL-accelerate
```

### Issue 2: "GLFW initialization failed"

**Cause**: GLFW library not found

**Solutions**:
- **Windows**: Should work out of the box
- **macOS**: `brew install glfw`
- **Linux**: `sudo apt install libglfw3`

### Issue 3: Black screen or no pieces visible

**Cause**: Graphics driver or OpenGL version

**Solution**:
1. Update graphics drivers
2. Check OpenGL version:
   ```python
   python -c "from OpenGL.GL import *; import glfw; glfw.init(); glfw.window_hint(glfw.VISIBLE, False); w = glfw.create_window(1,1,'',None,None); glfw.make_context_current(w); print('OpenGL:', glGetString(GL_VERSION)); glfw.terminate()"
   ```
3. Must be OpenGL 3.3+ (should show "3.3" or higher)

### Issue 4: ImportError on numpy

**Cause**: Numpy not installed or wrong version

**Solution**:
```bash
pip install numpy>=1.24.3
```

### Issue 5: Game crashes immediately

**Cause**: Various (check error message)

**Debug steps**:
1. Run with Python directly to see full error:
   ```bash
   python -u main.py
   ```
2. Check if all dependencies installed:
   ```bash
   pip list | grep -E "(OpenGL|glfw|numpy)"
   ```
3. Try running tests:
   ```bash
   pytest test_engine.py -v
   ```

### Issue 6: Mouse picking doesn't work correctly

**Cause**: DPI scaling on Windows

**Solution**:
- Already handled in code
- If still issues, disable DPI scaling:
  - Right-click `python.exe` → Properties → Compatibility
  - Check "Override high DPI scaling behavior"

### Issue 7: AI takes forever to move

**Cause**: Depth too high

**Solution**:
- Reduce depth in `ai.py` (line 19) to 2 or 3
- Performance: depth 2 = 0.1s, depth 3 = 1s, depth 4 = 10s

### Issue 8: Text not visible

**Cause**: Text rendering is simplified in this version

**Note**: UI text uses simple stroke rendering (not full font rendering)
- Text is visible but basic
- For production, integrate FreeType or bitmap fonts

---

## 📦 Package Dependencies

### Core Dependencies

```
PyOpenGL==3.1.7          # OpenGL bindings for Python
PyOpenGL-accelerate==3.1.7  # Optional acceleration (C extensions)
glfw==2.6.3              # Window and input handling
numpy==1.24.3            # Numerical arrays and math
```

### Development Dependencies

```
pytest==7.4.3            # Testing framework
pytest-cov               # Coverage reporting
black                    # Code formatting
flake8                   # Code linting
```

### Optional Dependencies

```
matplotlib               # For visualizing evaluation
pillow                   # For saving screenshots
```

---

## 🔄 Updating

To update to a newer version:

```bash
# Update code
git pull

# Update dependencies
pip install --upgrade -r requirements.txt

# If using dev install
pip install --upgrade -e ".[dev]"
```

---

## 🗑️ Uninstallation

### Remove Virtual Environment

```bash
# Just delete the venv folder
rm -rf venv  # Linux/macOS
rmdir /s venv  # Windows
```

### Remove System-Wide Install

```bash
pip uninstall PyOpenGL PyOpenGL-accelerate glfw numpy pytest
```

### Remove Project

```bash
# Delete project folder
cd ..
rm -rf ancient-indian-chess  # Linux/macOS
rmdir /s ancient-indian-chess  # Windows
```

---

## 💡 Tips

1. **Use Virtual Environments**: Prevents dependency conflicts
2. **Update Regularly**: Keep dependencies up to date
3. **Check GPU Drivers**: OpenGL issues usually = driver problems
4. **Test After Install**: Run `pytest` to verify installation
5. **Start Simple**: Use default settings first, optimize later

---

## 📞 Getting Help

If you still have issues after following this guide:

1. **Check error messages carefully** - they often tell you exactly what's wrong
2. **Search for the error** - someone likely had the same issue
3. **Check system requirements** - especially OpenGL version
4. **Try on different machine** - to isolate hardware issues
5. **Check README.md** - for additional troubleshooting

### Useful Diagnostic Commands

```bash
# Python version
python --version

# Installed packages
pip list

# OpenGL info (create test script)
python -c "from OpenGL.GL import *; import glfw; glfw.init(); glfw.window_hint(glfw.VISIBLE, False); w = glfw.create_window(1,1,'test',None,None); glfw.make_context_current(w); print('Vendor:', glGetString(GL_VENDOR)); print('Renderer:', glGetString(GL_RENDERER)); print('Version:', glGetString(GL_VERSION)); glfw.terminate()"

# GLFW version
python -c "import glfw; print(glfw.get_version_string())"

# System info
python -c "import platform; print(platform.platform())"
```

---

**Installation complete! Enjoy the game! ♟️**

For gameplay instructions, see [QUICKSTART.md](QUICKSTART.md)

For full documentation, see [README.md](README.md)
