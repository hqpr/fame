$(document).ready(function(){

    //Validate function to upload track form. Display Submit button when valid only
    function validate() {
        var invalid = false;
        var form = [$('#id_cover'),
                    $('#id_name'),
                    $('#id_artist'),
                    $('#id_type'),
                    $('#id_genre'),
                    $('#id_description'),
                    $('#id_bpm'),
                    $('#id_privacy')];
        for(var i = 0; i < form.length; i++) {
            if(!form[i].val()) invalid = true;
        }
        if(invalid) $('#submit-audio-2')[0].disabled = true;
        else $('#submit-audio-2')[0].disabled = false;
    }

    // bootstrap modal reload
    $(document).on('hidden.bs.modal', function (e) {
        $(e.target).removeData('bs.modal');
    });

    $(".audio_box").hover(
      function () {
        $( this ).find('div').fadeIn(200);
      },
      function () {
        $('.hover-frame').hide();
      }
    );

    $(".about_box").hover(
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
          $( this ).find('div').fadeOut(200);
      }
    );

    $(".video_box").hover(
      function () {
        $( this ).find('div').fadeIn(200);
      },
      function () {
          $( this ).find('div').fadeOut(200);
      }
    );
    $(".playlist_box").hover(
      function () {
        $( this ).find('div').fadeIn(200);
      },
      function () {
        $('.hover-frame').hide();
      }
    );

    // audio player
    //var settings_ap = {
    //    disable_volume: 'off'
    //    ,disable_scrub: 'default'
    //    ,design_skin: 'skin-wave'
    //    ,skinwave_dynamicwaves:'on'
    //};
    //dzsag_init('#mixtape',{
    //    'transition':'fade'
    //    ,'autoplay' : 'on'
    //    ,'settings_ap':settings_ap
    //});
    //

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
    $("#id_link").on("blur", updateAccount);
    function updateAccount() {
        var link = $(this).val();
        if (link.indexOf("facebook") >= 1) { $("#id_account").val("facebook"); $("#edit_social_form .social-icon").attr('class', "social-icon cloud-icon facebook-icon"); return; }
        if (link.indexOf("instagram") >= 1) { $("#id_account").val("instagram"); $("#edit_social_form .social-icon").attr('class', "social-icon cloud-icon instagram-icon"); return; }
        if (link.indexOf("twitter") >= 1) { $("#id_account").val("twitter"); $("#edit_social_form .social-icon").attr('class', "social-icon cloud-icon twitter-icon"); return; }
        if (link.indexOf("soundcloud") >= 1) { $("#id_account").val("soundcloud"); $("#edit_social_form .social-icon").attr('class', "social-icon cloud-icon soundcloud-icon"); return; }
        if (link.indexOf("wavo") >= 1) { $("#id_account").val("wavo"); $("#edit_social_form .social-icon").attr('class', "social-icon cloud-icon wavo-icon"); return; }
        if (link.indexOf("spotify") >= 1) { $("#id_account").val("spotify"); $("#edit_social_form .social-icon").attr('class', "social-icon cloud-icon spotify-icon"); return; }
        if (link.indexOf("vimeo") >= 1) { $("#id_account").val("vimeo"); $("#edit_social_form .social-icon").attr('class', "social-icon cloud-icon vimeo-icon"); return; }
        if (link.indexOf("youtube") >= 1) { $("#id_account").val("youtube"); $("#edit_social_form .social-icon").attr('class', "social-icon cloud-icon youtube-icon"); return; }
        $("#id_account").val("");
        alert("URL not recognised");
        return;
    }
    $('#update_social').on('click', function(){
        $('#edit_social_form').ajaxSubmit({
            success: function(data){
                if (data.success){
                    window.location = '/profile/';

                } else {
                    alert("There's an error");  
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
        $('.click-to-move').show()
    });


    // playlist
    $('#create_playlist').on('click', function () {
        $('#playlist_form').ajaxSubmit({
            success: function(data){
                if (data.success) {
                    $('#upload_music_modal').modal('hide');
                    window.location.href = "/profile/";
                } else {
                    console.log('error');
                    $('.modal-body').html(data.html);
                }
            }
            //dataType: 'json'
        });
    });

    // add track to playlist
    $('#connect_to_playlist').on('click', function () {
        $('#add_to_playlist_form').ajaxSubmit({
            success: function(data){
                if (data.success) {
                    $('#upload_music_modal').modal('hide');
                    window.location.href = "/profile/";
                } else {
                    console.log(data.msg);
                    $('#playlist_error').text(data.msg);
                }
            },
            dataType: 'json'
        });
    });


    $('#trackcard').on('hidden.bs.modal', function () {
        $('.pausebtn').trigger('click'); // pause audio
        /*$('.playbtn').stop();
        $('.pausebtn').stop();*/
        $(".video-js")[0].player.pause(); // pause video
    });

    $('#aboutDetails').on('blur', function () {
        $('#about_form').ajaxSubmit({
            success: function(data){
                if (data.success) {
                    console.log('success');
                } else {
                    console.log('error');
                }
            }
        });
    });

    $('#displayDetails').on('blur', function () {
        $('#display_name_form').ajaxSubmit({
            success: function(data){
                if (data.success) {
                    console.log('success');
                } else {
                    console.log('error');
                }
            }
        });
    });

    $("#connect_button").on('click', function() {
        $("#connect_form").ajaxSubmit({
            success: function(data){
                alert("You're successfully following this person");
            },
            error: function(data) {
                alert("You're already following this person");
            }
        });
    });

    $(".likeAudioButton").on('click', function() {
        var id = $(".likeAudioButton")[0].attributes.toid.value;
        $.ajax({
            method: "POST",
            url: "/api/audio/like",
            data: { "audio": id },
            dataType: "application/json"
        })
        .done(function( msg ) {
            console.log( msg );
        })
        .fail(function( jqXHR, textStatus ) {
            console.log( jqXHR.responseText );
        });
    });

    $('.modal').on('hidden.bs.modal', function(){
        $(this).find('form')[0].reset();
    });
    $('.commentAudioButton').on('click', function() {
        var modalComment = $('#modal-comment');
        modalComment.modal('show');
        modalComment.find('[name=audio]').val(this.attributes.toid.value);
        modalComment.find('[name=time]').val($.now());
    });

});
