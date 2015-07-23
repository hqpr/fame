// custom input
$(function()
{
    // jquery fails if no .myClass on page
     $(".myClass").prettyCheckable();

    $("#checkboxDiv").click(function() {
        var checkbx = $("#checkbox");
        if (checkbx.is(':checked'))
        {
            checkbx.next().removeClass("checked");
            checkbx.each(function(){ this.checked = false; });
        } else {
            checkbx.next().addClass("checked");
            checkbx.each(function(){ this.checked = true; });
        }
    });

    // scroll
    $('.scroll-pane').jScrollPane({autoReinitialise: true});


    $('.close-icon').on('click', function(){
        $('#modal-body').modal('hide');
    });
    $('#cancel').on('click', function(){
        $('#modal-body').modal('hide');
    });

    // steps
    $('#to-2-step').on('click', function(){
        $('#competition_step1').hide();
        $('#competition_step2').show();
    });
    $('#back_to_step1').on('click', function(){
        $('#competition_step2').hide();
        $('#competition_select_track').hide();
        $('#competition_step1').show();
    });

    $('#pick_a_track').on('click', function(){
        $('#competition_step2').hide();
        $('#competition_select_track').show();
    });
    $('.back_to_step2').on('click', function(){
        $('#competition_select_track').hide();
        $('#competition_upload_audio').hide();
        $('#competition_step3').hide();
        $('#competition_step2').show();
    });

    $('#submit_select_track').on('click', function () {
        $('#competition_select_track_form').ajaxSubmit({
            success: function(data){
                if (data.success) {
                    console.log('success');
                    $('#competition_select_track').hide();
                    $('#competition_step2').hide();
                    $('#competition_step3').show();
                } else {
                    console.log('error');
                    $('#pick_error').hide().show();
                    $('#competition_step2').hide();
                }
            }
        });
    });

    $('.back_to_step3').on('click', function(){
        $('#competition_select_video').hide();
        $('#competition_step4').hide();
        $('#competition_step3').show();
    });

    $('#pick_a_video').on('click', function(){
        $('#competition_step3').hide();
        $('#competition_select_video').show();
    });

    var submit_select_video = $('#submit_select_video');

    submit_select_video.on('click', function () {
        $('#competition_select_video_form').ajaxSubmit({
            success: function(data){
                if (data.success) {
                    console.log('success');

                    // preview results
                    var competition = $('#competition_upload_video').data('slug');
                    $.get( '/competitions/'+competition+'/review/', function( data ) {
                      $( "#competition_select_video" ).html( data );
                    });
                } else {
                    console.log('error');
                    $('#competition_step2').hide();
                }
            }
        });
    });

    // upload audio file to competition
    $('#id_audio').on('change', function(){
        $('#form_upload_step1').ajaxSubmit({
            success: function(data){
                if (data.success) {
                    console.log('Audio successfully added');
                    window.next_url = data.redirect_to;
                    window.competition_add = data.competition_add;

                } else {
                    console.log('error');
                }
            }
        });

        $('#competition_step2').hide();
        $('#competition_upload_audio').show();
    });

    // adding info about audio to competition
    $('#submit_audio').on('click', function(){
        var form = $(this).closest('form');
        var modal = form.closest('.modal');
        $('#upload_competition_audio').ajaxSubmit({
            url: next_url,
            success: function(data){
                var audio_form = $('#competition_upload_audio');
                if (data.success) {
                    $.ajax({
                        type: "POST",
                        url: competition_add,
                        data: {slug: audio_form.data('slug')},
                        success: function(r){
                            if (r.success){
                                console.log('Added to competition');
                                $('#competition_upload_audio').hide();
                            }
                        }
                    });
                    audio_form.hide();
                    $('#competition_step3').show();
                } else {
                    $('#errors').text('Please fill all fields').show();
                }
            }
        });
    });

    // upload video file to competition
    $('#id_video').on('change', function(){
        $('#form_upload_step3').ajaxSubmit({
            success: function(data){
                if (data.success) {
                    console.log('Video successfully added');
                    window.next_url = data.redirect_to;
                    window.competition_add = data.competition_add;
                    window.competition_add_video = data.competition_add_video;
                    $('#competition_step3').hide();
                    $('#competition_upload_video').show();

                } else {
                    console.log('error');
                    $('#file_error').hide().show()
                }
            }
        });


    });

    // adding info about video to competition
    $('#submit_video').on('click', function(){
        var video_form = $('#upload_competition_video');
        var form = $(this).closest('form');
        var modal = form.closest('.modal');
        video_form.ajaxSubmit({
            url: next_url,
            success: function(data){
                console.log(competition_add_video);
                console.log(video_form.data('slug'));
                if (data.success) {
                    $.ajax({
                        type: "POST",
                        url: competition_add_video,
                        data: {slug: $('#competition_upload_video').data('slug')},
                        success: function(r){
                            if (r.success){
                                console.log('Added to competition');
                                $('#competition_upload_video').hide();
                                $('#competition_step4').show();
                            }
                        }
                    });
                } else {
                    $('#errors').text('Please fill all fields').show();
                }
            }
        });
    });





});
