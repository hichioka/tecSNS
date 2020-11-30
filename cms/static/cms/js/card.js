$(document).ready(function(){

//画像データ取得
var margin = $(".front").width()/2;
// 返した後の幅と高さの指定
var width = 270;
var height = 410;


//初期（裏面に隠す）
//width:はめくった後の幅、補足すると下までテキストが伸びてしまうが捕捉しないとカードめくった感がない
$(".back").stop().css({width:'0px',height:''+height+'px',marginLeft:''+margin+'px',opacity:'.0'});

$(".front").click(function(){
  $(this).stop().animate({width:'0px',height:''+height+'px',marginLeft:''+margin+'px',opacity:'.0'},{duration:200});
  window.setTimeout(function() {
    $(".back").stop().animate({width:''+width+'px',height:''+height+'px',marginLeft:'0px',opacity:'1'},{duration:200});
  },200);
});

$(".back").click(function(){
  $(this).stop().animate({width:'0px',height:''+height+'px',marginLeft:''+margin+'px',opacity:'.0'},{duration:200});
  window.setTimeout(function() {
    $(".front").stop().animate({width:''+width+'px',height:''+height+'px',marginLeft:'0px',opacity:'1'},{duration:200});
  },200);
});

});

//２種類めのカードエフェクト
// $(function() {
//     $("left-content").click(function() {
//       // 変数の定義
//         var $currentElm = $("front.active");
//             $targetElm = $("back");
 
//         $("front").removeClass("active");
//         $(back).addClass("active");
 
//         $(".left-content").addClass("animate");
//         $targetElm
//             .addClass("animate");
//         var timer = setTimeout(function() {
//             $currentElm
//                 .removeClass("active")
//                 .addClass("animate");
//             $targetElm
//                 .removeClass("animate")
//                 .addClass("active");
//             $(".left-content")
//                 .removeClass("animate")
//                 .addClass("animateEnd");
//             var timer = setTimeout(function() {
//                 $(".left-content")
//                     .removeClass("animateEnd");
//                 $currentElm
//                     .removeClass("animate");
//                 $(".left-content").removeClass("animate");
//             }, 500);
//         }, 500);
//         return false;
//     });
// });