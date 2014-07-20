'use strict';

/* Controllers */

angular.module('myApp.controllers', [])
  .controller('MainCtrl', ['$scope','$window', function($scope,$window) {
  	angular.element($window).bind("scroll", function(e) {
  		if ($window.pageYOffset > 50) {
  			$scope.fixed = true;
  		} else {
  			$scope.fixed = false;
  		}
  		$scope.$apply();
  	});
  }])
  .controller('ArticleCtrl', ['$scope','BlogFactory','$routeParams','$compile', function($scope,BlogFactory,$routeParams,$compile) {
    $scope.article = [];
    function refreshItems(){
      BlogFactory.getPost($routeParams.id).then(function(data){
        $scope.article = data.post;
        console.log(data.post);
      },
      function(errorMessage){
        $scope.error=errorMessage;
      });
    };
    refreshItems();
  }])
  .controller('BlogCtrl', ['$scope','BlogFactory', function($scope,BlogFactory) {
  	$scope.blog = [];
    function refreshItems(){
      BlogFactory.getRecentPosts().then(function(data){
        $scope.blog = data;
        console.log(data);
      },
      function(errorMessage){
        $scope.error=errorMessage;
      });
    };
    refreshItems();
  }])
  .controller('ProjectsCtrl', ['$scope', function($scope,BlogFactory) {
  	
  }]);
