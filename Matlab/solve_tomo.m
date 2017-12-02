function ret = solve_tomo( row_c, column_c, diag_c, antidiag_c )
	% Inputs = Comma separated arrays containing sums

    % Get length of each row
    cols = length(column_c);
    rows = length(row_c);
    
    % Create A and b
    Aeq = create_A(rows, cols);
    beq = [ row_c, column_c, diag_c, antidiag_c ]';
    
    % Lower and upper bounds
    lb = zeros(size(Aeq, 2), 1);
    ub = lb + 1;
     
    % All vars must be ints
    intcon = 1:length(lb);
    
    % Solve the problem
    f = zeros(length(lb), 1); A = zeros(size(Aeq)); b = zeros(size(beq));
    [x,fval,exitflag,output] = intlinprog(f, intcon, A, b, Aeq, beq, lb, ub );

    % Check for errors
    if exitflag ~= 1
        msg = sprintf('intlinprog exited with non 1 exit flag: %d !', exitflag);
        warning(msg);
        return;
    end
    
    % Convert x to a matrix
    ret = vec2mat( x, cols );
    
    % Display the image
    imshow(255*(1-ret),'InitialMagnification','fit');
end
