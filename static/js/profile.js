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
    dzsag_init('#ag1',{
        'transition':'fade'
        ,'autoplay' : 'off'
        ,'settings_ap':settings_ap
    });

});
