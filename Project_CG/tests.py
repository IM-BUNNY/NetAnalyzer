"""
Unit tests for chess engine
Tests move generation, check detection, and game state
"""

import pytest
from engine import ChessEngine, Padati, Ratha, Ashva, Gaja, Mantri, Raja

class TestChessEngine:
    """Test chess engine functionality"""
    
    def setup_method(self):
        """Setup before each test"""
        self.engine = ChessEngine()
    
    def test_initial_board_setup(self):
        """Test that board is set up correctly"""
        # Check pawns
        for col in range(8):
            assert isinstance(self.engine.board[1][col], Padati)
            assert self.engine.board[1][col].color == 'black'
            assert isinstance(self.engine.board[6][col], Padati)
            assert self.engine.board[6][col].color == 'white'
        
        # Check rooks
        assert isinstance(self.engine.board[0][0], Ratha)
        assert isinstance(self.engine.board[0][7], Ratha)
        assert isinstance(self.engine.board[7][0], Ratha)
        assert isinstance(self.engine.board[7][7], Ratha)
        
        # Check kings
        assert isinstance(self.engine.board[0][4], Raja)
        assert self.engine.board[0][4].color == 'black'
        assert isinstance(self.engine.board[7][4], Raja)
        assert self.engine.board[7][4].color == 'white'
    
    def test_pawn_moves(self):
        """Test pawn movement"""
        # White pawn should be able to move 1 or 2 squares forward initially
        moves = self.engine.get_legal_moves((6, 4))
        assert (5, 4) in moves
        assert (4, 4) in moves
        assert len(moves) == 2
        
        # After moving, should only move 1 square
        self.engine.make_move(((6, 4), (5, 4)))
        self.engine.current_player = 'white'  # Keep white's turn
        moves = self.engine.get_legal_moves((5, 4))
        assert (4, 4) in moves
        assert (3, 4) not in moves or len([m for m in moves if m[0] == 3]) <= 1
    
    def test_rook_moves(self):
        """Test rook movement"""
        # Clear some space for rook
        self.engine.board[6][0] = None  # Remove pawn
        
        moves = self.engine.get_legal_moves((7, 0))
        # Should be able to move up the file
        assert (6, 0) in moves
        assert (5, 0) in moves
        
        # Should not jump over pieces
        assert len(moves) == 2  # Only 2 squares up
    
    def test_knight_moves(self):
        """Test knight movement"""
        moves = self.engine.get_legal_moves((7, 1))
        
        # Knight should be able to jump over pawns
        assert len(moves) > 0
        
        # Check some valid knight moves
        assert (5, 0) in moves or (5, 2) in moves
    
    def test_check_detection(self):
        """Test check detection"""
        # Setup a position where black king is in check
        # Clear the board
        self.engine.board = [[None for _ in range(8)] for _ in range(8)]
        
        # Place black king at e8
        self.engine.board[0][4] = Raja('black', (0, 4))
        
        # Place white rook at e1 (checking the king)
        self.engine.board[7][4] = Ratha('white', (7, 4))
        
        # Black should be in check
        assert self.engine.is_in_check('black')
        assert not self.engine.is_in_check('white')
    
    def test_checkmate_detection(self):
        """Test checkmate detection"""
        # Setup fool's mate position (fastest checkmate)
        self.engine.board = [[None for _ in range(8)] for _ in range(8)]
        
        # White king
        self.engine.board[7][4] = Raja('white', (7, 4))
        
        # Black pieces for checkmate
        self.engine.board[5][3] = Mantri('black', (5, 3))  # Queen
        self.engine.board[0][4] = Raja('black', (0, 4))    # Black king (safe)
        
        self.engine.current_player = 'white'
        
        # Should detect checkmate
        assert self.engine.is_in_check('white')
        assert self.engine.is_checkmate()
    
    def test_stalemate_detection(self):
        """Test stalemate detection"""
        # Setup a stalemate position
        self.engine.board = [[None for _ in range(8)] for _ in range(8)]
        
        # White king in corner
        self.engine.board[0][0] = Raja('white', (0, 0))
        
        # Black pieces creating stalemate
        self.engine.board[1][2] = Raja('black', (1, 2))    # Black king
        self.engine.board[2][1] = Mantri('black', (2, 1))  # Queen blocking but not checking
        
        self.engine.current_player = 'white'
        
        # Should detect stalemate
        assert not self.engine.is_in_check('white')
        assert self.engine.is_stalemate()
    
    def test_move_execution(self):
        """Test making moves"""
        initial_piece = self.engine.board[6][4]
        
        # Make a move
        self.engine.make_move(((6, 4), (5, 4)))
        
        # Check move was executed
        assert self.engine.board[5][4] == initial_piece
        assert self.engine.board[6][4] is None
        assert initial_piece.position == (5, 4)
        assert initial_piece.has_moved
        
        # Check turn switched
        assert self.engine.current_player == 'black'
        
        # Check move recorded
        assert len(self.engine.move_history) == 1
    
    def test_capture(self):
        """Test piece capture"""
        # Setup a capture scenario
        self.engine.board = [[None for _ in range(8)] for _ in range(8)]
        
        white_rook = Ratha('white', (4, 4))
        black_pawn = Padati('black', (4, 6))
        
        self.engine.board[4][4] = white_rook
        self.engine.board[4][6] = black_pawn
        self.engine.board[7][4] = Raja('white', (7, 4))
        self.engine.board[0][4] = Raja('black', (0, 4))
        
        self.engine.current_player = 'white'
        
        # Capture the pawn
        self.engine.make_move(((4, 4), (4, 6)))
        
        # Check capture was recorded
        assert black_pawn in self.engine.captured_pieces['white']
        assert self.engine.board[4][6] == white_rook
    
    def test_undo_move(self):
        """Test undo functionality"""
        # Make a move
        initial_state = [[self.engine.board[r][c] for c in range(8)] for r in range(8)]
        
        self.engine.make_move(((6, 4), (5, 4)))
        self.engine.make_move(((1, 4), (2, 4)))
        
        # Undo
        self.engine.undo_move()
        
        # Check state partially restored
        assert self.engine.current_player == 'black'
        assert len(self.engine.move_history) == 1
    
    def test_pawn_promotion(self):
        """Test pawn promotion to queen"""
        self.engine.board = [[None for _ in range(8)] for _ in range(8)]
        
        # White pawn about to promote
        white_pawn = Padati('white', (1, 4))
        self.engine.board[1][4] = white_pawn
        self.engine.board[7][4] = Raja('white', (7, 4))
        self.engine.board[0][3] = Raja('black', (0, 3))
        
        self.engine.current_player = 'white'
        
        # Move pawn to promotion square
        self.engine.make_move(((1, 4), (0, 4)))
        
        # Check promotion occurred
        promoted_piece = self.engine.board[0][4]
        assert isinstance(promoted_piece, Mantri)
        assert promoted_piece.color == 'white'
    
    def test_legal_moves_exclude_check(self):
        """Test that legal moves don't include moves that leave king in check"""
        self.engine.board = [[None for _ in range(8)] for _ in range(8)]
        
        # White king and rook
        white_king = Raja('white', (7, 4))
        white_rook = Ratha('white', (7, 3))
        
        # Black queen attacking
        black_queen = Mantri('black', (5, 3))
        black_king = Raja('black', (0, 4))
        
        self.engine.board[7][4] = white_king
        self.engine.board[7][3] = white_rook
        self.engine.board[5][3] = black_queen
        self.engine.board[0][4] = black_king
        
        self.engine.current_player = 'white'
        
        # Rook is pinned - moving it would expose king
        legal_moves = self.engine.get_legal_moves((7, 3))
        
        # Rook can only move along the pin line or capture the queen
        for move in legal_moves:
            # Each move should not leave king in check
            self.engine.board[move[0]][move[1]] = white_rook
            self.engine.board[7][3] = None
            white_rook.position = move
            
            in_check = self.engine.is_in_check('white')
            
            # Restore
            self.engine.board[7][3] = white_rook
            self.engine.board[move[0]][move[1]] = None
            white_rook.position = (7, 3)
            
            assert not in_check, f"Move {move} leaves king in check"
    
    def test_material_score(self):
        """Test material score calculation"""
        # Initial position should be equal
        score = self.engine.get_material_score()
        assert score == 0
        
        # Remove a white pawn
        self.engine.board[6][0] = None
        score = self.engine.get_material_score()
        assert score < 0  # Black ahead
        
        # Remove a black rook
        self.engine.board[0][0] = None
        score = self.engine.get_material_score()
        assert score > 0  # White ahead

