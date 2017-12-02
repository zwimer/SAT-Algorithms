**!! RENDER MARKDOWN !!**
**!! STOP RENDERING !!**
**!! READ MORE BELOW !!**
**!!! BLOG ITEM DELIMITER !!!**
// Define the render commands and delimiter

// Title
IP to SAT

**!!! BLOG ITEM DELIMITER !!!**

// Title description
Testing with digital tomography

**!!! BLOG ITEM DELIMITER !!!**

// Date of post 
October 18, 2017

**!!! BLOG ITEM DELIMITER !!!**
**!! RENDER MARKDOWN !!**
// Note: Markdown should always be rendered first as latex does not respect whitespace

// Body
Digital tomography can be solved efficiently, comparatively, via IP, a known NP-Complete problem. Since IP is NP-Complete, it can be reduced to SAT; so the question is: is it faster? Short answer: No. 

**!! READ MORE BELOW !!**

<p>Long answer: Not even close. IP can be thought of as a set of cardinality constraints. That is, a set of constraints looking like the following: <span class="math display">\[ {\vec \alpha}{\vec x} = \alpha_1 x_1 + ... + \alpha_nx_n = C \in {\mathbb R}, {\vec x} \in {\mathbb R}^n \]</span> That is to say, an linear combination <span class="math inline">\({\vec \alpha}\)</span> of our optimization variable <span class="math inline">\({\vec x}\)</span> results in some integer constant <span class="math inline">\(C\)</span>. In our case, <span class="math inline">\({\vec \alpha} \in \{0, 1\}^n\)</span>.</p>
<p>To convert this into SAT, there is a rather trivial formula. For each cardinality constraint, we construct a number of constraints; this number is the number of different states <span class="math inline">\(Z\)</span> can possibly be in where <span class="math inline">\(Z \in {\mathbb Z}^C\)</span> such that <span class="math display">\[Z \in {\mathbb Z}^C,\ Z = \{ Z_i \in ({\mathbb Z} \cup [1,n])\ |\ Z_i \neq Z_k,\ \forall i,k \} \]</span> Our new constraints thus are in the form: <span class="math display">\[ \bigwedge\limits_{i \in Z} x_i \wedge \bigwedge\limits_{i \in (({\mathbb Z} \cup [1, n]) \backslash Z) } \neg x_i\]</span></p>
<p>Obviously, this converts each constraint into an NP problem itself, and thus should be avoided... A polynomial run time algorithm, resulting in <span class="math inline">\( O(N \log(N) ) \)</span> constraints, where <span class="math inline">\(N\)</span> is the number of cardinality constraints, could be implemented as well, but it is less trivial to explain, read about it here:</p>

> Bailleux, O., and Boufkhad, Y. 2003. Efficient CNF encoding of Boolean cardinality constraints. In Rossi, F., ed., Principles and Practice of Constraint Programming – CP 2003: 9th International Conference, CP 2003, Kinsale, Ireland, September 29 – October 3, 2003, Proceedings, volume 2833 of Lecture Notes in Computer Science, 108–122. Springer-Verlag. 

After implementing an algorithm to do this conversion, I decided to test my results; and... they were less than joyous. What took my tomography problem a fraction of a second, took this nearly a minute... and that was for small images...

**!!! BLOG ITEM DELIMITER !!!**

// Edits of this post
0
