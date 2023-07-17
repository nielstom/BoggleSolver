clear; clc;

% CONFIGURE
candidateVals = [1 3  4 6:9 11];  % Don't include > 10 elements (perms crashes)
totalVal = 31;

N = numel(candidateVals);

m = [];
for ii = 0:N
    inputVec = [true(1, ii), false(1, N-ii)];
    m = [m; unique(perms(inputVec), 'rows')];
end
m = logical(m);

goodAns = [];
for ii = 1:size(m,1)
    c = candidateVals .* m(ii,:);
    if sum(c) == totalVal
        goodAns(end+1,:) = c;
    end
end

disp(goodAns)

printYes = false;
for jj = 1:size(goodAns,2)
    if all(goodAns(1,jj) == goodAns(:,jj))
        printYes = true;
        break;
    end
end
if printYes
    disp("yes: reducable")
else
    disp("no: not reducable")
end

