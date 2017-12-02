// Page number
var page_number = 1;
var blogs_per_page = 5;
var blog_list_split = 0;

// Generate the footer
function generate_footer( increase_page_num_by, force = false, update_blog = true ) {

	// Alter the page number
	old_page_num = page_number;
	page_number += increase_page_num_by

	// The types of buttons
	var enabled_class = 'w3-button w3-black w3-padding-large w3-margin-bottom';
	var disabled_class = 'w3-button w3-black w3-disabled w3-padding-large w3-margin-bottom';

	// The classes of the buttons
	var prev_class = enabled_class;
	var next_class = enabled_class;

	// The max page number
	var max_page_num = Math.ceil( blog_list_split.length / blogs_per_page );

	// Disable buttons if needed
	if ( page_number <= 1 ) {
		page_number = 1;
		prev_class = disabled_class;
	}
	if ( page_number >= max_page_num ) {
		page_number = max_page_num;
		next_class = disabled_class;
	}

	// If the page number did not change, do nothing
	if ( (force === false) && (old_page_num === page_number) ) {
		return;
	}

	// Create the footer
	var footer = '\n';
	footer += '	<button onclick="generate_footer(-1)" class="' + prev_class + '">Previous</button>\n';
  	footer += '	<button onclick="generate_footer(1)" class="' + next_class + '">Next »</button>\n';
	footer += '	<p>Copyright &copy; zwimer.com 2017 </p>\n'

	// Set the footer
	document.getElementById( 'CustomFooter' ).innerHTML = footer;

	// Change the blog list
	if (update_blog === true) {
		generate_blog("Blog-List")
	}
}
