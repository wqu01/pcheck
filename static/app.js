'use strict'

angular.module('pcheckApp', [])
	.controller('SearchController', ['$scope', '$http', function($scope, $http){
		$scope.search = function(){
			$http.get("/jolseresults/"+$scope.item_name)
	    		.then(function(response) {
	        		$scope.jolseResults = response.data;
	    	});

	    	//make another request for rrs and tk
	    	$http.get("/rrsresults/"+$scope.item_name)
	    		.then(function(response) {
	        		$scope.rrsResults = response.data;
	    	});
	    	$http.get("/tkresults/"+$scope.item_name)
	    		.then(function(response) {
	        		$scope.tkResults = response.data;});
    	};

    	//when mkaing get price call pass in product_num for jolse
    	$scope.selectJolse = function(choosenLink){
    		//console.log("in select jolse");
    		//console.log(choosenLink);
    		var index = choosenLink.indexOf('product_no');
    		var product_num = choosenLink.slice(index);
    		//console.log(product_num);
    		$http.get("/jolseprice/"+product_num)
	    		.then(function(response) {
	        		$scope.jolseResults = response.data;
	        });

    	};
    	$scope.selectRRS = function(choosenLink){
    		$http.get("/rrsprice/"+choosenLink)
	    		.then(function(response) {
	        		$scope.rrsResults = response.data;
	        });
    	};
    	$scope.selectTK = function(choosenLink){
			$http.get("/tkprice/"+choosenLink)
	    		.then(function(response) {
	        		$scope.tkResults = response.data;
	        });
    	};

	}]);
