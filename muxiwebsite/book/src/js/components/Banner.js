// banner.js
// by StephenLiu

$(document).ready(function(){
	var boxwidth,boxheight,current,left,boxwidthnum;
	//初始化
	current = 0;
	//获取showbox的高度和宽度
	boxwidth = $(".showbox").css("width");
	boxheight = $(".showbox").css("height");
	boxwidthnum = $(".showbox").width();
	//设置每个box的的宽高
	$(".box").css("height",boxheight);
	$(".box").css("width",boxwidth);
	//设置总的宽度和高度
	$(".slide").width(boxwidthnum*($(".box").length));
	$(".slide").css("height",boxheight);
	//向前
	$("#prev").bind("click",function(){
		prev(current);
	});
	//向后
	$("#next").bind("click",function(){
		next(current);
	});
	//定义向前移动
	function prev(num){

	if (current == 0)
	  {
	  current = $(".box").length-1;
	  $(".slide").animate({left:current*(-boxwidthnum) + 'px'});
	  }
	else
	  {
	  current -= 1;
	  $(".slide").animate({left:current*(-boxwidthnum) + 'px'});

	  }

	};
	//定义向后移动
	function next(num){
	if (current == ($(".box").length-1))
	  {
	  current = 0;
	  $(".slide").animate({left:current*(-boxwidthnum) + 'px'});
	  }
	else
	  {
	  current += 1;
	  $(".slide").animate({left:current*(-boxwidthnum) + 'px'});
	 }
	};
});