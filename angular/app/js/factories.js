'use strict';

/* Factory */

angular.module('myApp.factories', ['ngResource'])

	.factory('BlogFactory', ['$http','$q', function($http,$q){
		var blog = {},
		baseUrl = 'http://local.api.rtancman.com.br/';

		blog.getRecentPosts = function(){
			var deferred = $q.defer();
			$http({method: 'GET', url: baseUrl + '?json=get_recent_posts'}).
			    success(function(data, status, headers, config) {
			      deferred.resolve(data);
			    }).
			    error(function(data, status, headers, config) {
			      deferred.reject("An error occured while fetching items");
			    });
			return deferred.promise;
		};

		blog.getPost = function(id){
			var deferred = $q.defer();
			$http({method: 'GET', url: baseUrl + '?json=get_post&post_id='+id}).
			    success(function(data, status, headers, config) {
			      deferred.resolve(data);
			    }).
			    error(function(data, status, headers, config) {
			      deferred.reject("An error occured while fetching items");
			    });
			return deferred.promise;
		};

		return blog;
	}]);