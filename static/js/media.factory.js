'use strict';

function Medias($http, $q) {
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
      var url = '/api/media' + (query_list ? "?" + query_list.join("&") : "");
      $http
        .get(url)
        .then(function(result) {
          var tracks = [];
          var videos = [];
          var playlists = [];
          if (result.data.tracks.length) {
            tracks = result.data.tracks;
            tracks = _.sortByOrder(tracks, params.sorting, params.reverseOrder ? 'desc' : 'asc');
          }
          if (result.data.videos.length) {
            videos = result.data.videos;
            videos = _.sortByOrder(videos, params.sorting, params.reverseOrder ? 'desc' : 'asc');
          }
          if (result.data.playlists.length) {
            playlists = result.data.playlists;
            playlists = _.sortByOrder(playlists, params.sorting, params.reverseOrder ? 'desc' : 'asc');
          }
          deferred.resolve({
            tracks: tracks.slice(params.offset, params.offset + params.limit),
            totalTracksCount: tracks.length,
            videos: videos.slice(params.offset, params.offset + params.limit),
            totalVideosCount: videos.length,
            playlists: playlists.slice(params.offset, params.offset + params.limit),
            totalPlaylistsCount: playlists.length
          });
        })
        .catch(function(err) {
          deferred.reject(err);
        });
      return deferred.promise;
    },
    get: function(params) {
      var deferred = $q.defer();
      $http.get('/api/media', {
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
            artists: response.data,
            totalMediasCount: response.data.totalEntriesCount
          })
        })
        .catch(function(err) {
          deferred.reject(err);
        });
      return deferred.promise;
    }
  }
}

angular.module('MediaApp')
  .factory('Medias', ['$http', '$q', Medias]);
