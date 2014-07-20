'use strict';


// Declare app level module which depends on filters, and services
angular.module('myApp', [
  'ngRoute',
  'ngResource',
  'ngSanitize',
  'ui.bootstrap',
  'duScroll',
  'myApp.filters',
  'myApp.services',
  'myApp.factories',
  'myApp.directives',
  'myApp.controllers'
]).
config(['$routeProvider','$locationProvider','$sceProvider', function($routeProvider,$locationProvider,$sceProvider) {
  $sceProvider.enabled(true);
  $locationProvider.html5Mode(true);
  $routeProvider.when('/', {templateUrl: 'partials/main.html', controller: 'MainCtrl'});
  $routeProvider.when('/artigos', {templateUrl: 'partials/blog.html', controller: 'BlogCtrl', containerClass: 'blog', showNavigation: true});
  $routeProvider.when('/projetos', {templateUrl: 'partials/projects.html', controller: 'ProjectsCtrl', containerClass: 'projects', showNavigation: true});
  $routeProvider.when('/:permalink-m:id', {templateUrl: 'partials/article.html', controller: 'ArticleCtrl', containerClass: 'article', showNavigation: true});
  $routeProvider.otherwise({redirectTo: '/'});
}])
.run(['$location', '$rootScope', function($location, $rootScope) {
    $rootScope.$on('$routeChangeSuccess', function (event, current, previous) {
        $rootScope.showNavigation = current.$$route.showNavigation;
        $rootScope.containerClass = current.$$route.containerClass;
    });
}]);