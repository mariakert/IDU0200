var app = angular.module('animalApp', []);

app.controller('tabController', function() {
    this.tab = 1;

    this.setTab = function(newTab){
      this.tab = newTab;
    };

    this.isSet = function(tabNum){
      return this.tab === tabNum;
    };
});

app.controller('animalController', function($scope, $http) {

    $scope.data = {};
    $scope.savedSearch = {};

    $scope.addAnimal = function() {
        var animal = $scope.animal;
        $http({
            method: 'POST',
            url: '/addAnimal',
            data: {
                animal: animal
            }
        }).then(function(response) {
            console.log(response.data.message);
            $scope.query = $scope.savedSearch;
            $scope.search();
            $scope.animal = {};
        }, function(error) {
            console.log(error);
        });
    }
    
    $scope.addSighting = function () {
        var sighting = $scope.sighting;
        var splitDate = ("" + sighting.sight_date).split(" ");
        var date = splitDate[2] + " " + splitDate[1] + " " + splitDate[3];
        var splitTime = ("" + sighting.time).split(" ")[4].split(":");
        var time = splitTime[0] + ":" + splitTime[1];
        $http({
            method: 'POST',
            url: '/addSighting',
            data: {
                sighting: {
                    name: sighting.name,
                    location: sighting.location,
                    sight_date: date,
                    time: time
                }
            }
        }).then(function(response) {
            console.log(response.data);
            $scope.query = $scope.savedSearch;
            $scope.search();
            $scope.sighting = {};
        }, function(error) {
            console.log(error);
        });
    }
    
    $scope.search = function () {
        var search = $scope.query;
        $scope.savedSearch = search;
        $http({
            method: 'POST',
            url: '/search',
            data: {
                search: search
            }
        }).then(function(response) {
            console.log(response.data);
            $scope.query = {};
            if (response.data.status != 'ERROR') {
                $scope.data = response.data;
            } else {
                $scope.data = {}
            }
        }, function(error) {
            console.log(error);
        });
    }

    $scope.editSighting = function($sighting) {
        $scope.animal = {};
        $scope.sighting = {};
        $scope.animal = {
            'id': $sighting[0],
            'name': $sighting[1],
            'species': $sighting[2]
        };
        $scope.sighting = {
            'id': $sighting[3],
            'location': $sighting[5],
            'sight_date': new Date($sighting[6]),
            'time': new Date(new Date().toDateString() + ' ' + $sighting[7])
        };
    }

    $scope.updateSighting = function () {
        var sighting = $scope.sighting;
        var splitDate = ("" + sighting.sight_date).split(" ");
        var date = splitDate[2] + " " + splitDate[1] + " " + splitDate[3];
        var splitTime = ("" + sighting.time).split(" ")[4].split(":");
        var time = splitTime[0] + ":" + splitTime[1];
        $scope.sighting.sight_date = date;
        $scope.sighting.time = time;
        console.log($scope.sighting);

        $http({
            method: 'POST',
            url:'/updateSighting',
            data: {
                animal: $scope.animal,
                sighting: $scope.sighting
            }
        }).then(function(response) {
            console.log(response.data);
            $scope.query = $scope.savedSearch;
            $scope.search();
            $scope.sighting = {};
            $scope.animal = {};
        }, function(error) {
            console.log(error);
        });
    }

    $scope.deleteSighting = function($id, $id2) {
        $http({
            method: 'POST',
            url:'/deleteSighting',
            data: {
                animal: $id,
                sighting: $id2
            },
            headers: {'Content-Type': 'application/json; charset=UTF-8'}
        }).then(function(response) {
            console.log(response.data);
            $scope.query = $scope.savedSearch;
            $scope.search();
        }, function(error) {
            console.log(error);
        });
    }
});
