 $(function(){

    //handle confirming deletes
    var currentDeleteForm = null;

    cdefaults = {
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

    $("form.delete a.delete").click(function(ev){
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

    $("#deleteItemBtn").click(function(){
        currentDeleteForm.submit();
        currentDeleteForm = null;
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
            $anchor.closest("tr").remove()
            $("#claimed tbody").append("<tr>"+response+"</tr>")
            bindClaimListeners();
            checkEmptyLists();
        }
    }

    function unclaimSuccess($anchor){
        return function(response){
            $anchor.closest("tr").remove()
            $("#available tbody").append("<tr>"+response+"</tr>")
            bindClaimListeners();
            checkEmptyLists();
        }
    }

    function checkEmptyLists(){
         checkEmptyList($("#available"));
         checkEmptyList($("#claimed"));
    }

    function checkEmptyList($table){
        var no_items = $table.find("tbody tr").length == 1;
        $table.find(".no-items").toggle(no_items);
    }

 })