function ret = antidiag_mtx(M)

    % Size of matrix
    n = size(M, 1);
    m = size(M, 2);
    
    % Get offset for diag index
    indx = -n;

    % Get all diagonals
    if min(size(M)) == 1
        warning('Passed a vector, not a matrix');
    end
    for i = 1:(n+m-1);
        ret{i} = diag(M, indx + i);
    end
end