import numpy as np
import itertools


class NonogramSolver:
    def __init__(self):
        # Initialize Grid
        self.row_clues = [  # CONFIGURE***
            [1, 1, 4, 3, 6, 10],
            [2, 6, 2, 5, 6],
            [9, 1, 4, 7],
            [1, 3, 3, 6, 6, 1, 1],
            [2, 2, 3, 2, 6, 6, 1],
            [3, 6, 1, 2, 7, 2],
            [2, 1, 7, 2, 2],
            [11, 7],
            [1, 14, 7],
            [2, 2, 1, 13, 6],

            [1, 2, 3, 4, 5, 4, 7, 5],
            [1, 3, 8, 1, 3, 5],
            [2, 3, 6, 6, 4, 2, 2, 5],
            [6, 4, 1, 4, 3, 2, 5],
            [2, 2, 5, 2, 3, 1, 8],
            [1, 1, 4, 2, 3, 1, 1, 7],
            [3, 3, 2, 1, 1, 3, 1, 1],
            [4, 2, 3, 1, 3, 1, 4, 2],
            [4, 2, 4, 1, 1, 6],
            [1, 4, 3, 3, 4, 2, 1],

            [3, 4, 4, 7],
            [4, 3, 8, 8, 1],
            [3, 4, 3, 4, 6, 1, 5],
            [4, 4, 17, 6],
            [1, 4, 1, 13, 9, 5],
            [9, 5, 1, 4, 1, 9, 3, 1],
            [2, 8, 1, 6, 8, 2, 1, 2],
            [1, 1, 4, 2, 6, 4, 1, 4, 2],
            [5, 1, 2, 7, 3, 1, 2, 3, 1, 1],
            [7, 11, 2, 9, 1, 1],

            [7, 2, 8, 6],
            [4, 6, 3, 3, 6],
            [4, 1, 1, 8, 5, 5],
            [2, 1, 1, 6, 1, 8, 5],
            [6, 3, 3, 5, 13],
            [4, 4, 3, 4, 9, 2],
            [4, 2, 3, 3, 1, 13, 3],
            [2, 3, 4, 1, 1, 1, 4, 8, 3],
            [3, 2, 8, 4, 8, 1],
            [9, 4, 1, 8, 3],

            [8, 4, 1, 1, 6, 7, 2],
            [7, 3, 7, 1, 2, 3, 1],
            [1, 2, 1, 2, 1, 1, 9, 2, 4, 1],
            [1, 1, 2, 1, 4, 9, 1, 3, 4, 1],
            [3, 1, 5, 2, 5, 1, 4, 4, 1, 1],
            [1, 4, 1, 1, 1, 3, 3, 4, 3],
            [5, 7, 7, 5, 3],
            [4, 11, 7, 7, 4],
            [3, 10, 10, 11, 3],
            [10, 3, 10, 15],
        ]
        self.col_clues = [  # CONFIGURE***
            [2, 3, 1, 1, 2, 2, 2, 3],
            [2, 7, 1, 4, 3, 4, 4],
            [1, 1, 1, 4, 2, 14, 5],
            [8, 1, 19, 6],
            [5, 8, 5, 1, 1, 3, 3, 1],
            [2, 12, 1, 1, 7, 2],
            [2, 7, 2, 3, 3],
            [3, 1, 1, 2, 2, 1, 5, 2, 4],
            [1, 1, 6, 3, 9, 4],
            [2, 7, 3, 4, 1, 8],

            [3, 7, 1, 3, 4, 3, 4],
            [4, 6, 3, 5],
            [4, 5, 4, 3, 2, 4],
            [4, 8, 2, 1, 4],
            [1, 12, 6, 3],
            [1, 1, 5, 3, 1, 2, 6, 1],
            [2, 2, 2, 2, 3, 8, 1],
            [3, 3, 1, 2, 3, 3],
            [5, 6, 3, 2, 2, 1, 2],
            [5, 2, 2, 6, 11, 2, 2],

            [2, 1, 3, 16, 1, 2],
            [4, 3, 18, 1, 4, 2],
            [2, 4, 1, 1, 2, 8, 2, 2],
            [3, 3, 6, 9, 2, 9],
            [4, 2, 6, 6, 1, 9],
            [2, 1, 2, 6, 4, 3, 10],
            [3, 3, 1, 4, 1, 3, 4],
            [1, 1, 1, 1, 6, 1, 3, 1, 11, 4],
            [3, 3, 4, 1, 6, 1, 1, 4, 4, 5],
            [3, 6, 1, 1, 1, 6, 8, 4, 3],

            [8, 6, 7, 1, 1, 1],
            [8, 1, 7, 4, 1, 5],
            [1, 7, 2, 10, 8, 1],
            [2, 12, 8, 1, 9, 2],
            [12, 9, 8, 4],
            [12, 7, 16],
            [3, 1, 4, 4, 1, 10, 6],
            [4, 4, 2, 2, 9, 5],
            [1, 4, 1, 4, 13, 4],
            [4, 4, 2, 3, 15, 3],

            [3, 1, 2, 1, 2, 5, 7, 5, 3],
            [2, 1, 2, 5, 4, 1, 3, 3],
            [2, 9, 3, 3, 3, 2],
            [2, 2, 9, 3, 5, 1, 2],
            [2, 13, 1, 3, 2, 1, 2],
            [1, 10, 3, 3, 4, 1, 2],
            [1, 9, 3, 3, 1, 1],
            [1, 4, 3, 2, 1, 9],
            [1, 5, 2, 1, 2, 2, 5],
            [1, 5, 1, 2, 4, 2, 6],
        ]
        self.grid_rows = len(self.row_clues)
        self.grid_cols = len(self.col_clues)
        self.row_candidates = []
        self.col_candidates = []
        self.UNKNOWN = 0
        self.MANDATORY_X = 1
        self.MANDATORY_O = 2
        self.mandatory_grid = [[self.UNKNOWN for _ in range(self.grid_cols)] for _ in range(self.grid_rows)]

    def begin_solving(self):
        self.set_row_candidates()  # [m rows  x  n cand-per-row]
        self.set_col_candidates()  # [m cols  x  n cand-per-row]

        # Optimization: set mandatory o/x points (T/F in all row_candidates)
        continue_optimizing = True
        while continue_optimizing:
            self.update_mandatory_grid()
            continue_optimizing = self.filter_candidates()

        # Using itertools.product() to compute all possible permutations
        # Time complexity: O(n^k), where k is n-rows or n-cols
        row_bitmap_permutations = itertools.product(*self.row_candidates)
        col_bitmap_permutations = itertools.product(*self.col_candidates)

        for row_bitmap in row_bitmap_permutations:
            col_bitmap = self.rowbitmap_2_colbitmap(row_bitmap)
            if col_bitmap in col_bitmap_permutations:
                self.print_solution(row_bitmap)
                return  # Solved!

        exit("No solution could be found")

    def update_mandatory_grid(self):
        # Updates mandatory grid with all rows/cols being T/F
        for i in range(self.grid_rows):  # Check rows
            row_candidate = self.row_candidates[i]
            all_false = [True] * self.grid_cols
            all_true = [True] * self.grid_cols
            for j in range(self.grid_cols):
                if self.mandatory_grid[i][j] is self.UNKNOWN:
                    for cand in row_candidate:
                        if cand[j]:
                            all_false[j] = False
                        else:
                            all_true[j] = False
                else:
                    all_true[j] = False
                    all_false[j] = False
            for j in range(self.grid_cols):
                if all_false[j]:
                    self.mandatory_grid[i][j] = self.MANDATORY_X
                elif all_true[j]:
                    self.mandatory_grid[i][j] = self.MANDATORY_O
        for i in range(self.grid_cols):  # Check cols
            col_candidate = self.col_candidates[i]
            all_false = [True] * self.grid_rows
            all_true = [True] * self.grid_rows
            for j in range(self.grid_rows):
                if self.mandatory_grid[j][i] is self.UNKNOWN:
                    for cand in col_candidate:
                        if cand[j]:
                            all_false[j] = False
                        else:
                            all_true[j] = False
                else:
                    all_true[j] = False
                    all_false[j] = False
            for j in range(self.grid_rows):
                if all_false[j]:
                    self.mandatory_grid[j][i] = self.MANDATORY_X
                elif all_true[j]:
                    self.mandatory_grid[j][i] = self.MANDATORY_O

    def filter_candidates(self):
        # If successful in removing any rows/cols from candidates list, continues optimizing
        continue_optimizing = False
        for i in range(self.grid_rows):  # Filter out row candidates
            for cand in self.row_candidates[i][:]:
                candidate_removed = False
                for k in range(self.grid_cols):
                    if ((cand[k] is True) and (self.mandatory_grid[i][k] is self.MANDATORY_X)) or \
                       ((cand[k] is False) and (self.mandatory_grid[i][k] is self.MANDATORY_O)):
                        self.row_candidates[i].remove(cand)
                        candidate_removed = True
                        continue_optimizing = True
                        break
                if candidate_removed:
                    break
        for i in range(self.grid_cols):  # Filter out col candidates
            for cand in self.col_candidates[i][:]:
                candidate_removed = False
                for k in range(self.grid_rows):
                    if ((cand[k] is True) and (self.mandatory_grid[k][i] is self.MANDATORY_X)) or \
                       ((cand[k] is False) and (self.mandatory_grid[k][i] is self.MANDATORY_O)):
                        self.col_candidates[i].remove(cand)
                        candidate_removed = True
                        continue_optimizing = True
                        break
                if candidate_removed:
                    break

        return continue_optimizing

    def set_row_candidates(self):
        # e.g. 2 1 | | | | |  -> TTFTF, TTFFT, FTTFT
        # e.g. 1 1 | | | | |  -> TTFFF, TFFFT, FTFFT, ...
        # e.g. 5   | | | | |  -> TTTTT
        self.row_candidates = []
        for row_clue in self.row_clues:
            # init_list has the correct number of true/false values as the valid row. e.g. 2 1  and 5 rows  ->  TTTFF
            init_list = [True] * sum(row_clue) + [False] * (self.grid_rows - sum(row_clue))
            # All permutations with correct number of true/false values. e.g. TTTFF, TTFTF, TTFFT, ...
            row_candidate = list(set(itertools.permutations(init_list)))  # list(set(...)) removes duplicates
            # Only keep candidates if they match the clue. e.g.Match (2 1)
            for cand in row_candidate[:]:
                if not self.valid_candidate(cand, row_clue):
                    row_candidate.remove(cand)
            self.row_candidates.append(row_candidate)

    def set_col_candidates(self):
        # e.g. 2 1 | | | | |  -> TTFTF, TTFFT, FTTFT
        # e.g. 1 1 | | | | |  -> TTFFF, TFFFT, FTFFT, ...
        # e.g. 5   | | | | |  -> TTTTT
        self.col_candidates = []
        for col_clue in self.col_clues:
            # init_list has the correct number of true/false values as the valid col. e.g. 2 1  and 5 rows  ->  TTTFF
            init_list = [True] * sum(col_clue) + [False] * (self.grid_cols - sum(col_clue))
            # All permutations with correct number of true/false values. e.g. TTTFF, TTFTF, TTFFT, ...
            col_candidate = list(set(itertools.permutations(init_list)))  # list(set(...)) removes duplicates
            # Only keep candidates if they match the clue. e.g.Match (2 1)
            for cand in col_candidate[:]:
                if not self.valid_candidate(cand, col_clue):
                    col_candidate.remove(cand)
            self.col_candidates.append(col_candidate)

    @staticmethod
    def valid_candidate(candidate, clue):
        # e.g. cand=[T, F, T, F, F], clue=[1, 1]  --> returns True
        # e.g.  cand=[T, T, F, F, F], clue=[1, 1]  --> returns False
        cand_clue = []
        val = 0
        for t in candidate:
            if t:
                val += 1
            elif val == 0:
                pass
            else:
                cand_clue.append(val)
                val = 0
        if val != 0:
            cand_clue.append(val)
        return cand_clue == clue

    @staticmethod
    def rowbitmap_2_colbitmap(row_bitmap):
        return tuple(map(tuple, np.transpose(row_bitmap)))

    def print_solution(self, row_bitmap):
        for r in range(self.grid_rows):
            for c in range(self.grid_cols):
                if row_bitmap[r][c]:
                    print('X ', end='')
                else:
                    print('_ ', end='')
            print('')


def main():
    solver = NonogramSolver()
    solver.begin_solving()


if __name__ == '__main__':
    main()
