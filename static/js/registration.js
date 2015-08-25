$(document).ready(function(){
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

    //Validation
    var name = $('#id_username');
    var email = $('#id_email');
    var password = $('#id_password');
    var confirm_password = $('#id_password_2');

    var display_name = $('#id_display_name');
    var birthday = $('#id_birthday');

    name.on('input propertychange', function(){
        console.log('username');
        $.ajax({
            type: "POST",
            url: '/user/check_username/',
            data: {'username': name.val()},
            success: function(data){
                if (data.success){
                    console.log('success');
                    name.removeClass('has-warning').addClass('has-success bounceIn');
                } else {
                    console.log('error');
                    name.removeClass('has-success').addClass('has-warning');
                }
            } 
            ,
            dataType: 'json'
        });
    });
    email.on('input propertychange', function() {
        if(/.+@.+\..+/i.test(email.val())) {
            email.removeClass('has-warning').addClass('has-success');
        } else {
            email.removeClass('has-success').addClass('has-warning');
        }
    });
    password.on('input propertychange', function() {
        var valid = false;
        if(/(\w){6,32}/i.test(password.val())) {
            password.removeClass('has-warning').addClass('has-success');
            valid = true;
        } else {
            password.removeClass('has-success').addClass('has-warning');
        }
        if (password.val() != confirm_password.val()) {
            password.removeClass('has-success').addClass('has-warning');
            confirm_password.removeClass('has-success').addClass('has-warning');
        } else if(valid) {
            password.removeClass('has-warning').addClass('has-success');
            confirm_password.removeClass('has-warning').addClass('has-success');
        }
    });
    confirm_password.on('input propertychange', function() {
         var valid = false;
        if(/(\w){6,32}/i.test(confirm_password.val())) {
            confirm_password.removeClass('has-warning').addClass('has-success');
             valid = true;
        } else {
            confirm_password.removeClass('has-success').addClass('has-warning');
        }
        if (password.val() != confirm_password.val()) {
            password.removeClass('has-success').addClass('has-warning');
            confirm_password.removeClass('has-success').addClass('has-warning');
        } else if(valid) {
            password.removeClass('has-warning').addClass('has-success');
            confirm_password.removeClass('has-warning').addClass('has-success');
        }
    });
    display_name.on('input propertychange', function() {
        if(/(\w){2,32}/i.test(display_name.val())) {
            display_name.removeClass('has-warning').addClass('has-success');
        } else {
            display_name.removeClass('has-success').addClass('has-warning');
        }
    });
    birthday.on('input propertychange', function() {
        if(/[0-9]{4}-[0-9]{1,2}-[0-9]{1,2}/i.test(birthday.val())) {
            birthday.removeClass('has-warning').addClass('has-success');
        } else {
            birthday.removeClass('has-success').addClass('has-warning');
        }
    });
    //Validation

/*    // first step
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
    });*/

    // final step
    [].slice.call(document.querySelectorAll('#reg_semistep_submit_div')).forEach(function(bttn, pos) {
        new UIProgressButton(bttn, {
            callback: function (instance) {
                var res = 0,
                    redirectTo = '';
                var progress = 0,
                    interval = setInterval(function () {
                        progress = Math.min(progress + Math.random() * 0.1, 1);
                        instance.setProgress(progress);

                        if (res > 0 && progress === 1) {
                            if (res == 1) {
                                instance.stop(-1);
                            }
                            else {
                                instance.stop(1);
                                $('#reg_step_2_1').hide();
                                $('#reg_step_2_2').show();
                            }
                            clearInterval(interval);
                        }
                    }, 100);

                if (!$("input[name='account_type']:checked").val()) {
                    $('#error').css('color', '#f10950');
                    res = 1;
                    return false;
                } else {
                    res = 2;
                    [].slice.call(document.querySelectorAll('#finish_registration_div')).forEach(function (bttn, pos) {
                        new UIProgressButton(bttn, {
                            callback: function (instance) {
                                var res = 0,
                                    redirectTo = '';
                                var progress = 0,
                                    interval = setInterval(function () {
                                        progress = Math.min(progress + Math.random() * 0.1, 1);
                                        instance.setProgress(progress);

                                        if (res > 0 && progress === 1) {
                                            if (res == 1) {
                                                instance.stop(-1);
                                            }
                                            else {
                                                instance.stop(1);
                                                window.location = redirectTo;
                                            }
                                            clearInterval(interval);
                                        }
                                    }, 100);
                                $('#reg_step_2').ajaxSubmit({
                                    success: function (data) {
                                        if (data.success) {
                                            res = 2;
                                            //location.reload();
                                            if (window.location == data.redirect_to) {
                                                //location.reload();
                                            }
                                            redirectTo = data.redirect_to;
                                        } else {
                                            res = 1;
                                            $('#reg_step_2_2').html(data.html);
                                            console.log('reg errors')
                                        }
                                    },
                                    dataType: 'json'
                                });
                            }
                        });
                    });
                }
            }
        });
    });

    [].slice.call(document.querySelectorAll('#reg_step_1_submit_div')).forEach(function(bttn, pos) {
        new UIProgressButton(bttn, {
            callback: function (instance) {
                var res = 0,
                    redirectTo = '';
                var progress = 0,
                interval = setInterval( function() {
                    progress = Math.min( progress + Math.random() * 0.1, 1 );
                    instance.setProgress( progress );

                    if( res > 0 && progress === 1) {
                        if(res == 1) {
                            instance.stop(-1);
                        }
                        else {
                            instance.stop(1);
                            window.location = redirectTo;
                        }
                        clearInterval( interval );
                    }
                }, 100 );

                var pass = $("#id_password");
                var pass_repeat = $("#id_password_2");
                if (($.trim(pass_repeat.val()).length > 0) &&
                    (pass.val() != pass_repeat.val())) {
                    res = 1;
                } else {
                    $('#reg_step_1').ajaxSubmit({
                        success: function (data) {
                            res = 1;
                            if (data.success) {
                                res = 2;
                                //location.reload();
                                if (window.location == data.redirect_to) {
                                    //location.reload();
                                }
                                redirectTo = data.redirect_to;
                            }
                        },
                        error: function(err) {
                            res = 1;
                        },
                        dataType: 'json'
                    });
                }
            }
        });
    });

    $('#to_step_2_1').on('click', function(){
        $('#reg_step_2_2').hide();
        $('#reg_step_2_1').show();
    })

});