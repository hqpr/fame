$(document).ready(function(){

    $(".frame").hover(
      function () {
        $( this ).find('div').fadeIn(200);
      },
      function () {
        $('.hover-frame').hide();
      }
    );

    $(".music_box").hover(
      function () {
        $( this ).find('div').fadeIn(200);
      },
      function () {
        $('.playlist-thumb-hover').hide();
      }
    );

    var settings_ap = {
        disable_volume: 'off'
        ,disable_scrub: 'default'
        ,design_skin: 'skin-wave'
        ,skinwave_dynamicwaves:'on'
    };
    dzsag_init('#mixtape',{
        'transition':'fade'
        ,'autoplay' : 'off'
        ,'settings_ap':settings_ap
    });
    $('#update_audio').on('click', function(){
        $('#edit_audio_form').ajaxSubmit({
            success: function(data){
                if (data.success){
                    window.location = '/profile/';

                } else {
                    console.log('error');
                    $('.modal-body').html(data.html);
                }
            },
            dataType: 'json'
        });
    });

    $('.btn-cancel').on('click', function(){
       $('#upload_music_modal').modal('hide');
    });

    $('#edit_button').one('click', function(){
        $('.top-menu').append(' +');
        $('.click-to-move').show()
    });

});
