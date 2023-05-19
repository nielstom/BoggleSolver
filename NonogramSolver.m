clear; clc

row_clues = {
  [1 2];
  [2 2];
  [1];
  [4];
  [3 1];
  };

col_clues = {
  [1 2];
  [2 2];
  [1];
  [4];
  [3 1];
  };

grid_rows = length(row_clues);
grid_cols = length(col_clues);
row_candidates = [];
col_candidates = [];

UNKNOWN = 0;
MANDATORY_X = 1;
MANDATORY_O = 2;

mandatory_grid = UNKNOWN * ones(grid_rows, grid_cols);

function begin_solving()
  set_row_candidates();
  set_col_candidates();
  
  % Set Mandatory o/x points
  continue_optimizing = true;
  while continue_optimizing
    update_mandatory_grid();
    continue_optimizing = filter_candidates();
  end

  % Using itertools.product() to compute all possible permutations
  % Time complexity: O(n^k), where k is n-rows or n-cols
  row_bitmap_permutations = itertools_product(row_candidates);
  col_bitmap_permutations = itertools_product(col_candidates);
  
  
  for ii = 1:numel(row_bitmap_permutations)
    row_bitmap = row_bitmap_permutations(ii);
    col_bitmap = rowbitmap_2_colbitmap(row_bitmap);
    if contains(col_bitmap_permutations, col_bitmap)
      print_solution(row_bitmap);
      return
    end
  end
  
  error("No solution could be found");

end










