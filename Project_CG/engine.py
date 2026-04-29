"""
Chess Engine - Game logic, rules, and state management
Supports both standard chess and Chaturanga variant
"""

import json
from copy import deepcopy

class Piece:
    """Base class for chess pieces"""
    
    def __init__(self, color, position):
        self.color = color  # 'white' or 'black'
        self.position = position  # (row, col)
        self.has_moved = False
        self.symbol = '?'
        self.value = 0
        self.indian_name = "Unknown"
    
    def get_moves(self, board, check_validation=True):
        """Get all pseudo-legal moves (may include moves that leave king in check)"""
        return []
    
    def __repr__(self):
        return f"{self.color[0].upper()}{self.symbol}"

class Padati(Piece):
    """Pawn (Padati - foot soldier)"""
    
    def __init__(self, color, position):
        super().__init__(color, position)
        self.symbol = 'P'
        self.value = 1
        self.indian_name = "Padati"
    
    def get_moves(self, board, check_validation=True):
        moves = []
        row, col = self.position
        direction = -1 if self.color == 'white' else 1
        
        # Forward move
        new_row = row + direction
        if 0 <= new_row < 8 and board[new_row][col] is None:
            moves.append((new_row, col))
            
            # Double move from starting position
            if not self.has_moved:
                new_row2 = row + 2 * direction
                if 0 <= new_row2 < 8 and board[new_row2][col] is None:
                    moves.append((new_row2, col))
        
        # Captures
        for dc in [-1, 1]:
            new_col = col + dc
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                target = board[new_row][new_col]
                if target and target.color != self.color:
                    moves.append((new_row, new_col))
        
        return moves

class Ratha(Piece):
    """Rook (Ratha - chariot)"""
    
    def __init__(self, color, position):
        super().__init__(color, position)
        self.symbol = 'R'
        self.value = 5
        self.indian_name = "Ratha"
    
    def get_moves(self, board, check_validation=True):
        moves = []
        row, col = self.position
        
        # All four directions
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            for i in range(1, 8):
                new_row, new_col = row + dr * i, col + dc * i
                if not (0 <= new_row < 8 and 0 <= new_col < 8):
                    break
                
                target = board[new_row][new_col]
                if target is None:
                    moves.append((new_row, new_col))
                elif target.color != self.color:
                    moves.append((new_row, new_col))
                    break
                else:
                    break
        
        return moves

class Ashva(Piece):
    """Knight (Ashva - horse)"""
    
    def __init__(self, color, position):
        super().__init__(color, position)
        self.symbol = 'N'
        self.value = 3
        self.indian_name = "Ashva"
    
    def get_moves(self, board, check_validation=True):
        moves = []
        row, col = self.position
        
        # All 8 knight moves
        for dr, dc in [(2, 1), (2, -1), (-2, 1), (-2, -1),
                       (1, 2), (1, -2), (-1, 2), (-1, -2)]:
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                target = board[new_row][new_col]
                if target is None or target.color != self.color:
                    moves.append((new_row, new_col))
        
        return moves

class Gaja(Piece):
    """Bishop (Gaja - elephant)"""
    
    def __init__(self, color, position):
        super().__init__(color, position)
        self.symbol = 'B'
        self.value = 3
        self.indian_name = "Gaja"
    
    def get_moves(self, board, check_validation=True):
        moves = []
        row, col = self.position
        
        # All four diagonal directions
        for dr, dc in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
            for i in range(1, 8):
                new_row, new_col = row + dr * i, col + dc * i
                if not (0 <= new_row < 8 and 0 <= new_col < 8):
                    break
                
                target = board[new_row][new_col]
                if target is None:
                    moves.append((new_row, new_col))
                elif target.color != self.color:
                    moves.append((new_row, new_col))
                    break
                else:
                    break
        
        return moves

class Mantri(Piece):
    """Queen (Mantri - minister/advisor)"""
    
    def __init__(self, color, position):
        super().__init__(color, position)
        self.symbol = 'Q'
        self.value = 9
        self.indian_name = "Mantri"
    
    def get_moves(self, board, check_validation=True):
        moves = []
        row, col = self.position
        
        # All 8 directions (combination of rook and bishop)
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0),
                       (1, 1), (1, -1), (-1, 1), (-1, -1)]:
            for i in range(1, 8):
                new_row, new_col = row + dr * i, col + dc * i
                if not (0 <= new_row < 8 and 0 <= new_col < 8):
                    break
                
                target = board[new_row][new_col]
                if target is None:
                    moves.append((new_row, new_col))
                elif target.color != self.color:
                    moves.append((new_row, new_col))
                    break
                else:
                    break
        
        return moves

