var app = angular.module('wordApp', ["ng-file-model"]);

app.controller('tabController', function() {
    this.tab = 1;

    this.setTab = function(newTab){
      this.tab = newTab;
    };

    this.isSet = function(tabNum){
      return this.tab === tabNum;
    };
});

app.controller('wordController', function($scope, $http) {

    $scope.data = [];
    $scope.update = false;
    $scope.recording = false;
    $scope.playing = false;

    $scope.record = function() {
        var word = $scope.inputWord;
        if (!$scope.recording) {
            $scope.recording = true;
            $('#recordButton').removeClass('glyphicon-play');
            $('#recordButton').addClass('glyphicon-pause');
            $http({
                method: 'POST',
                url: '/record',
                data: word
            }).then(function(response) {
                console.log(response.data.message);
                if (response.data.status === 'OK') {
                    $('#saveButton').css('display', 'inline');
                } else {
                    alert("Salvestamine ebaõnnestus, proovige uuesti");
                }
                $scope.recording = false;
                $('#recordButton').removeClass('glyphicon-pause');
                $('#recordButton').addClass('glyphicon-play');
            }, function(error) {
                console.log(error);
            });
        }
    }

    $scope.play = function(word, index) {
        console.log("playing " + word.word + " " + word.audioFile);
        if (!$scope.playing) {
            $scope.playing = true;
            $('#playButton' + index).removeClass('glyphicon-play');
            $('#playButton' + index).addClass('glyphicon-pause');
            $http({
                method: 'POST',
                url: '/play',
                data: word
            }).then(function(response) {
                console.log(response);
                $scope.playing = false;
                $('#playButton' + index).removeClass('glyphicon-pause');
                $('#playButton' + index).addClass('glyphicon-play');
            }, function(error) {
                console.log(error);
            });
        }
    }

    $scope.chooseSavingMethod = function() {
        if ($scope.update) {
            $scope.updateWord();
        } else {
            $scope.addWord();
        }
    }

    $scope.addWord = function() {
        var word = $scope.inputWord;

        $http({
            method: 'POST',
            url: '/addWord',
            data: word
        }).then(function(response) {
            console.log(response.data.message);
            $scope.data = $scope.getAllWords();
        }, function(error) {
            console.log(error);
        });
    }

    $scope.updateWord = function() {
        var word = $scope.inputWord;

        $http({
            method: 'POST',
            url: '/updateWord',
            data: word
        }).then(function(response) {
            console.log(response.data.message);
            $scope.data = $scope.getAllWords();
        }, function(error) {
            console.log(error);
        });
    }

    $scope.getWord = function() {
        var word = $scope.inputWord;
        console.log(word);

        $http({
            method: 'POST',
            url: '/getWord',
            data: word,
            headers: {'Content-Type': 'application/json'}
        }).then(function(response) {
            console.log(response);
            if (response.data.message == 'entry not found') {
                $('#recordModal').modal();
                $scope.update = false;
            } else {
                $('#alertModal').modal();
                $scope.update = true;
            }
        }, function(error) {
            console.log(error);
        });
    }

    $scope.getAllWords = function() {

        $http({
            method: 'GET',
            url: '/getAllWords'
        }).then(function(response) {
            console.log(response);
            $scope.data = response.data;
            //$scope.inputWord = {};
        }, function(error) {
            console.log(error);
        });
    }

    $scope.hideButton = function() {
        $('#saveButton').css('display', 'none');
    }

    $scope.data = $scope.getAllWords();
});
