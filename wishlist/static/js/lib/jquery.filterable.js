(function($) {
    //for use on table elements, filterInput can be any dom input element
	$.fn.filterable = function (options) {
        var defaults = {
            filterInput: null,
            extractValue: _extractValue,
            afterFilter: function(){},
            beforeFilter: function(){}
        };

        var prefs = $.extend({}, defaults, options);

        prefs.filterInput.on("keyup afterpaste", filter.bind(this));

        function _extractValue($tr, cls){
            return $.trim($tr.find("span."+cls).text());
        }

        function filter(event){
            plug(this, prefs.beforeFilter);
            var value = $.trim($(event.target).val());

            var regexp = new RegExp(value, "i");
            var sortClasses = $.map(this.find("th.sort"), function(th){
                return $(th).data("sort");
            });

            this.find("tbody>tr").each(function(){
                var $tr = $(this);
                var match = false;
                //console.log("checking row", $tr);
                for(var i in sortClasses){
                    var cls = sortClasses[i];
                    var cellValue = prefs.extractValue($tr, cls);
                    match = regexp.test(cellValue);
                    if (match){
                        //console.log("matched column", cls, " on value: ", cellValue);
                        break;
                    }

                }
                $tr.toggle(match);
            })
            plug(this, prefs.afterFilter);
        }

        function plug(context, func){
            if(typeof func === "function"){
               func.call(context);
            }
        }
	}
})(jQuery);