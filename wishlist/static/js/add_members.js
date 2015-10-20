 $(function(){

    $("#searchBtn").click(function(){

        var name = $.trim($("#name").val());
        $.ajax({
            url : window.user_search_url,
            method: "post",
            data: {name: name, csrfmiddlewaretoken: window.csrf_token}
        }).done(displayUsers)

    })

    function displayUsers(users){
        console.log("Found users:", users);
        $("#user-list").html(users);
    }
});