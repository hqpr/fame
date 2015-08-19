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

    var button_handler = StripeCheckout.configure({
        key: 'pk_test_lvQ40oIEm0JqVmqE5wNmVNS5',
        image: '/static/images/fame-music-logo-left.png',
        token: function(token) {
            $.ajax({
                url: "/subscribe/",
                type: "POST",
                data: {
                    stripeToken : token.id,
                    csrfmiddlewaretoken: csrftoken
                },
                success: function(data) {
                    if (data.success) {
                        console.log('Success');
                        window.location.reload()
                    } else {
                        console.log('error');
                    }
                },
                dataType: "json"
            });
        }
    });

    $('#subscribe_button').on('click', function(e) {
        button_handler.open({
            name: 'Fame Music',
            description: ''
        });
        e.preventDefault();
    });


     //Close Checkout on page navigation
    //$(window).on('popstate', function() {
    //    handler.close();
    //});

});