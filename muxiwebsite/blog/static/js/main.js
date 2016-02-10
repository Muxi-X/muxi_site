(function(){
	// using regex to get the post id 
	var pid = window.location.href.match(/post\/([0-9])+/)[1];
	var $likeBtn = $('svg.like');
	// flag, prevent from sending request more than once
	var liked = false;
	var url = '/api/blog/' + pid + '/likes/';
	$likeBtn.click(function(){
		if (liked) return;
		$.post(url).done(function(){
			liked = !liked;
			$likeBtn.parent().addClass("clicked");
		})
	})
})();