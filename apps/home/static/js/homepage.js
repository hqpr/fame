(function($) {
    var tut1 = $('#tutorial_1');
    var tut2 = $('#tutorial_2');
    var tut3 = $('#tutorial_3');
    var tut4 = $('#tutorial_4');

    $('#step1').on('click', function(){
        tut1.fadeOut();
        tut2.fadeIn();
        $('#sidr-right').css('z-index', '9999').css('position', 'relative');
    });
    $('#step2').on('click', function(){
        tut2.fadeOut();
        tut3.fadeIn();
        $('#sidr-right').css('z-index', '0');
        $('.my-task-col').css('z-index', '9999').css('position', 'relative')
            .css('background-color', '#ececec').css('border-radius', '10px');
    });
    $('#step3').on('click', function(){
        tut3.fadeOut();
        tut4.fadeIn();
        $('.my-task-col').css('z-index', '0');
    });

    var complete_url = '/home/complete/tutorial/';
    $('.close-tutorial').on('click', function(){
        $.post(complete_url, function(data){
            if (data.success){
                console.log('ok');
                $('.modal-backdrop').hide();
                $('.modal').hide();
            } else {
                console.log('not ok');
            }
        });
    });

    $('#back_to_step1').on('click',function(){
        tut1.fadeIn();
        tut2.fadeOut();
        $('#sidr-right').css('z-index', '0');
    });
    $('#back_to_step2').on('click',function(){
        tut2.fadeIn();
        $('#sidr-right').css('z-index', '9999').css('position', 'relative');
        $('.my-task-col').css('z-index', '0');
        tut3.fadeOut();
    });

})(jQuery);