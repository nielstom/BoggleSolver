clear; clc;
global GG GGsqrt
GG = 16;
GGsqrt = sqrt(GG);

A = 10; B = 11; C = 12; D = 13; E = 14; F = 15; G = 16;
% Board clues
X = [
  0 5 0 6 0 D 3 8 0 0 0 1 0 0 0 0;
  E 3 0 0 0 0 0 0 9 0 0 7 4 8 0 0;
  0 0 0 0 1 0 0 0 2 0 F 0 6 E A B;
  1 0 0 0 9 0 2 0 6 0 0 8 0 0 0 0;
  5 9 6 0 0 F 4 3 0 0 0 0 0 0 B G;
  C 0 0 0 7 8 0 0 D 0 0 G 0 5 0 0;
  0 G B 0 0 A 0 0 0 E 0 0 2 0 F 7;
  0 E 3 0 0 6 0 0 0 0 B 4 9 0 0 0;
  0 0 0 D 2 G 0 0 0 0 4 0 0 A 7 0;
  6 2 0 1 0 0 D 0 0 0 9 0 0 4 E 0;
  0 0 8 0 3 0 0 A 0 0 6 F 0 0 0 D;
  4 A 0 0 0 0 0 0 E D G 0 0 6 3 2;
  0 0 0 0 B 0 0 F 0 6 0 D 0 0 0 C;
  B 8 G 9 0 7 0 C 0 0 0 3 0 0 0 0;
  0 0 E F A 0 0 4 0 0 0 0 0 0 6 3;
  0 0 0 0 G 0 0 0 B F 2 0 8 0 1 0;
 ];

S = rec_grid_solver(X);

S_pretty = repmat('x', GG);
for i = 1:GG
  for j = 1:GG
    v = S(i,j);
    if v < A
      S_pretty(i,j) = num2str(v);
    elseif v == A
      S_pretty(i,j) = 'A';
    elseif v == B
      S_pretty(i,j) = 'B';
    elseif v == C
      S_pretty(i,j) = 'C';
    elseif v == D
      S_pretty(i,j) = 'D';
    elseif v == E
      S_pretty(i,j) = 'E';
    elseif v == F
      S_pretty(i,j) = 'F';
    elseif v == G
      S_pretty(i,j) = 'G';
    end
  end
end
for i = 1:GG
  for j = 1:GG
    fprintf('\t%c', S_pretty(i,j));
  end
  fprintf('\n');
end


function X = rec_grid_solver(X) 
global GG GGsqrt
% Solve Grid Puzzles using recursive backtracking. 
%   rec_grid_solver(X), expects a G-by-G array X. 
 % Fill in all “singletons”. 
 % C is a cell array of candidate vectors for each cell. 
 % s is the first cell, if any, with one candidate. 
 % e is the first cell, if any, with no candidates. 
 [C,s,e] = candidates(X);
 while ~isempty(s) && isempty(e)
    X(s) = C{s};
    [C,s,e] = candidates(X);
 end
 % Return for impossible puzzles.
 if ~isempty(e)
    return
 end
 % Recursive backtracking.
 if any(X(:) == 0)
    Y = X;
    z = find(X(:) == 0,1);    % The first unfilled cell.
    for r = [C{z}]            % Iterate over candidates.
       X = Y;
       X(z) = r;              % Insert a tentative value.
       X = rec_grid_solver(X);         % Recursive call.
       if all(X(:) > 0) % && check_skyscrapers(X)  % Found a solution.
          return
       end
    end
 end
% ------------------------------
  function [C,s,e] = candidates(X)
      C = cell(GG,GG);
      tri = @(k) GGsqrt*ceil(k/GGsqrt-1) + (1:GGsqrt);

      for j = 1:GG
         for i = 1:GG
            if X(i,j)==0
               z = 1:GG;
               z(nonzeros(X(i,:))) = 0;
               z(nonzeros(X(:,j))) = 0;  % z() index matches val found/removed
               z(nonzeros(X(tri(i),tri(j)))) = 0;
               C{i,j} = nonzeros(z)'; 
            end 
         end 
      end 
  L = cellfun(@length,C);   % Number of candidates. 
  s = find(X==0 & L==1,1); 
  e = find(X==0 & L==0,1); 
  end % candidates 
end % rec_grid_solver

