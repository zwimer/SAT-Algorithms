function [ row, col, diag, anti ] = image_to_constraints(A) 

    % Dimensions
    n = size(A, 1);
    m = size(A, 2);

    % Error checking
    msg = 'A is not a binary image! This will cause issues! Quitting...';
    for i = 1:n; for k = 1:m; if (A(i,k) ~= 0) && (A(i,k) ~= 1); warning(msg); return; end; end; end
    
    % Row sums
    for i = 1:n
        row(i) = sum(A(i,:));
    end
    
    % Columns sums
    for i = 1:m
        col(i) = sum(A(:,i));
    end

    % Anti diag sums
    ad = antidiag_mtx(A);
    for i = 1:length(ad)
        anti(i) = sum(ad{i});
    end
    
    % Diag sums
    A = flipud(A);
    ad = antidiag_mtx(A);
    for i = 1:length(ad)
        diag(i) = sum(ad{i});
    end

end