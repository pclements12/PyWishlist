 $(function(){

    //handle confirming deletes
    var currentDeleteForm = null;

    $("form.delete a").click(function(ev){
        var $target = $(ev.target)
        currentDeleteForm = $target.closest("form")
        if(!currentDeleteForm){
            console.error("Couldn't find a form for delete command")
        }
        else{
            //delete anchor should have a data-name attribute
            showDeleteModal($target.data("name"))
        }
    })

    $("#deleteItemBtn").click(function(){
        currentDeleteForm.submit();
        currentDeleteForm = null;
    })

    $("#cancelDeleteBtn").click(function(){
        currentDeleteForm = null;
    })

    function showDeleteModal(itemName){
        var modal = $("#confirmDeleteModal")
        modal.find("#modalDeleteItemName").html(itemName)
        modal.modal("show");
    }



 })