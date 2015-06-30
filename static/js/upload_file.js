(function($) {
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    var csrftoken = getCookie('csrftoken');


    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    $(document).on('change','#id_audio' , function(){
        $('#form_upload_step1').ajaxSubmit({
            success: function(data){
                if (data.success){
                    var mw = $('#upload_music_modal');
                    mw.modal('hide');
                    mw.find('.modal-body').load(data.redirect_to);
                    mw.find('.modal-body form').data('action', data.redirect_to);
                    mw.modal('show');

                }
            },
            dataType: 'json'
        });
    });

    $(document).on('submit', '#audio_step2_form', function (e) {
        e.preventDefault();

        var form = $(this).closest('form');
        var modal = form.closest('.modal');
        form.ajaxSubmit({
            success: function(data){
                if (data.success){
                    console.log('Success');
                    location.reload();
                    if (window.location == data.redirect_to){
                        location.reload();
                    }
                    window.location = data.redirect_to;

                } else {
                    modal.find('.modal-body').html(data.html);
                }
            },
            dataType: 'json'
        });

        return false;
    });


})(jQuery);