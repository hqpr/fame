$().ready(function(){
    $(".myClass").prettyCheckable();
    $("#checkboxDiv").click(function() {
        if ($("#checkbox").is(':checked'))
        {
            $("#checkbox").next().removeClass("checked");
            $('#checkbox').each(function(){ this.checked = false; });
        } else {
            $("#checkbox").next().addClass("checked");
            $('#checkbox').each(function(){ this.checked = true; });
        }
    });
});


$(function()
{
    $('.scroll-pane').jScrollPane({autoReinitialise: true});
});

$(document).ready(function(){
    $('.close-icon').on('click', function(){
        $('#modal-body').modal('hide');
    });
    $('#cancel').on('click', function(){
        $('#modal-body').modal('hide');
    });
    $('.btn-pink').on('click', function(){
        $('#competition_step1').hide();
        $('#competition_step2').show();
    });
    $('#back_to_step1').on('click', function(){
        $('#competition_step2').hide();
        $('#competition_step1').show();
    });
    $('#competition_upload_track').on('click', function(){
        $('#competition_step2').hide();
        $('#competition_upload_audio').show();
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

    $('#submit_select_video').on('click', function () {
        $('#competition_select_video_form').ajaxSubmit({
            success: function(data){
                if (data.success) {
                    console.log('success');
                    $('#competition_select_video').hide();
                    $('#competition_step2').hide();
                    $('#competition_step3').hide();
                    $('#competition_step4').show();
                } else {
                    console.log('error');
                    $('#competition_step2').hide();
                }
            }
        });
    });

    $('#competition_to_finish').on('click', function(){
        $('#competition_select_video').hide();
        $('#competition_select_track').hide();
        $('#competition_step4').hide();
        $('#competition_step5').show();
    });

});
