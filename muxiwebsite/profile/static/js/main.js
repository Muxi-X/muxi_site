/**
 * navigation for users page
 *
 * 
 */
'use strict';

(function() {

	var btn = document.querySelector(".btn");
	var pop = document.querySelector(".pop");
	var cancel = document.querySelector(".cancel");

	btn.addEventListener('click', function () {

		pop.className = pop.className.replace(/hide/, ' ');
		pop.className += ' appear ';
	});
	cancel.addEventListener('click', function () {

		pop.className = pop.className.replace(/appear/, ' ');
		pop.className += ' hide ';
	});
})();


