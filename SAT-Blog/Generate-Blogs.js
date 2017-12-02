//*************************************************************//
//*                                                           *//
//*                         Globals                           *//
//*                                                           *//
//*************************************************************//

// *** Settings ***

// The div storing all the blogs
var blogs_output_div;

// The folder containing the un-rendered blog markdown files
var blog_folder;

// The file containing the format for the blog post
var format_file;

// *** Automatically set / constants ***

// Holds info about each blog, used by the READ MORE button
// Blog file name mapped to the object it holds
// Structure of each object: { "Beginning": xyz, "Continued" }
var read_more_dict_dict = {};
var read_more_key = "read-more";
var marker_key = "marker";

// Contains the format of a blog and a marker
// denoting where the button info should be put
var format_list = [];
var button_marker = "";

// A dict mapping a filename to an index 
var ready_for_display_dict = {};

// Page number
var page_number = 1;
var blogs_per_page = 5;
var blog_list_split = 0;

//*************************************************************//
//*                                                           *//
//*                        Functions                          *//
//*                                                           *//
//*************************************************************//


// A function used to read a file
function read_file(url, obj) {
	var xhttp = new XMLHttpRequest();
	xhttp.onreadystatechange = function() {
		if (this.readyState == 4 && this.status == 200) {
			obj.internal = this.responseText;
		}
	};
	xhttp.open("GET", url, true);
	xhttp.send();
}

// A function used to set the settings for the blog generation
function set_blog_settings(output_div, blog_folder_in, format_file_in) {

	// The div storing all the blogs
	blogs_output_div = output_div;

	// The folder containing the un-rendered blog markdown files
	blog_folder = blog_folder_in;

	// HTML to encapsulate the blog post
	format_file = format_file_in;
}

// A function used to remove comment lines
function remove_comments(input, comment_type) {
	var lst = input.split("\n");
	var not_comments = [];
	for ( var i = 0; i < lst.length; ++i ) {
		if (lst[i].startsWith(comment_type) === false) {
			not_comments.push(lst[i]);
		}
	}
	return not_comments.join("\n");
}

// Function used to render a chunk of text properly according to it's markers
render_text = function( text, dict, read_more_dict, starting_entry ) {

	// The output
	var ret = "";

	// Continue while the more of text should render
	for ( var brk = false; text.length > 0;  ) {

		// If a render marker was found, break
		for ( var key in dict ) {
			if ( text.startsWith(key) ) { brk = true; break; }
		}
		if (brk === true) { break; }

		// If the read more marker was found
		if (text.startsWith(read_more_dict[marker_key])) {

			// If everything should be displayed, remove this marker and continue
			if ( read_more_dict[read_more_key] ) {
				text = text.slice(read_more_dict[marker_key].length);
				continue;
			}

			// Otherwise, add an ellipsis, then clear text and break
			else {
				ret += " ...";
				text = "";
				break;
			}
		}

		// If the read more marker was not found
		// then record the next character in text
		else {
			ret += text[0];
			text = text.slice(1);
		}
	}

	// Render it if there is anything to render
	if (ret) { ret = dict[starting_entry](ret); }

	// Remove the marker and recurse if needed
	if ( text.trim().length ) {
		text = text.slice(key.length).trim();
		ret += render_text( text, dict, read_more_dict, key );
	}

	// Return the result
	return ret;
}

