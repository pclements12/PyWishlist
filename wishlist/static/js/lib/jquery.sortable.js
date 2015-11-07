(function($) {
	$.fn.sortable = function () {
		var tbody = this.find('tbody');
		var $th = this.find('thead th.sort');

        var $sort_column = null;

        function extract_value(tr) {
            var $cell = $(tr).find('td').eq($sort_column.index());
            var $header = $sort_column

            var sort_value = $cell.find("span."+$header.data("sort")).text();
            sort_value = $.trim(sort_value);
            var data_sort_value = $cell.data('sort-value');
            if(typeof data_sort_value !== "undefined") {
                sort_value = data_sort_value;
            }

            return sort_value;
        }

        function compare(tr_a, tr_b) {
            var aval = extract_value(tr_a);
            var bval = extract_value(tr_b);

            if(isNaN(aval) || isNaN(bval)) {
                return aval.localeCompare(bval);
            }
            else{
                aval = parseFloat(aval);
                bval = parseFloat(bval);
                return (aval > bval ? 1 : (bval > aval) ? -1 : 0);
            }
        }

        function reverseCompare(a, b){
            return -1 * compare(a, b);
        }

		function sort_by_column($th, desc) {
			$sort_column = $th;
            var rows = tbody.find('tr');

            if(desc){
                rows.sort(reverseCompare)
            }
            else{
                rows.sort(compare);
            }

            tbody.append(rows);
		}

        function sortClick(ev){
            var header = $(ev.target);
            //clear previous sort markings
            header.siblings(".sort").removeClass("asc").removeClass("desc")
            //set sort markings on current column
            var desc = false;
            if(header.hasClass("asc")){
                header.removeClass("asc");
                header.addClass("desc");
                desc = true;
            }
            else{
                //default to ascending sort when no sort applied
                header.removeClass("desc");
                header.addClass("asc");
            }
            sort_by_column(header, desc);
        }

        $th.on("click", sortClick);
	}
})(jQuery);