$(document).ready(function(){
	var width = $('#bgimg').width();
	var height = $('#bgimg').height();
	var halfWidth = width / 2;
	var halfHeight = height /2;
	$('#bgimg').mousemove(function(e){
		var x = e.clientX;
		var y = e.clientY;

		var rx = (x - halfWidth) / 100;
		var ry = (halfHeight - y) / 90;

	

		$(this).css("background-position",rx + "px " + ry + "px");
	});
});