**!! RENDER MARKDOWN !!**
**!! STOP RENDERING !!**
**!! READ MORE BELOW !!**
**!!! BLOG ITEM DELIMITER !!!**
// Define the render commands and delimiter

// Title
P-Time Failure

**!!! BLOG ITEM DELIMITER !!!**

// Title description
Approximating IP with LP.

**!!! BLOG ITEM DELIMITER !!!**

// Date of post 
October 3, 2017

**!!! BLOG ITEM DELIMITER !!!**
// Note: Markdown should always be rendered first as latex does not respect whitespace

// Body
Last week I found myself wondering: What if I could approximate the integer programming problem with linear programming? To find out, I simply removed the constraint from <span class="math inline">\(A{\vec x}={\vec b}\)</span> that for <span class="math inline">\(x_i \in {\vec x}\)</span>, <span class="math inline">\(x_i \in \{ 0, 1 \}\)</span>. Doing so was a relaxation of this problem

**!! READ MORE BELOW !!**

Unfortunately, my luck with this was not very good. As it turned out, this approximation turned out to be fairly poor. While this function was approximate to solve each problem significantly faster, the errors given ended up being substantially larger. The following is done with each block size (see previous blogs) being the size of the image itself.

**!! RENDER MARKDOWN !!**

For the Jagged-A image, 12% total error (black and white pixels) was found.

![Jagged-A](https://www.zwimer.com/SAT-Algorithms/SAT-Blog/Blogs/figs/P-Time-Fail/Jagged_A.bmp)

Became:

![Jagged-A-error](https://www.zwimer.com/SAT-Algorithms/SAT-Blog/Blogs/figs/P-Time-Fail/Jagged_A_5_5.bmp)

For the elephant image, 16.2% total error was found.

![Elephant](https://www.zwimer.com/SAT-Algorithms/SAT-Blog/Blogs/figs/P-Time-Fail/Elephant.bmp)

Became:

![Elephant-error](https://www.zwimer.com/SAT-Algorithms/SAT-Blog/Blogs/figs/P-Time-Fail/Elephant_80_36.bmp)

For the cat2 image, 49.88% total error was found.

![cat2](https://www.zwimer.com/SAT-Algorithms/SAT-Blog/Blogs/figs/P-Time-Fail/cat2.bmp)

Became:

![cat2-error](https://www.zwimer.com/SAT-Algorithms/SAT-Blog/Blogs/figs/P-Time-Fail/cat2_72_56.bmp)

**!!! BLOG ITEM DELIMITER !!!**

// Edits of this post
1
