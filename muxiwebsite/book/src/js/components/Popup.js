// poppup.js
// by StephenLiu

$(document).ready(function(){
	function displayNew(){
		var sHeight = document.documentElement.scrollHeight;
		var sWidth = document.documentElement.scrollWidth;
		//可视区域
		var wHeight = document.documentElement.clientHeight;

		var mask = document.createElement('div');
		mask.id = "mask";
		mask.style.height = sHeight + "px";
		mask.style.width = sWidth + "px";
		document.body.appendChild(mask);
		
		//关闭
		var close = document.getElementById('close');
		var cancel = document.getElementById('cancel');
		cancel.onclick = mask.onclick = close.onclick = function(){
		document.body.removeChild(mask);
		$('#search_border,#content_log').slideUp('fast');
		};
	};
	//添加事件绑定
	$('#search').click(function(){
		$('#search_border').slideDown('fast');
		displayNew();
	});
	$('#logon').click(function(){
		$('#content_log').slideDown('fast');
		displayNew();
	});

});
