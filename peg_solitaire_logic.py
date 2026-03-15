class PegSolitaireGame:
    def __init__(self, board_type="English", size=7):
        self.board_type = board_type
        self.size = size
        self.board = []
        self._initialize_board()

    def _initialize_board(self):
        """
        Initializes the board based on the board type and size.
        Board representation:
        0: Invalid (out of bounds for the specific geometry)
        1: Peg
        2: Empty hole
        """
        # Create an empty NxN grid first
        self.board = [[0 for _ in range(self.size)] for _ in range(self.size)]

        if self.board_type == "English":
            # For English, it's typically a cross shape.
            # Assuming size is odd and >= 3. A 7x7 has a 3x3 center and 3x3 arms.
            arm_width = self.size // 3
            if self.size % 3 != 0:
                arm_width = self.size // 3 if self.size // 3 > 0 else 1
                # this is an approximation for non-standard English board sizes

            # Use a more generic approach: standard is 7x7 with 3x3 corners missing.
            # We'll calculate a generic cross based on a third of the dimension.
            one_third = self.size // 3
            two_thirds = self.size - one_third

            for r in range(self.size):
                for c in range(self.size):
                    # Corners are invalid (0)
                    if (r < one_third and c < one_third) or \
                       (r < one_third and c >= two_thirds) or \
                       (r >= two_thirds and c < one_third) or \
                       (r >= two_thirds and c >= two_thirds):
                        self.board[r][c] = 0
                    else:
                        self.board[r][c] = 1 # Peg

            # Center is empty
            center = self.size // 2
            self.board[center][center] = 2 # Empty hole

        elif self.board_type == "Diamond":
            # A diamond shape in a square grid.
            center = self.size // 2
            for r in range(self.size):
                for c in range(self.size):
                    distance = abs(r - center) + abs(c - center)
                    if distance <= center:
                        self.board[r][c] = 1
                    else:
                        self.board[r][c] = 0
            self.board[center][center] = 2

        elif self.board_type == "Hexagon":
            # Hexagon on a hexagonal grid (typically represented on a slanted square grid)
            # Let's map it onto a square grid where a regular hexagon is formed by 
            # bounds on x, y, and x+y.
            center = self.size // 2
            for r in range(self.size):
                for c in range(self.size):
                    # Hexagonal distance in axial coordinates
                    # using r as q and c as r.
                    dq = r - center
                    dr = c - center
                    if abs(dq) <= center and abs(dr) <= center and abs(dq + dr) <= center:
                         self.board[r][c] = 1
                    else:
                         self.board[r][c] = 0
            self.board[center][center] = 2

    def is_valid_position(self, r, c):
        return 0 <= r < self.size and 0 <= c < self.size and self.board[r][c] != 0

    def get_peg(self, r, c):
        if self.is_valid_position(r, c):
            return self.board[r][c]
        return 0

    def is_valid_move(self, start_r, start_c, end_r, end_c):
        if not self.is_valid_position(start_r, start_c) or not self.is_valid_position(end_r, end_c):
            return False
        
        if self.board[start_r][start_c] != 1 or self.board[end_r][end_c] != 2:
            return False

        dr = end_r - start_r
        dc = end_c - start_c

        # Orthogonal moves for English and Diamond
        if self.board_type in ["English", "Diamond"]:
            if (abs(dr) == 2 and dc == 0) or (dr == 0 and abs(dc) == 2):
                mid_r = start_r + dr // 2
                mid_c = start_c + dc // 2
                if self.board[mid_r][mid_c] == 1:
                    return True
        elif self.board_type == "Hexagon":
            # Valid moves in axial hex coordinates (dr, dc) can be:
            # (2, 0), (-2, 0), (0, 2), (0, -2), (2, -2), (-2, 2)
            # corresponding to jumping over an adjacent hex
            if (abs(dr) == 2 and dc == 0) or (dr == 0 and abs(dc) == 2) or (dr == 2 and dc == -2) or (dr == -2 and dc == 2):
                mid_r = start_r + dr // 2
                mid_c = start_c + dc // 2
                if self.board[mid_r][mid_c] == 1:
                    return True

        return False

    def make_move(self, start_r, start_c, end_r, end_c):
        if self.is_valid_move(start_r, start_c, end_r, end_c):
            dr = end_r - start_r
            dc = end_c - start_c
            mid_r = start_r + dr // 2
            mid_c = start_c + dc // 2

            self.board[start_r][start_c] = 2 # Make start empty
            self.board[mid_r][mid_c] = 2     # Remove jumped peg
            self.board[end_r][end_c] = 1     # Place peg at end
            return True
        return False

    def is_game_over(self):
        """Returns True if no more valid moves exist."""
        for r in range(self.size):
            for c in range(self.size):
                if self.board[r][c] == 1: # Find a peg
                    # Check all possible moves from this peg
                    moves = [(0, 2), (0, -2), (2, 0), (-2, 0)]
                    if self.board_type == "Hexagon":
                        moves.extend([(2, -2), (-2, 2)])
                    
                    for dr, dc in moves:
                        if self.is_valid_move(r, c, r + dr, c + dc):
                            return False # Found a valid move
        return True

    def get_peg_count(self):
        count = 0
        for r in range(self.size):
            for c in range(self.size):
                if self.board[r][c] == 1:
                    count += 1
        return count

    def has_won(self):
        """Returns True if only one peg is left."""
        return self.get_peg_count() == 1
