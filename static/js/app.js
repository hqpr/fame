'use strict';

var ChartApp = angular.module('ChartApp', [
  'ui.bootstrap'
]);
var playerid = 'ag1';
var settings_ap = {
    disable_volume: 'off'
    ,disable_scrub: 'default'
    ,design_skin: 'skin-wave'
    ,skinwave_dynamicwaves:'on'
    ,skinwave_enableSpectrum:'off'
    ,settings_backup_type:'full'
    ,skinwave_enableReflect:'on'
    ,skinwave_comments_enable:'on'
    ,skinwave_timer_static:'off'
    ,disable_player_navigation: 'off'
    ,skinwave_mode: 'normal'
    ,skinwave_comments_retrievefromajax:'on'
};

function MainCtrl($scope, Charts) {

  // Initialize $scope using the value of the model attribute, e.g.,
  $scope.url = "/api/competitions/" + $scope.slug + "/chart";
  
  $scope.maxChartsPerPage = 5;
  $scope.maxPages = 5;
  $scope.chartsCurrPage = 1;
  $scope.chartSearchString = '';
  $scope.order = 'chart_position';
  $scope.reverseOrder = false;
  $scope.sortingTypes = [
    {
      title: 'Track Name',
      active: false
    },
    {
      title: 'Chart',
      active: true
    },
    {
      title: 'Play',
      active: false
    },
    {
      title: 'Date Added',
      active: false
    },
    {
      title: 'Popularity',
      active: false
    }
  ];

  Charts.getFromJSON({
    limit: 5,
    offset: 0,
    search: '',
    url: $scope.url
  })
    .then(function(result) {
      $scope.charts = result.charts;
      $scope.totalChartsCount = result.totalChartsCount;
    })
    .catch(function(err) {
      console.log(err);
    });

  $scope.loadCharts = function() {
    Charts.getFromJSON({
      limit: $scope.maxChartsPerPage,
      offset: ($scope.chartsCurrPage - 1) * $scope.maxChartsPerPage,
      search: $scope.chartSearchString,
      sorting: $scope.order,
      reverseOrder: $scope.reverseOrder,
      url: $scope.url
    })
      .then(function(result) {
        $scope.charts = result.charts;
        $scope.totalChartsCount = result.totalChartsCount;
      })
      .catch(function(err) {
        console.log(err);
      });
  };

  $scope.visible = true;

  $scope.sortBy = function(sortingType) {
    $scope.sortingTypes.forEach(function(type) { type.active = false; });
    sortingType.active = true;
    switch (sortingType.title) {
      case 'Track Name': $scope.order = 'track.name'; $scope.reverseOrder = false; break;
      case 'Chart': $scope.order = 'position'; $scope.reverseOrder = false; break;
      case 'Play': $scope.order = 'track.plays'; $scope.reverseOrder = true; break;
      case 'Date Added': $scope.order = 'track.added'; $scope.reverseOrder = true; break;
      case 'Popularity': $scope.order = 'track.likes'; $scope.reverseOrder = true; break;
    }
    $scope.loadCharts();
  }
  $scope.selectTrack = function($idx) {
    $scope.entry = $scope.charts[$idx];
    $("#modal").show(function() {
      dzsag_init('#'+playerid,{
          'transition':'fade'
          ,'cueFirstMedia' : 'on'
          ,'autoplay' : 'on'
          ,'autoplayNext' : 'off'
          ,design_menu_position:'bottom'
          ,'settings_ap':settings_ap
          ,design_menu_state:'open'
          ,design_menu_show_player_state_button: 'off'
          ,embedded: 'off'
          ,enable_easing: 'on'
      });
    });
  }
  $("#modalDismiss").click(function() {
    $("#modal").hide();
  });
}

function Decorate($provide) {
  $provide.decorator('paginationDirective', function($delegate) {
    var directive = $delegate[0];

    directive.templateUrl = "/static/js/paginationOverride.tpl.html";

    return $delegate;
  });
}

ChartApp
  .config(['$provide', Decorate])
  .controller('MainCtrl', ['$scope', 'Charts', MainCtrl]);