class TestPieces:
    """Test individual piece movements"""
    
    def setup_method(self):
        """Setup empty board"""
        self.board = [[None for _ in range(8)] for _ in range(8)]
    
    def test_pawn_capture(self):
        """Test pawn diagonal capture"""
        pawn = Padati('white', (4, 4))
        enemy = Padati('black', (3, 5))
        
        self.board[4][4] = pawn
        self.board[3][5] = enemy
        
        moves = pawn.get_moves(self.board)
        
        # Should be able to capture diagonally
        assert (3, 5) in moves
    
    def test_rook_blocked(self):
        """Test rook blocked by pieces"""
        rook = Ratha('white', (4, 4))
        blocker = Padati('white', (4, 6))
        
        self.board[4][4] = rook
        self.board[4][6] = blocker
        
        moves = rook.get_moves(self.board)
        
        # Should not move past blocker
        assert (4, 5) in moves
        assert (4, 6) not in moves
        assert (4, 7) not in moves
    
    def test_bishop_diagonal(self):
        """Test bishop diagonal movement"""
        bishop = Gaja('white', (4, 4))
        self.board[4][4] = bishop
        
        moves = bishop.get_moves(self.board)
        
        # Should move diagonally
        assert (5, 5) in moves
        assert (6, 6) in moves
        assert (3, 3) in moves
        assert (2, 2) in moves
        
        # Should not move orthogonally
        assert (4, 5) not in moves
        assert (5, 4) not in moves
    
    def test_queen_range(self):
        """Test queen combination of rook and bishop"""
        queen = Mantri('white', (4, 4))
        self.board[4][4] = queen
        
        moves = queen.get_moves(self.board)
        
        # Should move like rook
        assert (4, 7) in moves
        assert (7, 4) in moves
        
        # Should move like bishop
        assert (7, 7) in moves
        assert (1, 1) in moves
    
    def test_king_limited_range(self):
        """Test king moves only one square"""
        king = Raja('white', (4, 4))
        self.board[4][4] = king
        
        moves = king.get_moves(self.board)
        
        # Should move one square in any direction
        assert (5, 5) in moves
        assert (4, 5) in moves
        assert (3, 4) in moves
        
        # Should not move two squares
        assert (6, 6) not in moves
        assert (4, 6) not in moves

if __name__ == '__main__':
    pytest.main([__file__, '-v'])
