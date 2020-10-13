<script>
$(document).ready(function(){

//画像データ取得
var margin = $("#front").width()/2;
var width = 150;
var height = 100;


//初期（裏面に隠す）
$("#back").stop().css({width:'0px',height:''+height+'px',marginLeft:''+margin+'px',opacity:'0.5'});

$("#front").click(function(){
  $(this).stop().animate({width:'0px',height:''+height+'px',marginLeft:''+margin+'px',opacity:'0.5'},{duration:200});
  window.setTimeout(function() {
    $("#back").stop().animate({width:''+width+'px',height:''+height+'px',marginLeft:'0px',opacity:'1'},{duration:200});
  },200);
});

$("#back").click(function(){
  $(this).stop().animate({width:'0px',height:''+height+'px',marginLeft:''+margin+'px',opacity:'0.5'},{duration:200});
  window.setTimeout(function() {
    $("#front").stop().animate({width:''+width+'px',height:''+height+'px',marginLeft:'0px',opacity:'1'},{duration:200});
  },200);
});

});
</script>