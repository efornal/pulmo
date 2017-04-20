$(document).ready(function() {

    // for existing rows
    $.each($("#tab_logic tbody tr:nth(0) td"), function() {
        $("a#delete_row").on("click", function() {
            if ( $('#tab_logic tr').length > 2 ) // header + first row
                $(this).closest("tr").remove();
        });
    });
    
    $("#add_row").on("click", function() {

        // Dynamic Rows Code
        // Get max row id and set new id
        var newid = $('#tab_logic tr').length - 2;

        
        $.each($("#tab_logic tr"), function() {
            if (parseInt($(this).data("id")) > newid) {
                newid = parseInt($(this).data("id"));
            }
        });
        newid++;
        
        var tr = $("<tr></tr>", {
            id: "addr"+newid,
            "data-id": newid
        });
        
        // loop through each td and create new elements with name of newid
        $.each($("#tab_logic tbody tr:nth(0) td"), function() {
            var cur_td = $(this);
            
            var children = cur_td.children();
            
            // add new td and element if it has a nane
            if ($(this).data("name") != undefined) {
                var td = $("<td></td>", {
                    "data-name": $(cur_td).data("name")
                });
                
                var c = $(cur_td).find($(children[0]).prop('tagName')).clone().val("");

                if (c.attr('type') == 'checkbox'){
                    c.attr("name", $(cur_td).data("name") + newid);
                }else{
                    c.attr("name", $(cur_td).data("name")+ "[]");
                }

                c.appendTo($(td));
                
                if ( $(this).data("name") == 'permissions' ) {
                    c.find("option").each(function(){
                        if ( $(this).attr("selected") == 'selected' ){
                            $(this).prop('selected', true);
                        }
                    });
                }
                td.appendTo($(tr));
            } else {
                var td = $("<td></td>", {
                    'text': $('#tab_logic tr').length
                }).appendTo($(tr));
            }
        });

        $(tr).appendTo($('#tab_logic'));

        $(tr).find("td a#delete_row").on("click", function() {
            if ( $('#tab_logic tr').length > 2 ) // header + first row
                $(this).closest("tr").remove();
        });

    });


    $("#delete_row").on("click", function() {
        if ( $('#tab_logic tr').length > 2 ) // header + first row
            $(this).closest("tr").remove();
    });



    $("#add_row1").on("click", function() {

        // Dynamic Rows Code
        // Get max row id and set new id
        var newid = $('#tab_logics tr').length - 2;

        $.each($("#tab_logics tr"), function() {
            if (parseInt($(this).data("id")) > newid) {
                newid = parseInt($(this).data("id"));
            }
        });
        newid++;
        
        var tr = $("<tr></tr>", {
            id: "addsr"+newid,
            "data-id": newid
        });
        
        // loop through each td and create new elements with name of newid
        $.each($("#tab_logics tbody tr:nth(0) td"), function() {
            var cur_td = $(this);
            
            var children = cur_td.children();
            
            // add new td and element if it has a nane
            if ($(this).data("name") != undefined) {
                var td = $("<td></td>", {
                    "data-name": $(cur_td).data("name")
                });
                
                var c = $(cur_td).find($(children[0]).prop('tagName')).clone().val("");
                if (c.attr('type') == 'checkbox'){
                    c.attr("name", $(cur_td).data("name") + newid);
                }else{
                    c.attr("name", $(cur_td).data("name")+ "[]");
                }
                c.appendTo($(td));
                td.appendTo($(tr));
            } else {
                var td = $("<td></td>", {
                    'text': $('#tab_logics tr').length
                }).appendTo($(tr));
            }
        });

        $(tr).appendTo($('#tab_logics'));


        $(tr).find("td a#delete_rows").on("click", function() {
            if ( $('#tab_logics tr').length > 2 ) // header + first row
                $(this).closest("tr").remove();
        });
    });

    $("#delete_rows").on("click", function() {
        if ( $('#tab_logics tr').length > 2 ) // header + first row
            $(this).closest("tr").remove();
    });
    
});
