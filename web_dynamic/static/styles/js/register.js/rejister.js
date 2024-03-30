// Check the user category chosen
//if nurse is chosen, show <select id="company"> to show only hospitals

$("#userType").
change(function(){
    if($(this).val() == "nurse"){
        $(".company").show();
        $(".company").find("option").each(function(){
            if($(this).val() != "Hospital"){
                $(this).hide();
            }
        });
    }
    else{
        $(".company").find("option").each(function(){
            $(this).show();
        });
    }
});
