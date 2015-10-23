 $(function(){

     $("#name").keypress(function(el){
         if(el.which == 13){
             search();
         }
     })

    $("#searchBtn").click(search)

     function search(){
        $("#search_error").hide()
        var name = $.trim($("#name").val());
        if(name.length < 4){
            $("#search_error").html("Search term must be at least 4 characters").show()
            return;
        }
        $.ajax({
            url : window.user_search_url,
            method: "post",
            data: {name: name, csrfmiddlewaretoken: window.csrf_token}
        }).done(displayUsers)

    }

    function displayUsers(users){
        console.log("Found users:", users);
        $("#user-list").html(users);
    }
});