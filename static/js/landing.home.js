$(document).ready(function() {
    $('#fullpage').fullpage({
        afterLoad: function(anchorLink, index){
                	$('.animated').appear(function() {

	        var elem = $(this);
	        var animation = elem.data('animation');

	        if ( !elem.hasClass('visible_animate') ) {
	        	var animationDelay = elem.data('animation-delay');
	            if ( animationDelay ) {
	                setTimeout(function(){
	                    elem.addClass( animation + " visible_animate" );
	                }, animationDelay);

	            } else {
	                elem.addClass( animation + " visible_animate" );
	            }
	        }
	    });
        },
        onSlideLeave: function() {
            WOW().stop();
        }
    });

});

$('#what-fame-music-bttm').click(function(){
    $.fn.fullpage.moveSectionDown();
});
