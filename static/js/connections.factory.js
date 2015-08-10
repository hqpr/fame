'use strict';

function Connections($http, $q) {
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
      var url = '/api/connect' + (query_list ? "?" + query_list.join("&") : "");
      $http
        .get(url)
        .then(function(result) {
          var connections = result.data;
          // var entries = result.data.filter(function (element) {
          //   return element.track.name.toLowerCase().indexOf(params.search.toLowerCase()) !== -1
          // });
          connections = _.sortByOrder(connections, params.sorting, params.reverseOrder ? 'desc' : 'asc');
          deferred.resolve({
            connections: connections.slice(params.offset, params.offset + params.limit),
            totalConnectionsCount: connections.length
          });
        })
        .catch(function(err) {
          deferred.reject(err);
        });
      return deferred.promise;
    },
    get: function(params) {
      var deferred = $q.defer();
      $http.get('/connections', {
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
            connections: response.data,
            totalConnectionsCount: response.data.totalEntriesCount
          })
        })
        .catch(function(err) {
          deferred.reject(err);
        });
      return deferred.promise;
    }
  }
}

angular.module('ConnectionApp')
  .factory('Connections', ['$http', '$q', Connections]);
