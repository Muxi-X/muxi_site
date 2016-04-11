$(document).ready(function(){
  banner.initModule();
});

var banner = (function () {
  var
    jqueryMap, 
    toggle;
    
  jqueryMap = {

    $masks  : $('.image_box_mask img'),
    $text_boxes : $('.text_box')
  };
  
  toggle = function (e,diret) {
      var $t = $(e.target),
          $border = $t.parent().prev().prev(),
          $mask = $t.parent().prev(),
          $b = jqueryMap.$text_boxes,
          index = jqueryMap.$masks.index($t);
      if (diret === 0) {
        $t.animate({opacity:'0'},100);
        $border.fadeIn(200).animate({left:'98%'},200);
        $mask.delay(200).animate({width:'98%'},200);
        $b.hide();
        $b.eq(index).show();
      }
      else{
         $(e.target).parent().prev().prev().animate({left:'94%'},100).fadeOut(20);
         $(e.target).parent().prev().animate({width:'94%'},100);
         $(e.target).animate({opacity:'1'});
         
      };
  };
  
  
  var initModule = function () {
    //bind evevt
    jqueryMap.$masks.bind("mouseover",function (e) {
      toggle(e,0);
    });
    jqueryMap.$masks.bind("mouseout",function (e) {
      toggle(e,1);
    });
    jqueryMap.$text_boxes.hide();
    jqueryMap.$text_boxes.eq(0).show();
  };

  return { initModule: initModule };
}());