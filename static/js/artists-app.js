'use strict';

var ArtistApp = angular.module('ArtistApp', [
  'ui.bootstrap'
]);


function MainCtrl($scope, Artists) {
  $scope.maxArtistsPerPage = 12;
  $scope.maxPages = 5;
  $scope.artistsCurrPage = 1;
  $scope.artistSearchString = '';
  $scope.order = 'artist_position';
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
  Artists.getFromJSON({
    limit: $scope.maxArtistsPerPage,
    offset: 0,
    search: '',
    countries: [],
    genres: [],
    status: ""
  })
    .then(function(result) {
      $scope.artists = result.artists;
      $scope.totalArtistsCount = result.totalArtistsCount;
    })
    .catch(function(err) {
      console.log(err);
    });

  $scope.loadArtists = function() {
    Artists.getFromJSON({
      limit: $scope.maxArtistsPerPage,
      offset: ($scope.artistsCurrPage - 1) * $scope.maxArtistsPerPage,
      search: '',
      countries: $scope.selectedCountries,
      genres: $scope.selectedGenres,
      status: $scope.selectedStatus,
      sorting: $scope.order
    })
      .then(function(result) {
        $scope.artists = result.artists;
        $scope.totalArtistsCount = result.totalArtistsCount;
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
    tempHtml += "</ul><button id='filterGenre' class='btn btn-blue' ng-click='loadArtists()'>Filter</button>";
    return tempHtml;
  }

  $scope.visible = true;

  $scope.sortBy = function(sortingType) {
    $scope.sortingTypes.forEach(function(type) { type.active = false; });
    sortingType.active = true;
    switch (sortingType.title) {
      case 'Entries': $scope.order = 'entries'; $scope.reverseOrder = false; break;
    }
    $scope.loadArtists();
  }
}

function Decorate($provide) {
  $provide.decorator('paginationDirective', function($delegate) {
    var directive = $delegate[0];

    directive.templateUrl = "/static/js/paginationOverride.tpl.html";

    return $delegate;
  });
}

ArtistApp
  .config(['$provide', Decorate])
  .controller('MainCtrl', ['$scope', 'Artists', MainCtrl]);
