'use strict';

var MediaApp = angular.module('MediaApp', [
  'ui.bootstrap'
]);


function MainCtrl($scope, Medias) {
  $scope.maxMediasPerPage = 8;
  $scope.maxPages = 5;
  $scope.mediasCurrPage = 1;
  $scope.mediaSearchString = '';
  $scope.order = 'media_position';
  $scope.reverseOrder = false;
  
  $scope.genres = ["Pop","Rap","Rock"];
  $scope.selectedGenres = [];
  $scope.countries = [{"key":"GB","value":"United Kingdom"},
                      {"key":"IT","value":"Italy"}];
  $scope.selectedCountries = [];
  $scope.status = [{"key":"1","value":"Active"},
                      {"key":"0","value":"Inactive"}];
  $scope.selectedStatus = [];

  $scope.sortingTypes = [
    {
      title: 'Entries',
      active: false
    }
  ];
  Medias.getFromJSON({
    limit: $scope.maxMediasPerPage,
    offset: 0,
    search: '',
    countries: [],
    genres: [],
    status: ""
  })
    .then(function(result) {
      $scope.tracks = result.tracks;
      $scope.totalTracksCount = result.totalTracksCount;
      $scope.videos = result.videos;
      $scope.totalVideosCount = result.totalVideosCount;
      $scope.playlists = result.playlists;
      $scope.totalPlaylistsCount = result.totalPlaylistsCount;
      debugger;
    })
    .catch(function(err) {
      console.log(err);
    });

  $scope.loadMedias = function() {
    Medias.getFromJSON({
      limit: $scope.maxMediasPerPage,
      offset: ($scope.mediasCurrPage - 1) * $scope.maxMediasPerPage,
      search: '',
      countries: $scope.selectedCountries,
      genres: $scope.selectedGenres,
      status: $scope.selectedStatus,
      sorting: $scope.order
    })
      .then(function(result) {
        $scope.tracks = result.tracks;
        $scope.totalTracksCount = result.totalTracksCount;
        $scope.videos = result.videos;
        $scope.totalVideosCount = result.totalVideosCount;
        $scope.playlists = result.playlists;
        $scope.totalPlaylistsCount = result.totalPlaylistsCount;
        debugger;
      })
      .catch(function(err) {
        console.log(err);
      });
  };
  var updateGenreSelected = function(action, id) {
    if (action === 'add' && $scope.selectedGenres.indexOf(id) === -1) {
      $scope.selectedGenres.push(id);
    }
    if (action === 'remove' && $scope.selectedGenres.indexOf(id) !== -1) {
      $scope.selectedGenres.splice($scope.selectedGenres.indexOf(id), 1);
    }
  };

  $scope.updateGenreSelection = function($event, id) {
    var checkbox = $event.target;
    var action = (checkbox.checked ? 'add' : 'remove');
    updateSelected(action, id);
  };
  $scope.genreContent = function() {
    var tempHtml = "<ul>";
    $.each($scope.genres, function(idx, genre) {
      tempHtml += "<div class='checkbox'><label><input type='checkbox' ng-click='updateGenreSelection($event, genre.id)'> " + genre + "</label></div>";
    });
    tempHtml += "</ul><button id='filterGenre' class='btn btn-blue' ng-click='loadMedias()'>Filter</button>";
    return tempHtml;
  }

  $scope.visible = true;

  $scope.sortBy = function(sortingType) {
    $scope.sortingTypes.forEach(function(type) { type.active = false; });
    sortingType.active = true;
    switch (sortingType.title) {
      case 'Entries': $scope.order = 'entries'; $scope.reverseOrder = false; break;
    }
    $scope.loadMedias();
  }
}

function Decorate($provide) {
  $provide.decorator('paginationDirective', function($delegate) {
    var directive = $delegate[0];

    directive.templateUrl = "/static/js/paginationOverride.tpl.html";

    return $delegate;
  });
}

MediaApp
  .config(['$provide', Decorate])
  .controller('MainCtrl', ['$scope', 'Medias', MainCtrl]);
