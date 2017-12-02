function A = create_A(rows, cols)
    % rows = number of rows in origonal matrix
    % columns = number of columns in origonal matrix

    % A is sparse
    A = sparse([]);

    % Populate A for rows
    num_rows = 0;
    for i = 1:rows
        for k = 1:rows
            if i == k
                A(i + num_rows, (1:cols) + (k-1)*cols) = 1;
            end
        end
    end
    
    % Populate A for columns
    num_rows = num_rows + rows;
    for i = 1:cols
        for k = 1:rows
            A(i + num_rows, (k-1)*cols + i) = 1;
        end
    end
    
    % Populate A for diagonals
    num_rows = num_rows + cols;
    diag_mtx = get_diag_mtx(rows, cols, false);
    for i = 1:length(diag_mtx)
        for k = 1:length(diag_mtx{i})
            coord = diag_mtx{i}{k};
            A(i + num_rows, cols*(coord(1)-1) + coord(2) ) = 1;
        end
    end
    
    % Populate A for anti-diagonals
    num_rows = num_rows + length(diag_mtx);
    diag_mtx = get_diag_mtx(rows, cols, true);
    for i = 1:length(diag_mtx)
        for k = 1:length(diag_mtx{i})
            coord = diag_mtx{i}{k};
            A(i + num_rows, cols*(coord(1)-1) + coord(2) ) = 1;
        end
    end
end