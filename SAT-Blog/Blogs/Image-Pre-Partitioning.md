**!! RENDER MARKDOWN !!**
**!! STOP RENDERING !!**
**!! READ MORE BELOW !!**
**!!! BLOG ITEM DELIMITER !!!**
// Define the render commands and delimiter

// Title
Image Pre-Partitioning

**!!! BLOG ITEM DELIMITER !!!**

// Title description
Splitting an image then reconstructing each section

**!!! BLOG ITEM DELIMITER !!!**

// Date of post 
October 10, 2017

**!!! BLOG ITEM DELIMITER !!!**
// Note: Markdown should always be rendered first as latex does not respect whitespace

// Body
If you read my earlier blogs, you know that I tried to 'downscale' images. Basically, I split up each image into many different chunks; in each chunk we set a variable to either true or false depending on whether or not there were more black or white pixels in the chunk. Using this information as additional constraints led to a significant increase in quality, but also an increase if run time. What if we instead took each chunk and used digital tomography to reconstruct that section of the image?

**!! READ MORE BELOW !!**

NP problems often have an order notation of <span class="math inline">\(O(2^N)\)</span>. As such, decreasing <span class="math inline">\(N\)</span> by a factor of <span class="math inline">\(k\)</span> massively reduces the run time to <span class="math inline">\(O(k2^{\frac{N}{k}})\)</span>, as we now must solve <span class="math inline">\(k\)</span> problems, each of complexity <span class="math inline">\(O(2^{\frac{N}{k}})\)</span>. By running digital tomography on each image section, which should thus be faster; furthermore, to end we simply stitch all the images together in polynomial time. However: there is a tradeoff. If this were to be used as a compression method, the problem is that this method requires more information to be given. For example, the row sums of each sub-image must be saved instead of simply the row sum of the collective image.

When running this on the elehpant.bmp image, with block sizes of <span class="math inline">\(40\ \times\ 36\)</span>, I get 11.3194444444% image, which takes .87 seconds to run
**!! RENDER MARKDOWN !!**

![Elephant-40-36](https://www.zwimer.com/SAT-Algorithms/SAT-Blog/Blogs/figs/Image-Pre-Part/Elephant_40_36.bmp)

**!! STOP RENDERING !!**
When running this on the elehpant.bmp image, with block sizes of <span class="math inline">\(20\ \times\ 36\)</span>, I get 1.18055555556% image, which takes .38 seconds to run.
**!! RENDER MARKDOWN !!**

![Elephant-20-36](https://www.zwimer.com/SAT-Algorithms/SAT-Blog/Blogs/figs/Image-Pre-Part/Elephant_20_36.bmp)

**!! STOP RENDERING !!**
When running this on the elehpant.bmp image, with block sizes of <span class="math inline">\(8\ \times\ 9\)</span>, I get 0.27777777778% image, which takes .72 seconds to run. This same image, when run on my previous partitioning program took over an hour before I finally stopped the calculation.
**!! RENDER MARKDOWN !!**

![Elephant-8-9](https://www.zwimer.com/SAT-Algorithms/SAT-Blog/Blogs/figs/Image-Pre-Part/Elephant_8_9.bmp)

The actual elephant.bmp is here:

![Elephant](https://www.zwimer.com/SAT-Algorithms/SAT-Blog/Blogs/figs/Image-Pre-Part/Elephant.bmp)

For more examples, click [here](https://github.com/zwimer/SAT-Algorithms/tree/master/SAT-Blog/Blogs/figs/Image-Pre-Part/Examples)

**!!! BLOG ITEM DELIMITER !!!**

// Edits of this post
1
