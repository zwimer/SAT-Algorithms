function ret = Knuth()
   
    % Sums
    row = [ 1, 0, 13, 6, 12, 7, 19 ];
    col = [ 4, 3, 3, 4, 1, 6, 1, 3, 3, 3, 5, 1, 1, 5, 1, 5, 1, 5, 1, 1, 1 ];
    diag = [ 0, 0, 1, 2, 2, 3, 2, 3, 3, 2, 3, 3, 4, 3, 2, 3, 3, 3, 4, 3, 2, 2, 1, 1, 1, 1, 1 ];
    anti = [ 0, 0, 0, 0, 0, 1, 3, 3, 4, 3, 2, 2, 2, 3, 3, 4, 2, 3, 3, 3, 3, 3, 4, 3, 2, 1, 1 ];

    % So, his notation is the reverse of mine...
    anti= fliplr(anti);

    % Sove and display the result
    ret = solve_tomo(row, col, diag, anti)
end