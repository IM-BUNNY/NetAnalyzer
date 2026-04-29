"""
Chess AI using minimax with alpha-beta pruning
Includes piece-square tables and mobility evaluation
"""

from engine import Padati, Ratha, Ashva, Gaja, Mantri, Raja
import random

class ChessAI:
    """AI opponent for chess"""
    
    def __init__(self, depth=3):
        self.depth = depth
        self.nodes_searched = 0
        
        # Evaluation weights (tunable)
        self.weight_material = 1.0
        self.weight_mobility = 0.1
        self.weight_position = 0.05
        
        # Piece-square tables (values for white, flip for black)
        # Encourage center control and piece development
        self.pawn_table = [
            [0,  0,  0,  0,  0,  0,  0,  0],
            [50, 50, 50, 50, 50, 50, 50, 50],
            [10, 10, 20, 30, 30, 20, 10, 10],
            [5,  5, 10, 25, 25, 10,  5,  5],
            [0,  0,  0, 20, 20,  0,  0,  0],
            [5, -5,-10,  0,  0,-10, -5,  5],
            [5, 10, 10,-20,-20, 10, 10,  5],
            [0,  0,  0,  0,  0,  0,  0,  0]
        ]
        
        self.knight_table = [
            [-50,-40,-30,-30,-30,-30,-40,-50],
            [-40,-20,  0,  0,  0,  0,-20,-40],
            [-30,  0, 10, 15, 15, 10,  0,-30],
            [-30,  5, 15, 20, 20, 15,  5,-30],
            [-30,  0, 15, 20, 20, 15,  0,-30],
            [-30,  5, 10, 15, 15, 10,  5,-30],
            [-40,-20,  0,  5,  5,  0,-20,-40],
            [-50,-40,-30,-30,-30,-30,-40,-50]
        ]
        
        self.bishop_table = [
            [-20,-10,-10,-10,-10,-10,-10,-20],
            [-10,  0,  0,  0,  0,  0,  0,-10],
            [-10,  0,  5, 10, 10,  5,  0,-10],
            [-10,  5,  5, 10, 10,  5,  5,-10],
            [-10,  0, 10, 10, 10, 10,  0,-10],
            [-10, 10, 10, 10, 10, 10, 10,-10],
            [-10,  5,  0,  0,  0,  0,  5,-10],
            [-20,-10,-10,-10,-10,-10,-10,-20]
        ]
        
        self.rook_table = [
            [0,  0,  0,  0,  0,  0,  0,  0],
            [5, 10, 10, 10, 10, 10, 10,  5],
            [-5,  0,  0,  0,  0,  0,  0, -5],
            [-5,  0,  0,  0,  0,  0,  0, -5],
            [-5,  0,  0,  0,  0,  0,  0, -5],
            [-5,  0,  0,  0,  0,  0,  0, -5],
            [-5,  0,  0,  0,  0,  0,  0, -5],
            [0,  0,  0,  5,  5,  0,  0,  0]
        ]
        
        self.queen_table = [
            [-20,-10,-10, -5, -5,-10,-10,-20],
            [-10,  0,  0,  0,  0,  0,  0,-10],
            [-10,  0,  5,  5,  5,  5,  0,-10],
            [-5,  0,  5,  5,  5,  5,  0, -5],
            [0,  0,  5,  5,  5,  5,  0, -5],
            [-10,  5,  5,  5,  5,  5,  0,-10],
            [-10,  0,  5,  0,  0,  0,  0,-10],
            [-20,-10,-10, -5, -5,-10,-10,-20]
        ]
        
        self.king_middle_table = [
            [-30,-40,-40,-50,-50,-40,-40,-30],
            [-30,-40,-40,-50,-50,-40,-40,-30],
            [-30,-40,-40,-50,-50,-40,-40,-30],
            [-30,-40,-40,-50,-50,-40,-40,-30],
            [-20,-30,-30,-40,-40,-30,-30,-20],
            [-10,-20,-20,-20,-20,-20,-20,-10],
            [20, 20,  0,  0,  0,  0, 20, 20],
            [20, 30, 10,  0,  0, 10, 30, 20]
        ]
    
    def get_best_move(self, engine):
        """Get the best move using minimax with alpha-beta pruning"""
        self.nodes_searched = 0
        
        # Get all legal moves
        all_moves = []
        for row in range(8):
            for col in range(8):
                piece = engine.board[row][col]
                if piece and piece.color == engine.current_player:
                    moves = engine.get_legal_moves((row, col))
                    for move_to in moves:
                        all_moves.append(((row, col), move_to))
        
        if not all_moves:
            return None
        
        # Search for best move
        best_move = None
        best_value = float('-inf')
        alpha = float('-inf')
        beta = float('inf')
        
        # Randomize move order for variety
        random.shuffle(all_moves)
        
        for move in all_moves:
            # Make move
            from_pos, to_pos = move
            piece = engine.board[from_pos[0]][from_pos[1]]
            captured = engine.board[to_pos[0]][to_pos[1]]
            
            engine.board[to_pos[0]][to_pos[1]] = piece
            engine.board[from_pos[0]][from_pos[1]] = None
            old_pos = piece.position
            piece.position = to_pos
            
            # Evaluate
            value = -self.minimax(engine, self.depth - 1, -beta, -alpha, False)
            
            # Undo move
            engine.board[from_pos[0]][from_pos[1]] = piece
            engine.board[to_pos[0]][to_pos[1]] = captured
            piece.position = old_pos
            
            if value > best_value:
                best_value = value
                best_move = move
            
            alpha = max(alpha, value)
        
        print(f"AI searched {self.nodes_searched} nodes, evaluation: {best_value:.2f}")
        return best_move
    
    def minimax(self, engine, depth, alpha, beta, maximizing):
        """Minimax with alpha-beta pruning"""
        self.nodes_searched += 1
        
        if depth == 0 or engine.is_game_over():
            return self.evaluate(engine)
        
        # Get all legal moves for current player
        all_moves = []
        for row in range(8):
            for col in range(8):
                piece = engine.board[row][col]
                if piece and piece.color == engine.current_player:
                    moves = engine.get_legal_moves((row, col))
                    for move_to in moves:
                        all_moves.append(((row, col), move_to))
        
        if not all_moves:
            # No legal moves - checkmate or stalemate
            if engine.is_in_check(engine.current_player):
                return -10000  # Checkmate
            return 0  # Stalemate
        
        if maximizing:
            max_eval = float('-inf')
            for move in all_moves:
                from_pos, to_pos = move
                piece = engine.board[from_pos[0]][from_pos[1]]
                captured = engine.board[to_pos[0]][to_pos[1]]
                
                # Make move
                engine.board[to_pos[0]][to_pos[1]] = piece
                engine.board[from_pos[0]][from_pos[1]] = None
                old_pos = piece.position
                piece.position = to_pos
                old_player = engine.current_player
                engine.current_player = 'white' if engine.current_player == 'black' else 'black'
                
                eval_score = self.minimax(engine, depth - 1, alpha, beta, False)
                
                # Undo move
                engine.board[from_pos[0]][from_pos[1]] = piece
                engine.board[to_pos[0]][to_pos[1]] = captured
                piece.position = old_pos
                engine.current_player = old_player
                
                max_eval = max(max_eval, eval_score)
                alpha = max(alpha, eval_score)
                
                if beta <= alpha:
                    break  # Beta cutoff
            
            return max_eval
        else:
            min_eval = float('inf')
            for move in all_moves:
                from_pos, to_pos = move
                piece = engine.board[from_pos[0]][from_pos[1]]
                captured = engine.board[to_pos[0]][to_pos[1]]
                
                # Make move
                engine.board[to_pos[0]][to_pos[1]] = piece
                engine.board[from_pos[0]][from_pos[1]] = None
                old_pos = piece.position
                piece.position = to_pos
                old_player = engine.current_player
                engine.current_player = 'white' if engine.current_player == 'black' else 'black'
                
                eval_score = self.minimax(engine, depth - 1, alpha, beta, True)
                
                # Undo move
                engine.board[from_pos[0]][from_pos[1]] = piece
                engine.board[to_pos[0]][to_pos[1]] = captured
                piece.position = old_pos
                engine.current_player = old_player
                
                min_eval = min(min_eval, eval_score)
                beta = min(beta, eval_score)
                
                if beta <= alpha:
                    break  # Alpha cutoff
            
            return min_eval
    
    def evaluate(self, engine):
        """Evaluate board position"""
        score = 0
        
        # Material + Position
        for row in range(8):
            for col in range(8):
                piece = engine.board[row][col]
                if piece:
                    piece_value = self.get_piece_value(piece, row, col)
                    if piece.color == 'black':  # AI is black
                        score += piece_value
                    else:
                        score -= piece_value
        
        # Mobility
        mobility_score = self.evaluate_mobility(engine)
        score += mobility_score * self.weight_mobility
        
        return score
    
    def get_piece_value(self, piece, row, col):
        """Get piece value including position bonus"""
        material_value = piece.value
        position_value = 0
        
        # Get position bonus from piece-square table
        if isinstance(piece, Padati):
            if piece.color == 'white':
                position_value = self.pawn_table[row][col]
            else:
                position_value = self.pawn_table[7 - row][col]
        elif isinstance(piece, Ashva):
            if piece.color == 'white':
                position_value = self.knight_table[row][col]
            else:
                position_value = self.knight_table[7 - row][col]
        elif isinstance(piece, Gaja):
            if piece.color == 'white':
                position_value = self.bishop_table[row][col]
            else:
                position_value = self.bishop_table[7 - row][col]
        elif isinstance(piece, Ratha):
            if piece.color == 'white':
                position_value = self.rook_table[row][col]
            else:
                position_value = self.rook_table[7 - row][col]
        elif isinstance(piece, Mantri):
            if piece.color == 'white':
                position_value = self.queen_table[row][col]
            else:
                position_value = self.queen_table[7 - row][col]
        elif isinstance(piece, Raja):
            if piece.color == 'white':
                position_value = self.king_middle_table[row][col]
            else:
                position_value = self.king_middle_table[7 - row][col]
        
        return (material_value * self.weight_material + 
                position_value * self.weight_position * 0.01)
    
    def evaluate_mobility(self, engine):
        """Evaluate mobility (number of legal moves)"""
        black_moves = 0
        white_moves = 0
        
        for row in range(8):
            for col in range(8):
                piece = engine.board[row][col]
                if piece:
                    moves = len(piece.get_moves(engine.board, check_validation=False))
                    if piece.color == 'black':
                        black_moves += moves
                    else:
                        white_moves += moves
        
        return black_moves - white_moves
