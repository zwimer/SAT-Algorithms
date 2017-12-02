**!! RENDER MARKDOWN !!**
**!! STOP RENDERING !!**
**!! READ MORE BELOW !!**
**!!! BLOG ITEM DELIMITER !!!**
// Define the render commands and delimiter

// Title
Minimum bad matrix

**!!! BLOG ITEM DELIMITER !!!**

// Title description
How small can we go before we become deterministic

**!!! BLOG ITEM DELIMITER !!!**

// Date of post 
October 23, 2017

**!!! BLOG ITEM DELIMITER !!!**
// Note: Markdown should always be rendered first as latex does not respect whitespace

// Body
The question is as follows: How small can we make a (roughly square) matrix such that it cannot be perfectly solved via this algorithm? To start off, and to avoid wasting computations, I asked myself this very question from a simplistic point of view: How many variables must we solve for and how many constraints do we have?

**!! READ MORE BELOW !!**

Simply put, there are <span class="math inline">\( n \times m \)</span> variables. As for constraints, we have <span class="math inline">\( n + m + 2(n + m - 1) \)</span>. Since we would like the matrix to be roughly square, we let <span class="math inline">\(m = n\)</span>, thus we simply had to find when <span class="math inline">\( n*n < 4n - 2\)</span>. From here, since our size must be rounded up to the nearest integer, we can find that <span class="math inline">\( n \geq 4\)</span>. As such, I chose to use <span class="math inline">\( 4 \times 4 \)</span> matrix as my starting point.

From this point onwards, I chose to find the answer with code. To do this, I simply simply wrote a program to generate a large number of random <span class="math inline">\(n \times n\)</span> matrix, then ran this through my tomography solver. If any of these matricies were not reconstructed perfectly, then the program stopped and printed the matrix which couldn't be reconstructed perfectly, then tried again with a large number of smaller matricies. If however the program could not find any such matrix, it tries again with a large number of matricies of an increased the size.

When I ran this program, it found a <span class="math inline">\(4 \times 4\)</span> matrix which could not be reconstructed perfectly, shown below:

<span class="math display">
	\[\begin{bmatrix}
        1 &amp; 1 &amp; 0 &amp; 0 \\
        0 &amp; 0 &amp; 1 &amp; 1 \\
        1 &amp; 0 &amp; 0 &amp; 0 \\
        1 &amp; 0 &amp; 1 &amp; 0
    \end{bmatrix}\]
</span>

This program then moved down to check for <span class="math inline">\(3 \times 4\)</span> (roughly square) matricies which would not be solvable, but was unable to find any. In this case, the 'large number' of matricies used was 100,000,000. Thus I have concluded that the <span class="math inline">\(4 \times 4\)</span> matrix is the smallest, roughly square, matrix which cannot necessarily be reconstructed perfectly.

**!!! BLOG ITEM DELIMITER !!!**

// Edits of this post
0
