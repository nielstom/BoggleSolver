clear; clc;
global GG ZZ AA SS
GG = 9;
A = 10; B = 11; C = 12; D = 13; E = 14;
F = 15; G = 16; H = 17; I = 18; J = 19;
K = 20; L = 21; M = 22; N = 23; O = 24;
P = 25; Q = 26; R = 27; S = 28; T = 29;
U = 30; V = 31; W = 32; X = 33; Y = 34; Z = 35; a = 36;

% Board clues
XX = zeros(GG);

% Jigsaw Regions
ZZ = [
  1 1 2 2 2 2 3 3 3;
  1 1 2 9 9 3 3 3 3;
  1 2 2 9 9 4 3 4 3;
  1 2 9 9 9 4 4 4 4;
  1 2 9 9 8 8 8 4 5;
  1 1 7 8 8 8 4 4 5;
  7 7 7 8 8 6 6 5 5;
  7 7 7 8 6 6 6 5 5;
  7 7 6 6 6 6 5 5 5;
];
% Killer Addition Regions
AA = [
  1 1 2 2 2 3 3 4 5;
  6 6 7 8 8 9 9 4 5;
  A A 7 B C C D E E;
  G G B B H L D F E;
  I I J K H L M F O;
  Y Z J K H T M N O;
  Y Z X K U T N N P;
  Y W X V U S Q Q P;
  W W V V S S R R P;
];

% Killer Addition Solutions
SS = [
  4 4 F F F D D 8 F;
  A A 8 C C 6 6 8 F;
  F F 8 F 9 9 C H H;
  A A F F B D C 7 H;
  B B A A B D C 7 5;
  H F A A B C C B 5;
  H F C A F C B B D;
  H 8 C G F D D D D;
  8 8 G G D D C C D;
];

for i=1:GG
  for j=1:GG
    assert(all(SS(i,j) == SS(AA==AA(i,j))));
  end
end

S = rec_grid_solver(XX);

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
global GG ZZ AA SS
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
      for j = 1:GG
         for i = 1:GG
            if X(i,j)==0
               z = 1:GG;
               z(nonzeros(X(i,:))) = 0;
               z(nonzeros(X(:,j))) = 0;  % z() index matches val found/removed
%                z(nonzeros(diag(X))) = 0;  % check diagonals - COMMENT OUT IF UNUSED!!!NOTE - NOT WORKING. No solution reached for some reason with this check left in.
%                z(nonzeros(diag(flip(X)))) = 0;  % check diagonals - COMMENT OUT IF UNUSED!!!
               z(nonzeros(X(ZZ==ZZ(i,j)))) = 0;  % check jigsaw regions
               z(sum(X(AA==AA(i,j))) + (1:GG) > SS(i,j)) = 0;  % check killer regions
               
               C{i,j} = nonzeros(z)';
            end 
         end 
      end 
  L = cellfun(@length,C);   % Number of candidates. 
  s = find(X==0 & L==1,1); 
  e = find(X==0 & L==0,1); 
  end % candidates 
end % rec_grid_solver

