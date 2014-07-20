'use strict';

/* Factory */

angular.module('myApp.factories', ['ngResource'])

	.factory('BlogFactory', ['$http','$q', function($http,$q){
		var blog = {},
		baseUrl = 'http://local.api.rtancman.com.br/';

		blog.sendApi = function(link,method){
			var deferred = $q.defer();
			$http({method: method, url: link}).
			    success(function(data, status, headers, config) {
			      deferred.resolve(data);
			    }).
			    error(function(data, status, headers, config) {
			      deferred.reject("An error occured while fetching items");
			    });
			return deferred.promise;
		};
		
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
		

		blog.getCategoryPosts = function(slug){
			var deferred = $q.defer();
			$http({method: 'GET', url: baseUrl + '?json=get_category_posts&slug='+slug}).
			    success(function(data, status, headers, config) {
			      deferred.resolve(data);
			    }).
			    error(function(data, status, headers, config) {
			      deferred.reject("An error occured while fetching items");
			    });
			return deferred.promise;
		};

		blog.getCategories = function(){
			var deferred = $q.defer();
			$http({method: 'GET', url: baseUrl + '?json=get_categories'}).
			    success(function(data, status, headers, config) {
			      deferred.resolve(data);
			    }).
			    error(function(data, status, headers, config) {
			      deferred.reject("An error occured while fetching items");
			    });
			return deferred.promise;
		};

		blog.getCategoriesByType = function(child){
			var deferred = $q.defer(),
			apiUrl = baseUrl + '?json=categories.get_categories_types';

			if( child === false ){
				apiUrl += '&father=1';
			}

			$http({method: 'GET', url: apiUrl}).
			    success(function(data, status, headers, config) {
			      deferred.resolve(data);
			    }).
			    error(function(data, status, headers, config) {
			      deferred.reject("An error occured while fetching items");
			    });
			return deferred.promise;
		};

		blog.getAuthors = function(){
			return blog.sendApi(baseUrl + '?json=authors.get_authors','GET');
		};

		blog.getAuthorById = function(id){
			return blog.sendApi(baseUrl + '?json=authors.get_author_id&author_id='+id,'GET');
		};

		blog.getCategoriesAuthors = function(slug){
		};		

		return blog;
	}]);
