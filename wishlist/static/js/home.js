 $(function(){

    //handle confirming deletes
    var currentDeleteForm = null;

    var cdefaults = {
        title: "Delete",
        action: "delete",
        item: "this item"
    }

    function cap(string){
        return string.charAt(0).toUpperCase() + string.slice(1);
    }

    //Configurable: title/action/item
    //eg: title: Delete?, action: delete, item = "my item name"
    //produces:
    //{{title}}!?
    //"Are you sure you want to {{action}} {{item}}?

    $("form.delete .delete").click(function(ev){
        var $target = $(ev.target)
        currentDeleteForm = $target.closest("form")
        if(!currentDeleteForm){
            console.error("Couldn't find a form for delete command")
        }
        else{
            //delete anchor should have a data-name attribute
            var options = {
                title: $target.data("title"),
                action: $target.data("action"),
                item: $target.data("name")
            }

            showDeleteModal($target, $.extend(cdefaults, options))
        }
    })

    function populateModal($modal, options){
        $modal.find(".confirmation-title").html(options.title)
        $modal.find(".confirmation-action").html(options.action)
        $modal.find(".confirmation-button").html(cap(options.action))
        $modal.find(".confirmation-item").html(options.item)
    }

     function populateModalError($modal, error){

     }

    $("#deleteItemBtn").click(function(){
        if(currentDeleteForm.data("ajax") == true){
            currentDeleteForm.ajaxSubmit();
            currentDeleteForm.data("jqxhr").done(function(response){
                currentDeleteForm.trigger("delete:success", {
                    response:response,
                    form: currentDeleteForm
                });
            }).fail(function(response){
                currentDeleteForm.trigger("delete:fail", {
                    response: response,
                    form: currentDeleteForm
                })
            }).always(function(){
                currentDeleteForm = null;
                $(this).closest(".modal").modal("hide");
            });
        }
        else{
            currentDeleteForm.submit();
            currentDeleteForm = null;
        }
    })

    $("#cancelDeleteBtn").click(function(){
        currentDeleteForm = null;
    })

    function showDeleteModal(itemName, options){
        var $modal = $("#confirmDeleteModal")
        populateModal($modal, options);
        $modal.modal("show");
    }

    //handle item claim/unclaim ajax calls

    function bindClaimListeners(){
        console.log("rebind claim click listeners");
        //make sure we remove existing click listeners if we re-bind
        $("a.claim, a.unclaim").off("click");
        $("a.claim, a.unclaim").click(function(ev){
            ev.preventDefault();
            var $anchor = $(ev.target);
            //parse item id and url from event/target
            var url = $anchor.data("url");
            //show loading icon
            $anchor.data("text", $anchor.html());
            showLoading($anchor)
            if($anchor.hasClass("claim")){
                do_call(url)
                  .success(claimSuccess($anchor))
                  .always(hideLoading($anchor))
            }
            else{
                do_call(url)
                 .success(unclaimSuccess($anchor))
                 .always(hideLoading($anchor))
            }
        })
    }

    //register initial listeners
    bindClaimListeners();

    function showLoading($anchor){
        $anchor.find("i").addClass("fa-spin"); //.html("...")
    }

    function hideLoading($anchor){
        return function(response){
            $anchor.html($anchor.data("text")).find("i").removeClass("fa-spin")
        }
    }

    function do_call(url){
        //post to service to claim item
        return $.ajax({
            method: "POST",
            url: url,
            data: {csrfmiddlewaretoken: window.csrf_token}
        })
    }

    function claimSuccess($anchor){
        //move item from available to claimed
        return function(response){
            var $table = $anchor.closest("table");
            var data = {element: $anchor, response: response, claim:true, index: $anchor.index()};
            $table.trigger("item:beforeClaim", data);
            $anchor.closest("tr").remove()
            $("#claimed tbody").append("<tr>"+response+"</tr>")
            $table.trigger("item:claimSuccess", data);
            bindClaimListeners();
            checkEmptyLists();
        }
    }

    function unclaimSuccess($anchor){
        return function(response){
            var $table = $anchor.closest("table");
            var data = {element: $anchor, response: response, claim:true, index: $anchor.index()};
            $table.trigger("item:beforeClaim", data);
            $anchor.closest("tr").remove()
            $("#available tbody").append("<tr>"+response+"</tr>")
            $table.trigger("item:unclaimSuccess", data);
            bindClaimListeners();
            checkEmptyLists();
        }
    }

    function checkEmptyLists(){
         checkEmptyList($("#available"));
         checkEmptyList($("#claimed"));
    }

     window.checkEmptyLists = checkEmptyLists;

    function checkEmptyList($table){
        var no_items = $table.find("tbody tr").length == 1;
        $table.find(".no-items").toggle(no_items);
    }

 })