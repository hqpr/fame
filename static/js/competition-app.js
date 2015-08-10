'use strict';

var CompetitionApp = angular.module('CompetitionApp', [
  'ui.bootstrap'
]);


function MainCtrl($scope, Competitions) {
  $scope.maxCompetitionsPerPage = 6;
  $scope.maxPages = 5;
  $scope.competitionsCurrPage = 1;
  $scope.competitionSearchString = '';
  $scope.order = 'competition_position';
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
  Competitions.getFromJSON({
    limit: $scope.maxCompetitionsPerPage,
    offset: 0,
    search: '',
    countries: [],
    genres: [],
    status: ""
  })
    .then(function(result) {
      $scope.competitions = result.competitions;
      $scope.totalCompetitionsCount = result.totalCompetitionsCount;
    })
    .catch(function(err) {
      console.log(err);
    });

  $scope.loadCompetitions = function() {
    Competitions.getFromJSON({
      limit: 1,
      offset: ($scope.competitionsCurrPage - 1) * $scope.maxCompetitionsPerPage,
      search: '',
      countries: $scope.selectedCountries,
      genres: $scope.selectedGenres,
      status: $scope.selectedStatus,
      sorting: $scope.order
    })
      .then(function(result) {
        $scope.competitions = result.competitions;
        $scope.totalCompetitionsCount = result.totalCompetitionsCount;
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
    tempHtml += "</ul><button id='filterGenre' class='btn btn-blue' ng-click='loadCompetitions()'>Filter</button>";
    return tempHtml;
  }

  $scope.visible = true;

  $scope.sortBy = function(sortingType) {
    $scope.sortingTypes.forEach(function(type) { type.active = false; });
    sortingType.active = true;
    switch (sortingType.title) {
      case 'Entries': $scope.order = 'entries'; $scope.reverseOrder = false; break;
    }
    $scope.loadCompetitions();
  }
}

function Decorate($provide) {
  $provide.decorator('paginationDirective', function($delegate) {
    var directive = $delegate[0];

    directive.templateUrl = "/static/js/paginationOverride.tpl.html";

    return $delegate;
  });
}

CompetitionApp
  .config(['$provide', Decorate])
  .controller('MainCtrl', ['$scope', 'Competitions', MainCtrl]);
