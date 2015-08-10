'use strict';

function Competitions($http, $q) {
  return {
    getFromJSON: function(params) {
      //return $http
      //  .get('/chart-html/sample-api.json');
      var deferred = $q.defer();
      var query_string = "";
      var query_list = [];
      if (params["countries"]) { query_list.push("c=" + params["countries"].join()); }
      if (params["genres"]) { query_list.push("g=" + params["genres"].join()); }
      if (params["status"]) { query_list.push("s=" + params["status"]); }
      var url = '/api/competitions' + (query_list ? "?" + query_list.join("&") : "");
      $http
        .get(url)
        .then(function(result) {
          var competitions = result.data;
          // var entries = result.data.filter(function (element) {
          //   return element.track.name.toLowerCase().indexOf(params.search.toLowerCase()) !== -1
          // });
          competitions = _.sortByOrder(competitions, params.sorting, params.reverseOrder ? 'desc' : 'asc');
          deferred.resolve({
            competitions: competitions.slice(params.offset, params.offset + params.limit),
            totalCompetitionsCount: competitions.length
          });
        })
        .catch(function(err) {
          deferred.reject(err);
        });
      return deferred.promise;
    },
    get: function(params) {
      var deferred = $q.defer();
      $http.get('/competitions', {
        params: {
          search: params.search,
          limit: params.limit,
          offset: params.offset,
          sortby: params.sorting,
          order: params.reverseOrder ? 'desc' : 'asc'
        }
      })
        .then(function(response) {
          deferred.resolve({
            competitions: response.data,
            totalCompetitionsCount: response.data.totalEntriesCount
          })
        })
        .catch(function(err) {
          deferred.reject(err);
        });
      return deferred.promise;
    }
  }
}

angular.module('CompetitionApp')
  .factory('Competitions', ['$http', '$q', Competitions]);
