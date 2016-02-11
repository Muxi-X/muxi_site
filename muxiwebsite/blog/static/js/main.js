(function(){
	var $likeBtn = $('svg.like');
	var cookieFlag = Cookies.get('liked');
	if (cookieFlag){
		$likeBtn.parent().addClass("clicked");
	}
	// using regex to get the post id 
	var pid = window.location.href.match(/post\/([0-9])+/)[1];
	// flag, prevent from sending request more than once
	var liked = false;
	var url = '/api/blog/' + pid + '/likes/';
	$likeBtn.click(function(){
		if (liked || cookieFlag) return;
		$.post(url).done(function(){
			liked = !liked;
			Cookies.set('liked', 'true', { expires: 7 });
			$likeBtn.parent().addClass("clicked");
		})
	})
})();