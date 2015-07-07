var fameMusicApp = angular.module('fameMusicApp', []).config(function($httpProvider) {
  $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
});