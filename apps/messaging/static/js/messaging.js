(function($) {

    var conversation_url = $('#api').data('url');
    //var user_id = $('#user_id').data('user');

    //$('.enter-btn').on('click', function(){
    //    $.ajax({
    //      type: "POST",
    //      url: conversation_url,
    //      data: {'user_id': user_id},
    //      success: function(){console.log('yes')},
    //      dataType: 'json'
    //    });
    //});

    var conversation_info = $('.info');
    var close_conversation = $('.close_conversation');
    var message_box = $(".message-box");

    //$.get( "/api/connections/", function( data ) {
    //    $.each(data, function(index, element) {
    //        conversation_info.find('h5').html(element.connection.user);
    //        console.log(index);
    //        console.log(element.connection.user);
    //    })
    //});

    //$.get(conversation_url, function( data ) {
    //    $.each(data, function(index, element) {
    //        conversation_info.find('h5').html(element.receiver);
    //        console.log(index);
    //        console.log(element.receiver);
    //    })
    //});

    message_box.hover(
        function () {
            $(this).addClass('active');
            $(this).find('a').show();
        },
        function () {
            $(this).removeClass('active');
            close_conversation.hide();
        }
    );
    message_box.on('click', function(){
        var conversation_pk = $(this).data('url');
        window.location.replace('/messages/'+conversation_pk+'/');
        //$.get( "/api/messages/"+conversation_pk+"/", function(data) {
        //    $.each(data, function(index, element) {
        //        conversation_info.find('h5').html(element.connection.user);
                //console.log(index);
                //console.log(element);
            //})
        //});
    })

})(jQuery);