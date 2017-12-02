**!! RENDER MARKDOWN !!**
**!! STOP RENDERING !!**
**!! READ MORE BELOW !!**
**!!! BLOG ITEM DELIMITER !!!**
// Define the render commands and delimiter

// Title
Proof of Concept

**!!! BLOG ITEM DELIMITER !!!**

// Title description
A trivial test of theory

**!!! BLOG ITEM DELIMITER !!!**

// Date of post 
September 18, 2017

**!!! BLOG ITEM DELIMITER !!!**
**!! RENDER MARKDOWN !!**
// Note: Markdown should always be rendered first as latex does not respect whitespace

// Body
After reading up a little about how a trivial case of digital tomography is an SAT problem, I decided to test it / implement a solver to help deepen my understanding of this topic. To begin, I simply made a simplistic python program that can load a text file representing an image, calculate row sums, column sums, diagonal sums, and antidiagonal sums. I did this so I could create test images used as input in the program to come.

**!! READ MORE BELOW !!**
**!! STOP RENDERING !!**

<p>The math of this problem is actually fairly simplistic. Our image can be represented as an array of booleans. Let our row constraints be an array with indexing starting at 1. Now given our row constraints, we can apply them as follows:</p>
<p><span class="math display">\[ \text{ Given } \begin{bmatrix} x_{1,1} &amp; x_{2,1} &amp; ... &amp; x_{n,1} \\ x_{1,2} &amp; x_{2,2} &amp; ... &amp; x_{n,2} \\ \vdots &amp; \vdots &amp; \ddots &amp; \vdots \\ x_{1,m} &amp; x_{2,m} &amp; ... &amp; x_{n,m} \end{bmatrix}\]</span> <span class="math display">\[\forall k \in \{1,\ 2,\ ...,\ m\}, \text{ we require: } \sum_{i=1}^n x_{i,k} = row\_sum[k]  \]</span></p>
<p>We can repeat this same idea for our column sums, diagonal sums, and antidiagonal sums. This gives us a system of linear equations. Now, simply solving this as a LP problem would allow our variables <span class="math inline">\(x_{i,j}\)</span> to be decimals. But we are working with booleans, so we add the final restriction that <span class="math inline">\(x_{i,j} \in \{0,1\}, \forall i,k \in n,m\)</span>. This extra restriction converts our LP problem to an integer linear programming, ILP, problem.</p>
<p>As an ILP problem is NP-complete, it can be solved with a simply SAT solver. However, doing this could allow for a technically correct solution which may look nothing like our answer. As such, I decided to add an objective function to maximize while solving this ILP problem. The objective function was simply to maximize the <span class="math inline">\(x_{i,j}, \forall i,j\)</span> such that <span class="math inline">\(x_{i,j}\)</span> in the original image is true.</p>
<p>Instead of implementing my own ILP solver / optimizer, I simply downloaded the python library PuLP. I implemented the math above in python, and then tested it on the test cases above. And to my enjoyment, the output image matched the input image exactly for every image I tested!</p>

**!!! BLOG ITEM DELIMITER !!!**

// Edits of this post
0
