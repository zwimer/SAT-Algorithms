**!! RENDER MARKDOWN !!**
**!! STOP RENDERING !!**
**!! READ MORE BELOW !!**
**!!! BLOG ITEM DELIMITER !!!**
// Define the render commands and delimiter

// Title
Size vs error

**!!! BLOG ITEM DELIMITER !!!**

// Title description
A comparison of the size of the matrix and the error in reconstructing it.

**!!! BLOG ITEM DELIMITER !!!**

// Date of post 
November 8, 2017

**!!! BLOG ITEM DELIMITER !!!**
// Note: Markdown should always be rendered first as latex does not respect whitespace

// Body
**!! RENDER MARKDOWN !!**
To see the effects of the size of a matrix to it's error, I decided to write a program which would do the following

1. Fix a variable K
2. `for each n in range(4, 25 + 1)`
   1. `for each k in range(K)`
      1. Generate a matrix of size N x N
      2. Run the tomography program on the matrix
      3. Record the error
   2. Create a histogram of the error distributions for matricies of size N x N
3. Place each histogram on the same 3d graph

**!! READ MORE BELOW !!**

**!! STOP RENDERING !!**
Once I did this, here are a the results:

<div style="text-align: center;">
   <img src="https://github.com/zwimer/zwimer.github.io/blob/master/SAT-Blog/Blogs/figs/Size-Vs-Error/fig1.png?raw=true" style="max-width: 100%; height: auto;" alt="Alt text is required" />
</div>

**!!! BLOG ITEM DELIMITER !!!**

// Edits of this post
0