// Given the blog text, render the markdown, format it as a blog, then add the blog. 
function add_and_format_blog(filename, blog_info) {

	// Determine the delimiters of this file
	var blog_split_by_line = blog_info.split("\n");
	var md_render_marker = blog_split_by_line[0];
	var no_render_marker = blog_split_by_line[1];
	var read_more_marker = blog_split_by_line[2];
	var delimiter = blog_split_by_line[3];

	// Split the blog up according to the delimiter
	var split_blog = blog_info.split(delimiter);
	split_blog.shift()

	// Error checking
	if (md_render_marker === no_render_marker) {
		alert("Error: " + filename + " has identical render markdown and no render markers!");
		return;
	}
	else if (format_list.length < 2 || split_blog.length < 1) {
		alert("Error: " + filename + " has too few delimited fields!");
		return;
	}
	else if (format_list.length !== (1 + split_blog.length)) {
		alert("Error: " + filename + " has the wrong number of delimited fields!");
		return;
	}

	// Remove comment lines
	for ( var i = 0; i < split_blog.length; ++i ) {
		split_blog[i] = remove_comments(split_blog[i].trim(), "//").trim()
	}
	for ( var i = 0; i < format_list.length; ++i ) {
		format_list[i] = remove_comments(format_list[i].trim(), "//").trim()
	}

	// A dictionary mapping markers to their rendering functions
	var dict = { };
	dict[md_render_marker] = function(x) { return window.markdownit({"html":true}).render(x); }
	dict[no_render_marker] = function(x) { return x; }

	// A dict containing the body of the blog split into the read less
	// and read more sections along with the marker splitting the two sections
	// If it exits, load it, otherwise initialize it
	var read_more_dict = { }; 
	if ( filename in read_more_dict_dict ) {
		read_more_dict = read_more_dict_dict[filename];
	}
	else {
		read_more_dict[marker_key] = read_more_marker;
		read_more_dict[read_more_key] = false;
	}

	// Render markdown as required
	for ( var i = 0; i < split_blog.length; ++i ) {
		if (!split_blog[i].trim()) { continue; }
		split_blog[i] = render_text( split_blog[i].trim(), dict, read_more_dict, no_render_marker );
	}			

	// Add the read more dict to the global array
	read_more_dict_dict[filename] = read_more_dict;

	// Create the button's script
	for ( var btn_indx = 0; i < format_list.length; ++btn_indx ) {
		var tmp = format_list[btn_indx].split(button_marker);
		if ( tmp.length > 1 ) {
			var edited_button = tmp[0].trim() + "\"toggle_read_more('" + filename + "')\" ><b>READ ";
			var add = "MORE »"; if (read_more_dict_dict[filename][read_more_key]) { add = "LESS «"; }
			edited_button += add + "</b>" + tmp[1];
			break;
		}
	}

	// Interweave the blog info with the formatting items to create the new blog
	// Special case for creating the button
	var new_blog = format_list[0];
	for ( var i = 0; i < split_blog.length; ++i ) {
		if ( (i+1) === btn_indx ) {
			new_blog += split_blog[i] + edited_button;
		}
		else {
			new_blog += split_blog[i] + format_list[i+1];
		}
	}

	// Update the blog entry
	var indx = ready_for_display_dict[filename];

	// Display and render the new blog
	document.getElementById("BlogDiv" + indx).innerHTML = new_blog;
	var id = "BlogDiv" + indx
	RenderTex(id)
}

// Create a blog from a filename
// Takes the file to be blogged as the argument
function create_blog_post(filename) {

	// Read the blog file
	var blog_text = { internal:"" };
	read_file(blog_folder + filename, blog_text);

	// Wait for and blog file to have been read, then add the blog
	function wait_for_vars() {
		if ( blog_text.internal ) {
			add_and_format_blog(filename, blog_text.internal);
		}
		else {
			setTimeout(wait_for_vars, 50);
		}
	}
	wait_for_vars();
}

// A function called when the read more / read less button is clicked
function toggle_read_more(filename) {
	read_more_dict_dict[filename][read_more_key] = ! read_more_dict_dict[filename][read_more_key];
	create_blog_post(filename);
}

// A function to load all blogs in a list, ignores empty entries
function load_blogs(blog_names) {

	// Clear the blog output div
	document.getElementById(blogs_output_div).innerHTML = "";

	// Create the div to hold the blog
	for ( var i = 0; i < blog_names.length; ++i ) {
		var id = "BlogDiv" + i
		var dv = '<div id="' + id + '"></div>';
		var tmp = document.getElementById(blogs_output_div).innerHTML;
		document.getElementById(blogs_output_div).innerHTML = dv + tmp;
		ready_for_display_dict[blog_names[i]] = i;
	}

	// Create each post
	for ( var i = 0; i < blog_names.length; ++i ) {
		if (blog_names[i]) {		
			create_blog_post(blog_names[i]);
		}
	}
}

// Decide which blogs to load and load them
function load_current_page() {
	var end = page_number * blogs_per_page;
	blog_list_split.reverse();
	blogs = blog_list_split.slice( end - blogs_per_page, end );
	blog_list_split.reverse();
	blogs.reverse();
	load_blogs( blogs );
}

// A function used to load all blogs listed in the file blog_list_file
function generate_blog(blog_list_file) {

	// Read the blog list
	var blog_list = { internal:"" };
	read_file(blog_folder + blog_list_file, blog_list);

	// Read the blog format, the HTML to encapsulate the blog post
	var blog_format_obj = { internal:"" };
	read_file(format_file, blog_format_obj);

	// Wait for the blog list to have been read
	function wait_for_blog_list() {
		if ( blog_list.internal && blog_format_obj.internal ) {

			// Determine the format delimiter, button marker, and split the format up
			var format_split_by_line = blog_format_obj.internal.split("\n")
			button_marker = format_split_by_line[0];
			var delimiter = format_split_by_line[1];
			format_list = blog_format_obj.internal.split(delimiter);
			format_list.shift()

			// Store the split blog list
			blog_list_split = blog_list.internal.split("\n");
			if (blog_list_split[blog_list_split.length - 1] === "") {
				blog_list_split.splice(-1);
			}

			// Load all blogs listed
			load_current_page()
		}
		else {
			setTimeout(wait_for_blog_list, 50);
		}
	}

	// Only read blogs if needed
	if (blog_list_split === 0) {
		wait_for_blog_list();
	}

	// Otherwise, just load the blogs
	else {
		load_current_page()
	}
}
