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
        $("#user-list").html(users);
    }

     $("#inviteEmail").keypress(function(el){
         if(el.which == 13){
             invite();
         }
     })

    $("#sendInviteBtn").click(invite);

    function invite(ev){
        var emailInput = $("#inviteEmail");
        var email = $.trim(emailInput.val());
        var error = $("#invite_error").hide();
        var msg = $("#invite_msg").hide();
        if(email.length == 0 || email.indexOf("@") == -1){
            error.text("Please input a proper email address!").show();
            return;
        }
        console.log("invite", ev);
        var element = $(ev.target);
        element.prop("disabled", true);
        $.ajax({
            method: "post",
            url: element.data("url"),
            data: {
                csrfmiddlewaretoken: window.csrf_token,
                email: email,
                group_id: window.group_id
            }}
        ).done(function(){
            element.prop("disabled", false);
            msg.text(email + " invited successfully!").show();
            emailInput.val('');
        })
        .fail(function(){
            element.prop("disabled", false);
            error.text("Something went wrong. Try again later.").show();
        })
    }
});