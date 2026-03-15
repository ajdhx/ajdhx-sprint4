import unittest
from peg_solitaire_logic import PegSolitaireGame

class TestPegSolitaireGame(unittest.TestCase):

    def test_english_board_init(self):
        game = PegSolitaireGame("English", 7)
        self.assertEqual(game.board[3][3], 2) # Center is empty
        self.assertEqual(game.board[0][0], 0) # Corner is invalid
        self.assertEqual(game.board[0][3], 1) # Top middle is peg
        self.assertEqual(game.get_peg_count(), 32)
        
    def test_diamond_board_init(self):
        game = PegSolitaireGame("Diamond", 5)
        # Center is (2,2)
        self.assertEqual(game.board[2][2], 2)
        self.assertEqual(game.board[0][0], 0)
        self.assertEqual(game.board[0][2], 1)
        self.assertEqual(game.get_peg_count(), 12)
        
    def test_hexagon_board_init(self):
        game = PegSolitaireGame("Hexagon", 5)
        # Center is (2,2)
        self.assertEqual(game.board[2][2], 2)
        self.assertEqual(game.board[0][0], 0)
        # Hexagon of radius 2 has 19 cells, center is empty so 18 pegs
        self.assertEqual(game.get_peg_count(), 18)

    def test_valid_move_english(self):
        game = PegSolitaireGame("English", 7)
        # Center is (3, 3) and is empty.
        # Peg at (1, 3) can jump over (2, 3) to (3, 3).
        self.assertTrue(game.is_valid_move(1, 3, 3, 3))
        
        # Try moving it
        self.assertTrue(game.make_move(1, 3, 3, 3))
        
        # Check board update
        self.assertEqual(game.board[1][3], 2)
        self.assertEqual(game.board[2][3], 2)
        self.assertEqual(game.board[3][3], 1)
        
        # Check invalid move: already moved, it should be empty now
        self.assertFalse(game.is_valid_move(1, 3, 3, 3))
        
        # Check moves out of bounds
        self.assertFalse(game.is_valid_move(0, 3, -2, 3))
        
        # Check diagonal move (invalid in English)
        self.assertFalse(game.is_valid_move(2, 2, 4, 4))

    def test_hexagon_valid_move(self):
        game = PegSolitaireGame("Hexagon", 5)
        # Center is (2,2) empty. 
        # (0, 2) is a peg. Jump to (2,2) over (1,2)
        self.assertTrue(game.is_valid_move(0, 2, 2, 2))
        
        # (2, 0) is a peg. Jump to (2,2) over (2,1)
        self.assertTrue(game.is_valid_move(2, 0, 2, 2))
        
        # In axial coordinates, dq=2, dr=-2 is a valid move:
        # e.g., (4, 0) to (2, 2)
        self.assertTrue(game.is_valid_move(4, 0, 2, 2))

    def test_game_over(self):
        # Create a small English board (size 3) where no valid jumps are possible
        game = PegSolitaireGame("English", 3)
        self.assertTrue(game.is_game_over())
        self.assertFalse(game.has_won())
    
    #ChatGPT test #1
    def test_invalid_move_rejected(self):
        game = PegSolitaireGame("English", 7)

        # Attempt a move that is only one space away (invalid)
        result = game.make_move(2, 3, 3, 3)

        # Move should fail
        self.assertFalse(result)

        # Board should remain unchanged
        self.assertEqual(game.board[2][3], 1)  # original peg still there
        self.assertEqual(game.board[3][3], 2)  # center still empty
    
    #ChatGPT test #2
    def test_has_won_condition(self):
        game = PegSolitaireGame("English", 7)

        # Manually create a board with only one peg
        for r in range(game.size):
            for c in range(game.size):
                if game.board[r][c] != 0:
                    game.board[r][c] = 2  # empty hole

        game.board[3][3] = 1  # one remaining peg

        self.assertTrue(game.has_won())

if __name__ == '__main__':
    unittest.main()
