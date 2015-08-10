'use strict';

function Charts($http, $q, $location) {
  return {
    getFromJSON: function(params) {
      //return $http
      //  .get('/chart-html/sample-api.json');
      var deferred = $q.defer();
      var url = params.url;

      $http
        .get(url)
        .then(function(result) {
          var entries = result.data.filter(function (element) {
            return element.track.name.toLowerCase().indexOf(params.search.toLowerCase()) !== -1
          });
          entries = _.sortByOrder(entries, params.sorting, params.reverseOrder ? 'desc' : 'asc');
          deferred.resolve({
            charts: entries.slice(params.offset, params.offset + params.limit),
            totalChartsCount: entries.length
          });
        })
        .catch(function(err) {
          deferred.reject(err);
        });
      return deferred.promise;
    },
    get: function(params) {
      var deferred = $q.defer();
      $http.get('/chart', {
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
            charts: response.data.entries,
            totalChartsCount: response.data.totalEntriesCount
          })
        })
        .catch(function(err) {
          deferred.reject(err);
        });
      return deferred.promise;
    }
  }
}

angular.module('ChartApp')
  .factory('Charts', ['$http', '$q', '$location', Charts]);
