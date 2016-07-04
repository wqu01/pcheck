'use strict'

angular.module('pcheckApp', [])
	.controller('SearchController', ['$scope', '$http', function($scope, $http){
		$scope.search = function(){
			    	//make another request for rrs and tk
            $http.get("/rrsresults/"+$scope.item_name)
	    		.then(function(response) {
	        		$scope.rrsResults = response.data;
	        		
	    	});
	    	$http.get("/tkresults/"+$scope.item_name)
	    		.then(function successCallback(response) {
	        		$scope.tkResults = response.data;
	        		

			}, function erroCallback(response){
				
			});
	    	$http.get("/jolseresults/"+$scope.item_name)
	    		.then(function(response) {
	        		$scope.jolseResults = response.data;
	        		
	    	});


	    			
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

        $scope.showCart = false;
        $scope.toggleCart = function(){
            $scope.showCart = !$scope.showCart;
        };

        $scope.jolseTotal = 0;
        $scope.jolseCartList = [];
        $scope.addJolse = function(itemList){
            var price = Number(itemList[3].split(" ")[1]);
            //price is the 3rd index
            $scope.jolseTotal += price;
            $scope.jolseCartList.push({
                item_name: itemList[0],
                item_price: price
            });
            $scope.showCart = true;
        };


        $scope.tkTotalPrice = 0;
        $scope.tkTotalWeight = 0;
        $scope.tkCartList = [];
        $scope.addTK = function(itemList){
            var preprice = itemList[3].split('$')[1];
            var price = Number(preprice.split(')')[0]);
            //price is the 3rd index
            var weight = Number(itemList[4].split('g')[0]);
           
            $scope.tkTotalPrice += price;
            $scope.tkTotalWeight += weight;
            //make function call to get shipping cost
            $scope.tkShippingCost = getShipping($scope.tkTotalWeight);
          
            $scope.tkCartList.push({
                item_name: itemList[0],
                item_price: price,
                item_weight: weight
            });
            $scope.showCart = true;
        };
        $scope.rrsTotalPrice = 0;
        $scope.rrsTotalWeight = 0;
        $scope.rrsCartList = [];
        $scope.addRRS = function(itemList){
             
             var price = Number(itemList[3]);
            //price is the 3rd index
            var weight = Number(itemList[4].split('g')[0]);
            if(weight === "In Stock"){
                weight = 0;    
            }
            //console.log(price);
            //console.log(weight);
            $scope.rrsTotalPrice += price;
            $scope.rrsTotalWeight += weight;
            //make function call to get shipping cost
            $scope.rrsShippingCost = getShipping($scope.rrsTotalWeight);
           // $scope.tkTotalPrice += $scope.tkShippingCost;
            $scope.rrsCartList.push({
                item_name: itemList[0],
                item_price: price,
                item_weight: weight
            });
            $scope.showCart = true;
        };


         function getShipping(weight){
            if(weight <= 100){
                return 3.82;
            }
            else if (weight <= 250){
                return 5.46;
            }
            else if (weight <= 500){
                return 7.84;
            }
            else if (weight <= 1000){
                return 11.46;
            }
            else if (weight <= 1500){
                return 16.09;
            }
            else if (weight <= 1800){
                return 20.73;
            }
            else{
                return 0; //exceded max weight
            }

         }

	}])
    .controller('CartController', ['$scope', function($scope){
            
    }]);
