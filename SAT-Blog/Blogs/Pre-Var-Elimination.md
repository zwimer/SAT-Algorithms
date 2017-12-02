**!! RENDER MARKDOWN !!**
**!! STOP RENDERING !!**
**!! READ MORE BELOW !!**
**!!! BLOG ITEM DELIMITER !!!**
// Define the render commands and delimiter

// Title
Removing variables early

**!!! BLOG ITEM DELIMITER !!!**

// Title description
An attempt to decrease run time

**!!! BLOG ITEM DELIMITER !!!**

// Date of post 
October 29, 2017

**!!! BLOG ITEM DELIMITER !!!**
**!! RENDER MARKDOWN !!**
// Note: Markdown should always be rendered first as latex does not respect whitespace

// Body
<p>If I were to give you the following matrix, and ask you if you could simplify the following digital tomography problem associated with it, what would you do? <span class="math display">\[ A = \begin{bmatrix} 1 &amp; 1 &amp; 1 \\ 0 &amp; 1 &amp; 0 \\ 1 &amp; 0 &amp; 0 \end{bmatrix} \]</span></p>
<p>In this problem, you are only given the following information: <span class="math display">\[ row sum = \begin{bmatrix} 3 \\ 1 \\ 1 \end{bmatrix}\ column sum = \begin{bmatrix} 2 \\ 2 \\ 1 \end{bmatrix} \]</span></p>

**!! READ MORE BELOW !!**

<p>To start, notice that the top row is all 1s. We can determine this by looking at the first entry in the row sum vector. So then, why bother solving for those variable? Instead, just mark down that we know them. In the following matrix, let '?' represent an unknown value, and a number represent a known value. Well, since we can trivially determine that the fist row contains only 1s, we would know the following: <span class="math display">\[ A = \begin{bmatrix} 1 &amp; 1 &amp; 1 \\ ? &amp; ? &amp; ? \\ ? &amp; ? &amp; ? \end{bmatrix} \]</span></p>

<p>But what now? Well, notice how the last entry in the column sum vector has a value of 1. In other words, there is only one 1 in the last column of <span class="math inline">(A)</span>. But wait! We know that the first element of said column is a 1, so trivially, the other elements must be 0! Thus, we know that <span class="math display">\[ A = \begin{bmatrix} 1 &amp; 1 &amp; 1 \\ ? &amp; ? &amp; 0 \\ ? &amp; ? &amp; 0 \end{bmatrix} \]</span></p>
<p>With a simple analysis of the problem thus, we have reduced the number of variable we must solve for from 9 to 4! If we were to do the following with diagonal and anti-diagonal sums in fact, there exists no matrix of size <span class="math inline">(3 \times 3)</span> which couldn't be trivially solved like this!</p>
<p>So, instead of throwing <span class="math inline">(nm)</span> variables at our IP solver, what if we were to first run such an analysis on our input? We could implement the following trivial algorithm:</p>

1. Do (while something was learned the previous iteration)
   1. The following is done for row sums, but should also be done wlog to column, diagonal, and anti-diagonal sums
   3. `for i in range(row_sums):`
      1. Let `known` = variables in current row whose value was already determined
      1. if `row_sum[i] - sum(known) == 0`
         1. Mark each unknown variable in `row[i]` to be known with the value being 0
      2. else if `row_sum[i] - sum(known) == len(row[i]) - len(known))`
         1. Mark each unknown variable in `row[i]` to be known with the value being 1
      3. else
         1. There is nothing to learn from this iteration

If, each time the main loop runs, we process rows, then columns, diagonals, then anti-diagonals, this simply algorithm can quickly remove a size-able number of variables (depending on the image).

Unfortunately, after testing, there is no noticeable speed change on large or small images. Upon further inspection of my IP solver, it seems to not brute force a solution, and likely does remove trivial cases before processing anyway.

**!!! BLOG ITEM DELIMITER !!!**

// Edits of this post
0
