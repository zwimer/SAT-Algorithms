function ret = get_diag_mtx( rows, cols, anti_diag )

    % Create a 3d cell where the 3rd dimension is vector's x,y location
    mtx = zeros(rows, cols, 2);
    for i = 1:rows; for k = 1:cols; mtx(i,k, :) = [i,k]; end; end

    % Flip if needed
    if ~anti_diag; mtx = flipud(mtx); end

    % Diagonalize it
    diag = antidiag_3d_mtx(mtx);
    
    % Convert form to list of lists
    for i = 1:length(diag)
        for k = 1:length(diag{i}{1})
            ret{i}{k} = [ diag{i}{1}(k), diag{i}{2}(k) ];
        end
    end
end

function ret = antidiag_3d_mtx(M)

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
        ret{i} = { diag(M(:,:,1), indx + i), diag(M(:,:,2), indx + i) };
    end
end