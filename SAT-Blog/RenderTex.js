// Encapsulate a function to render tex
function RenderTex(id) {
	MathJax.Hub.Queue( ["Typeset", MathJax.Hub, document.getElementById(id)] );
};
