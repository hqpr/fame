$(document).ready(function(){

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
    $('#reg_step_1_submit').on('click', function(){
        var pass = $("#id_password");
        var pass_repeat = $("#id_password_2");
        if(($.trim(pass_repeat.val()).length > 0) &&
        (pass.val() != pass_repeat.val())) {
            console.log('pass did not match');
            pass.closest('div').addClass('has-warning');
            pass_repeat.closest('div').addClass('has-warning');
        } else {
            $('#reg_step_1').ajaxSubmit();
        }
    });

});