class Raja(Piece):
    """King (Raja - king)"""
    
    def __init__(self, color, position):
        super().__init__(color, position)
        self.symbol = 'K'
        self.value = 1000
        self.indian_name = "Raja"
    
    def get_moves(self, board, check_validation=True):
        moves = []
        row, col = self.position
        
        # All 8 adjacent squares
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                
                new_row, new_col = row + dr, col + dc
                if 0 <= new_row < 8 and 0 <= new_col < 8:
                    target = board[new_row][new_col]
                    if target is None or target.color != self.color:
                        moves.append((new_row, new_col))
        
        return moves

class ChessEngine:
    """Main chess engine handling game state and rules"""
    
    def __init__(self, use_chaturanga=False):
        self.use_chaturanga = use_chaturanga
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.current_player = 'white'
        self.move_history = []
        self.redo_stack = []
        self.captured_pieces = {'white': [], 'black': []}
        self.last_move = None
        
        self.setup_board()
    
    def setup_board(self):
        """Initialize the board with pieces"""
        # Pawns
        for col in range(8):
            self.board[1][col] = Padati('black', (1, col))
            self.board[6][col] = Padati('white', (6, col))
        
        # Rooks
        self.board[0][0] = Ratha('black', (0, 0))
        self.board[0][7] = Ratha('black', (0, 7))
        self.board[7][0] = Ratha('white', (7, 0))
        self.board[7][7] = Ratha('white', (7, 7))
        
        # Knights
        self.board[0][1] = Ashva('black', (0, 1))
        self.board[0][6] = Ashva('black', (0, 6))
        self.board[7][1] = Ashva('white', (7, 1))
        self.board[7][6] = Ashva('white', (7, 6))
        
        # Bishops
        self.board[0][2] = Gaja('black', (0, 2))
        self.board[0][5] = Gaja('black', (0, 5))
        self.board[7][2] = Gaja('white', (7, 2))
        self.board[7][5] = Gaja('white', (7, 5))
        
        # Queen/Minister
        self.board[0][3] = Mantri('black', (0, 3))
        self.board[7][3] = Mantri('white', (7, 3))
        
        # King
        self.board[0][4] = Raja('black', (0, 4))
        self.board[7][4] = Raja('white', (7, 4))
    
    def get_legal_moves(self, position):
        """Get all legal moves for piece at position"""
        row, col = position
        piece = self.board[row][col]
        
        if not piece or piece.color != self.current_player:
            return []
        
        pseudo_legal = piece.get_moves(self.board)
        legal_moves = []
        
        # Filter out moves that leave king in check
        for move_to in pseudo_legal:
            if self.is_legal_move((position, move_to)):
                legal_moves.append(move_to)
        
        return legal_moves
    
    def is_legal_move(self, move):
        """Check if a move is legal (doesn't leave king in check)"""
        from_pos, to_pos = move
        
        # Make temporary move
        piece = self.board[from_pos[0]][from_pos[1]]
        captured = self.board[to_pos[0]][to_pos[1]]
        
        self.board[to_pos[0]][to_pos[1]] = piece
        self.board[from_pos[0]][from_pos[1]] = None
        piece.position = to_pos
        
        # Check if king is in check
        in_check = self.is_in_check(piece.color)
        
        # Undo temporary move
        self.board[from_pos[0]][from_pos[1]] = piece
        self.board[to_pos[0]][to_pos[1]] = captured
        piece.position = from_pos
        
        return not in_check
    
    def is_in_check(self, color):
        """Check if the king of given color is under attack"""
        # Find king
        king_pos = None
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece and isinstance(piece, Raja) and piece.color == color:
                    king_pos = (row, col)
                    break
            if king_pos:
                break
        
        if not king_pos:
            return False
        
        # Check if any enemy piece can attack the king
        enemy_color = 'black' if color == 'white' else 'white'
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece and piece.color == enemy_color:
                    moves = piece.get_moves(self.board, check_validation=False)
                    if king_pos in moves:
                        return True
        
        return False
    
    def make_move(self, move):
        """Execute a move"""
        from_pos, to_pos = move
        piece = self.board[from_pos[0]][from_pos[1]]
        captured = self.board[to_pos[0]][to_pos[1]]
        
        if captured:
            self.captured_pieces[self.current_player].append(captured)
        
        # Move piece
        self.board[to_pos[0]][to_pos[1]] = piece
        self.board[from_pos[0]][from_pos[1]] = None
        piece.position = to_pos
        piece.has_moved = True
        
        # Pawn promotion
        if isinstance(piece, Padati):
            if (piece.color == 'white' and to_pos[0] == 0) or \
               (piece.color == 'black' and to_pos[0] == 7):
                self.board[to_pos[0]][to_pos[1]] = Mantri(piece.color, to_pos)
        
        # Record move
        self.move_history.append({
            'from': from_pos,
            'to': to_pos,
            'piece': piece.symbol,
            'captured': captured.symbol if captured else None,
            'player': self.current_player
        })
        self.redo_stack.clear()
        self.last_move = move
        
        # Switch player
        self.current_player = 'black' if self.current_player == 'white' else 'white'
    
    def undo_move(self):
        """Undo the last move"""
        if not self.move_history:
            return
        
        last = self.move_history.pop()
        from_pos = last['from']
        to_pos = last['to']
        
        piece = self.board[to_pos[0]][to_pos[1]]
        self.board[from_pos[0]][from_pos[1]] = piece
        piece.position = from_pos
        
        # Restore captured piece
        if last['captured']:
            # Find captured piece from history
            enemy_color = 'black' if last['player'] == 'white' else 'white'
            if self.captured_pieces[last['player']]:
                captured = self.captured_pieces[last['player']].pop()
                self.board[to_pos[0]][to_pos[1]] = captured
        else:
            self.board[to_pos[0]][to_pos[1]] = None
        
        self.redo_stack.append(last)
        self.current_player = last['player']
        self.last_move = self.move_history[-1] if self.move_history else None
    
    def redo_move(self):
        """Redo a previously undone move"""
        if not self.redo_stack:
            return
        
        move_data = self.redo_stack.pop()
        from_pos = move_data['from']
        to_pos = move_data['to']
        self.make_move((from_pos, to_pos))
    
    def is_checkmate(self):
        """Check if current player is checkmated"""
        if not self.is_in_check(self.current_player):
            return False
        
        # Check if any legal move exists
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece and piece.color == self.current_player:
                    if self.get_legal_moves((row, col)):
                        return False
        
        return True
    
    def is_stalemate(self):
        """Check if current player is stalemated"""
        if self.is_in_check(self.current_player):
            return False
        
        # Check if any legal move exists
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece and piece.color == self.current_player:
                    if self.get_legal_moves((row, col)):
                        return False
        
        return True
    
    def is_game_over(self):
        """Check if game has ended"""
        return self.is_checkmate() or self.is_stalemate()
    
    def get_material_score(self):
        """Calculate material advantage"""
        white_score = 0
        black_score = 0
        
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece:
                    if piece.color == 'white':
                        white_score += piece.value
                    else:
                        black_score += piece.value
        
        return white_score - black_score
    
    def save_game(self, filename):
        """Save game state to JSON"""
        game_state = {
            'current_player': self.current_player,
            'move_history': self.move_history,
            'use_chaturanga': self.use_chaturanga
        }
        
        with open(filename, 'w') as f:
            json.dumps(game_state, f, indent=2)
    
    def load_game(self, filename):
        """Load game state from JSON"""
        try:
            with open(filename, 'r') as f:
                game_state = json.load(f)
            
            self.reset()
            self.use_chaturanga = game_state['use_chaturanga']
            
            # Replay moves
            for move_data in game_state['move_history']:
                self.make_move((tuple(move_data['from']), tuple(move_data['to'])))
            
            return True
        except:
            return False
    
    def reset(self):
        """Reset game to initial state"""
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.current_player = 'white'
        self.move_history = []
        self.redo_stack = []
        self.captured_pieces = {'white': [], 'black': []}
        self.last_move = None
        self.setup_board()
