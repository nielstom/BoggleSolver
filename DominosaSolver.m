clear; clc;

fname = 'C:/Users/maize/Downloads/dominosaDaily.json'; % CONFIGURE
nCols = 27;
nRows = 26;

% ---------------------------
% Parse input json file
fid = fopen(fname); 
raw = fread(fid,inf); 
str = char(raw'); 
fclose(fid); 
val = jsondecode(str);
assert(nRows*nCols == val.childCount);
board = zeros(nCols, nRows);
for ii = 1:val.childCount
    board(ii) = str2double( val.children(ii).children.children.name );
end
board = board';
% disp(board);

% Inputs Sanity Check
maxTile = max(max(board));
s = sum(sum(board==maxTile));
for ii = 0:maxTile-1
    assert(s == sum(sum(board==ii)))
end

S = 99;  % Solved Tile
v1 = 1; v2 = 2; r1 = 3; c1 = 4; r2 = 5; c2 = 6;  % Column indeces

nTiles = 0;
for ii = 0:maxTile
    nTiles = nTiles + (maxTile + 1 - ii);
end
allSolvedTileRows = zeros(nTiles,c2);
solvedCounter = 1;
knownTiles = [];
badAnswer = false;


% Manually add solved tiles
% Some line-strats are hard to program in:
% - Boxed-in even/odd strats
% - 2 orientations both same dom 
% allSolvedTileRows(solvedCounter,:) = [3 23 5 7 5 8];
% knownTiles(end+1,1) = 323;
% board(5,7:8) = S;
% solvedCounter = solvedCounter + 1;
% 
% allSolvedTileRows(solvedCounter,:) = [13 13 22 22 23 22];
% knownTiles(end+1,1) = 1313;
% board(22:23,22) = S;
% solvedCounter = solvedCounter + 1;
% 
% allSolvedTileRows(solvedCounter,:) = [13 5 7 26 7 27];
% knownTiles(end+1,1) = 513;
% board(7,26:27) = S;
% solvedCounter = solvedCounter + 1;
% 
% allSolvedTileRows(solvedCounter,:) = [21 23 10 26 10 27];
% knownTiles(end+1,1) = 2123;
% board(10,26:27) = S;
% solvedCounter = solvedCounter + 1;


% Loop until full grid is solved
while any(any(board~=S)) && ~badAnswer
    clc;
    boardUpdated = false;
    
    % Look for forcing-orientationCounter tile placements
    for r = 1:size(board,1)
        for c = 1:size(board,2)
            if board(r,c) ~= S
                orientationCounter = 0;
                check = 0;
                DOWN = 1; UP = 2; RIGHT = 3; LEFT = 4;
                if r < nRows && board(r+1,c) ~= S  % DOWN
                    candTile = [board(r,c), board(r+1,c)];
                    candTileVal = min(candTile)*100 + max(candTile);
                    if ~ismember(candTileVal,knownTiles)
                        orientationCounter = orientationCounter + 1;
                        solvedTileRow = [board(r,c), board(r+1,c), r, c, r+1, c];
                    else
                        fprintf("REDLINE: [%d %d] | (%d,%d) (%d,%d)\n", [board(r,c), board(r+1,c), r, c, r+1, c]);
                    end
                end
                if r > 1 && board(r-1,c) ~= S  % UP
                    candTile = [board(r-1,c), board(r,c)];
                    candTileVal = min(candTile)*100 + max(candTile);
                    if ~ismember(candTileVal,knownTiles)
                        orientationCounter = orientationCounter + 1;
                        solvedTileRow = [board(r-1,c), board(r,c), r-1, c, r, c];
                    else
                        fprintf("REDLINE: [%d %d] | (%d,%d) (%d,%d)\n", [board(r-1,c), board(r,c), r-1, c, r, c]);
                    end
                end
                if c < nCols && board(r,c+1) ~= S  % RIGHT
                    candTile = [board(r,c), board(r,c+1)];
                    candTileVal = min(candTile)*100 + max(candTile);
                    if ~ismember(candTileVal,knownTiles)
                        orientationCounter = orientationCounter + 1;
                        solvedTileRow = [board(r,c), board(r,c+1), r, c, r, c+1];
                    else
                        fprintf("REDLINE: [%d %d] | (%d,%d) (%d,%d)\n", [board(r,c), board(r,c+1), r, c, r, c+1]);
                    end
                end
                if c > 1 && board(r,c-1) ~= S  % LEFT
                    candTile = [board(r,c-1), board(r,c)];
                    candTileVal = min(candTile)*100 + max(candTile);
                    if ~ismember(candTileVal,knownTiles)
                        orientationCounter = orientationCounter + 1;
                        solvedTileRow = [board(r,c-1), board(r,c), r, c-1, r, c];
                    else
                        fprintf("REDLINE: [%d %d] | (%d,%d) (%d,%d)\n", [board(r,c-1), board(r,c), r, c-1, r, c]);
                    end
                end
                if orientationCounter == 1
                    board(solvedTileRow(r1),solvedTileRow(c1)) = S;
                    board(solvedTileRow(r2),solvedTileRow(c2)) = S;
%                     fprintf("[%d %d] | (%d,%d) (%d,%d)\n", solvedTileRow);
                    allSolvedTileRows(solvedCounter,:) = solvedTileRow;
                    solvedCounter = solvedCounter + 1;
                    
                    % Update known tiles so they aren't reused by unique checker
                    knownTiles(end+1,1) = min(solvedTileRow(v1:v2))*100 + max(solvedTileRow(v1:v2));
                    boardUpdated = true;
                elseif orientationCounter == 0
                    disp("ERROR: Bad solution, islanded tile!")
                    badAnswer = true;
                    boardUpdated = true;
                end
            end
        end
    end
    
    % Initialize tileCombinationsMatrix
    % Horizontal
    counter = 0;
    for r = 1:size(board,1)-1
        for c = 1:size(board,2)
            if board(r,c)~=S && board(r+1,c)~=S
                counter = counter + 1;
            end
        end
    end
    % Vertical
    for r = 1:size(board,1)
        for c = 1:size(board,2)-1
            if board(r,c)~=S && board(r,c+1)~=S
                counter = counter + 1;
            end
        end
    end
    tileCombinationsMatrix = zeros(counter,c2);

    % Populate tileCombinationsMatrix
    % Horizontal
    counter = 1;
    for r = 1:size(board,1)-1
        for c = 1:size(board,2)
            if board(r,c)~=S && board(r+1,c)~=S
                tileCombinationsMatrix(counter,:) = [board(r,c), board(r+1,c),r,c,r+1,c];
                counter = counter + 1;
            end
        end
    end
    % Vertical
    for r = 1:size(board,1)
        for c = 1:size(board,2)-1
            if board(r,c)~=S && board(r,c+1)~=S
                tileCombinationsMatrix(counter,:) = [board(r,c), board(r,c+1),r,c,r,c+1];
                counter = counter + 1;
            end
        end
    end

    % Sort tiles in matrix so that min(val) comes before max(val); needed for unique checks later
    for ii = 1:size(tileCombinationsMatrix,1)
        tileCombinationRow = tileCombinationsMatrix(ii,:);
        if tileCombinationRow(v1) > tileCombinationRow(v2)
            tileCombinationsMatrix(ii,:) = tileCombinationRow([v2 v1 r2 c2 r1 c1]);
        end
    end

    % Gives you something like this...
    % tileCombinationsMatrix = [
    %     2 3 r1 c1 r2 c2;
    %     0 3 r1 c1 r2 c2;
    %     0 3 r1 c1 r2 c2;
    %     0 2 r1 c1 r2 c2;
    % ];

    % Find unique tiles
    tileCombinations = tileCombinationsMatrix(:,1)*100 + tileCombinationsMatrix(:,2);
    [counter,uniqueTiles] = groupcounts(tileCombinations);
    matches = uniqueTiles(counter == 1);

    % Print solved tiles and update board
    for ii = 1:numel(matches)
        solvedTileRow = tileCombinationsMatrix(matches(ii) == tileCombinations,:);
        
        % Sort solved tiles (useful for printing later)
        if solvedTileRow(r1) > solvedTileRow(r2) || solvedTileRow(c1) > solvedTileRow(c2)
            solvedTileRow = solvedTileRow([v2 v1 r2 c2 r1 c1]);
        end
        
%         if ismember(solvedTileRow(v1)*100 + solvedTileRow(2), knownTiles)
        if ismember(min(solvedTileRow(v1:v2))*100 + max(solvedTileRow(v1:v2)), knownTiles)
            continue;
        else
            knownTiles(end+1,1) = min(solvedTileRow(v1:v2))*100 + max(solvedTileRow(v1:v2));
        end
        
        % Checker for overlapping tiles
        for sc = 1:solvedCounter-1
            if (solvedTileRow(r1) == allSolvedTileRows(sc,r1) && solvedTileRow(c1) == allSolvedTileRows(sc,c1)) || ...
               (solvedTileRow(r1) == allSolvedTileRows(sc,r2) && solvedTileRow(c1) == allSolvedTileRows(sc,c2)) || ...
               (solvedTileRow(r2) == allSolvedTileRows(sc,r1) && solvedTileRow(c2) == allSolvedTileRows(sc,c1)) || ...
               (solvedTileRow(r2) == allSolvedTileRows(sc,r2) && solvedTileRow(c2) == allSolvedTileRows(sc,c2))
                disp("ERROR: Placing an overlapping tile!");
                disp(board);
                disp(solvedTileRow);
                disp(allSolvedTileRows(sc,:));
                keyboard;
            end
        end
        
        board(solvedTileRow(r1),solvedTileRow(c1)) = S;
        board(solvedTileRow(r2),solvedTileRow(c2)) = S;
%         fprintf("[%d %d] | (%d,%d) (%d,%d)\n", solvedTileRow);
        
        allSolvedTileRows(solvedCounter,:) = solvedTileRow;
        solvedCounter = solvedCounter + 1;
        boardUpdated = true;
    end
    
    if boardUpdated == false
        badAnswer = true;
        disp("Solver got stuck!!");
    end
end

% Print the solved board
if badAnswer
    disp("Bad solution");
else
    disp("Solved Board:");
end
prettyBoard = repmat(" ", 3*size(board,1)+3, 4*size(board,2)+100);
for ii = 1:solvedCounter-1
    solvedTileRow = allSolvedTileRows(ii,:);
    RR = 3*solvedTileRow(r1)-2;
    CC = 4*solvedTileRow(c1)-3;
    if solvedTileRow(r1) == solvedTileRow(r2)  % Horizontal Tile
        prettyBoard(RR,CC+1:CC+6) = "-";
        prettyBoard(RR+2,CC+1:CC+6) = "-";
        prettyBoard(RR+1,CC+1) = string( floor(solvedTileRow(v1)/10) );
        prettyBoard(RR+1,CC+2) = string( rem(solvedTileRow(v1),10) );
        prettyBoard(RR+1,CC+5) = string( floor(solvedTileRow(v2)/10) );
        prettyBoard(RR+1,CC+6) = string( rem(solvedTileRow(v2),10) );
    else  % Vertical Tile
        prettyBoard(RR+1:RR+4,CC) = "|";
        prettyBoard(RR+1:RR+4,CC+3) = "|";
        prettyBoard(RR+1,CC+1) = string( floor(solvedTileRow(v1)/10) );
        prettyBoard(RR+1,CC+2) = string( rem(solvedTileRow(v1),10) );
        prettyBoard(RR+4,CC+1) = string( floor(solvedTileRow(v2)/10) );
        prettyBoard(RR+4,CC+2) = string( rem(solvedTileRow(v2),10) );
    end
end

for ii = 1:size(prettyBoard,1)
    for jj = 1:size(prettyBoard,2)
        fprintf("%1c", prettyBoard(ii,jj));
    end
    fprintf("\n");
end
