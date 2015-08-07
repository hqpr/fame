$(document).ready(function(){
    $('.viewer-block').hover(function() {
            $(this).addClass('active');
        }, function() {
            $(this).removeClass('active');
        }
    );
})