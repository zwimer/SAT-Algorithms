**!! RENDER MARKDOWN !!**
**!! STOP RENDERING !!**
**!! READ MORE BELOW !!**
**!!! BLOG ITEM DELIMITER !!!**
// Define the render commands and delimiter

// Title
**!! RENDER MARKDOWN !!**
# PuLP is broken !!!
**!! STOP RENDERING !!**

**!!! BLOG ITEM DELIMITER !!!**

// Title description
PuLP may ignore bounding and integer constraints.

**!!! BLOG ITEM DELIMITER !!!**

// Date of post 
November 15, 2017

**!!! BLOG ITEM DELIMITER !!!**
// Note: Markdown should always be rendered first as latex does not respect whitespace

// Body
Last week, professor Moorthy asked me to run my digital tomography program on a specific set of inputs. I mis-read these inputs and entered them in, giving my program an un-satisfiable problem; despite this, my program spat out an answer. This answer was obviously incorrect, even at a brief glance it was easy to tell that there were too many white pixels. 

**!! READ MORE BELOW !!**

After exploring this problem, I discovered that this was because PuLP had output numbers such as <span class="math inline">\( -500,000 \)</span>, which did not fall in the set of valid possible values: <span class="math inline">\( \{0, 1\} \)</span>. After further analyzing my code, I discovered the problem was with not my code, but was PuLP !

If you give PuLP an infeasible problem, PuLP will not fail; instead it will ignore any constraints which make it infeasible; from ignoring the upper and lower bounds to using non-integers. The worst part of this is that while PuLP gives warnings to the user for many things, this action is silent; constraints are ignored without informing the user, giving the illusion that the solution returned solves the problem put in as is.

**!! RENDER MARKDOWN !!**
To this end, I created a simplified problem and submitted it along with an issue to PuLP, located [here](https://github.com/coin-or/pulp/issues/157)

**!!! BLOG ITEM DELIMITER !!!**

// Edits of this post
0
