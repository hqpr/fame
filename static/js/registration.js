$(document).ready(function(){

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

    // username check
    var name = $('#id_username');
    name.on('change', function(){
        console.log('username');
        $.ajax({
            type: "POST",
            url: '/user/check_username/',
            data: {'username': name.val()},
            success: function(data){
                if (data.success){
                    console.log('success');
                    name.closest('div').removeClass('has-warning').addClass('has-success');
                } else {
                    console.log('error');
                    name.closest('div').removeClass('has-success').addClass('has-warning');
                }
            } 
            ,
            dataType: 'json'
        });
    });

    // first step
    $('#reg_step_1_submit').on('click', function(){
        var pass = $("#id_password");
        var pass_repeat = $("#id_password_2");
        if(($.trim(pass_repeat.val()).length > 0) &&
        (pass.val() != pass_repeat.val())) {
            console.log('pass did not match');
            pass.closest('div').addClass('has-warning');
            pass_repeat.closest('div').addClass('has-warning');
        } else {
            $('#reg_step_1').ajaxSubmit({
                success: function(data){
                    if (data.success){
                        location.reload();
                        if (window.location == data.redirect_to){
                            location.reload();
                        }
                        window.location = data.redirect_to;
                    }
                },
                dataType: 'json'
            });
        }
    });

    // final step
    $('#reg_semistep').on('click', function(){
        $('#reg_step_2_1').hide();
        $('#reg_step_2_2').show();
        $('#finish_registration').on('click', function(){
            $('#reg_step_2').ajaxSubmit({
                success: function(data){
                    if (data.success){
                        location.reload();
                        if (window.location == data.redirect_to){
                            location.reload();
                        }
                        window.location = data.redirect_to;
                    } else {
                        $('#reg_step_2_2').html(data.html);
                        console.log('reg errors')
                    }
                },
                dataType: 'json'
            });
        });

    });

    $('#to_step_2_1').on('click', function(){
        $('#reg_step_2_2').hide();
        $('#reg_step_2_1').show();
    })

});