var optionList = [];

$("#searchButton").click(function() {
    var query = $("#searchBox").val();
    
    if (query == "") {
        $("#searchDiv").addClass("shake");
        setTimeout(function() {
            $("#searchDiv").removeClass("shake");
        }, 1500);
    } else {
        //$("#select").fadeIn("slow", function() {});
        $("#select").removeClass('fadeOutDown');
        $("#select").addClass('fadeInUp');
        $("#select").show();
        $("#colourDiv").css({"animation-name":"changeColour", 
                             "animation-duration":"1.5s"
                            });
        setTimeout(function() {
            $("#colourDiv").css({"animation-name":"", 
                                 "animation-duration":""
                                });
        }, 1600);
        
        var url = 'http://api.themoviedb.org/3/search/tv?query=' + query + '&api_key=352194ddda8e247861a410b67ef3d40e';

        $.ajax({
            type: 'GET', 
            url: url,
            dataType: 'json',
            success: function (data) {
                var searchResults = $("#searchResults");
                searchResults.empty();
                var results = data.results;

                results.forEach(function(item) {
                    var option = '<option value="' + item.name+ '">' + item.name + '</option>';
                    searchResults.append(option);
                });
            },
            error: function() {
                console.log("Error");
            }
        });
    }
});

$("#searchBox").click(function() {
    $("#searchBox").val('');
    //$("#select").fadeOut("slow", function() {});
    //$("#select").hide();
    $("#select").removeClass('fadeInUp');
    $("#select").addClass('fadeOutDown');
});