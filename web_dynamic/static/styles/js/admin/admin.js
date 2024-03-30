// display <table class="table-striped"> on the right side of the page
// when clicks on  <li class="hos"> 
// and hide the table when clicks on <li class="hos"> again
// $('.hosp').toggle('on')
$(".table-striped").toggle("off");
$(".table-striped-pat").toggle("off");
$(".filter-table").toggle("off");
$(document).ready(function(){
    // Hospitals
    $(".hosp").click(function(){
        ///change title in h1 to "Hospitals"
        document.getElementById("tit").innerHTML = "Hospitals";
        if ($(".filter-table").is(":visible")){
            $('input').attr('placeholder','Search for hospital..');
        } else {
            $(".filter-table").toggle("on");
            $('input').attr('placeholder','Search for hospital..');
        }
        //change placeholder of filter-table to 'Search for hospital..'
        $('input').attr('placeholder','Search for hospital..');

        var element3 = document.querySelector("#submenuEmvs");
        var element2 = document.querySelector("#submenuPa");
        var element1 = document.querySelector("#submenuHos");

        if (element1.classList.contains("active")){
            element1.classList.replace("active", "newClass");
        }
        if (element2.classList.contains("newClass")){
            element2.classList.replace("newClass", "active");
        }
        if (element3.classList.contains("newClass")){
            element3.classList.replace("newClass", "active");
        }
        
        //make hos unclickable: pointer-events: none;
        document.getElementById("hos").style.pointerEvents = "none";
         //make pat lickable: pointer-events: auto;
        document.getElementById("pa").style.pointerEvents = "auto";
        document.getElementById("emvs").style.pointerEvents = "auto";


        if ($(".table-striped-pat").is(":visible")) {
            $(".table-striped-pat").toggle("off");
            
        } 
        $(".table-striped").toggle("on");

        //turn off hos

        
        // if (element1.classList.contains("newClass")){
        //     element1.classList.replace("newClass", "active");
        // }


        

        //get <table class="table-striped"> and update it's content with column: Name, Latitude, Longitude, Alerts
    }
    );


    // Patient Requests


    // Emergency Vehicles
    $(".emvs-c").click(function(){
        //change title in h1 to "Patients"
        document.getElementById("tit").innerHTML = "Vehicles";
        //change placeholder of filter-table to 'Search for patients..'
        if ($(".filter-table").is(":visible")){
            $('input').attr('placeholder','Search for vehicles..');
        } else {
            $(".filter-table").toggle("on");
            $('input').attr('placeholder','Search for vehicles..');
        }
        
       
        var element1 = document.querySelector("#submenuHos");
        var element2 = document.querySelector("#submenuPa");
        var element3 = document.querySelector("#submenuEmvs");

        if (element3.classList.contains("active")) {
            element3.classList.replace("active", "newClass");
        }
        if (element1.classList.contains("newClass")){
            element1.classList.replace("newClass", "active");
        }
        if (element2.classList.contains("newClass")){
            element2.classList.replace("newClass", "active");
        }

        
        //make hos and pat unclickable: pointer-events: none;
        document.getElementById("emvs").style.pointerEvents = "none";
         //make emv lickable: pointer-events: auto;
        document.getElementById("pa").style.pointerEvents = "auto";
        document.getElementById("hos").style.pointerEvents = "auto";

        // if ($(".table-striped").is(":visible") || $(".table-striped-pat").is(":visible")) {
        //     $(".table-striped").toggle("off");
        //     $(".table-striped-pat").toggle("off");
        // }
        // $(".table-striped-emvs").toggle("on");
        // $(".table-striped-pat").toggle("on");



        
        // Create Patients table:

        
        //get <table class="table-striped"> and update it's content with column: Name, Latitude, Longitude, Alerts
    }
    );
});



// $(document).ready(function(){
    
// });


function load_patients(no_req){
    //get total patient requests stored in table property, value
    var totalRequests = $(".table-striped-pat").val()
    //change title in h1 to "Patients"
    document.getElementById("tit").innerHTML = "Requests [#"+no_req+"]";
    //change placeholder of filter-table to 'Search for patients..'
    if ($(".filter-table").is(":visible")){
        $('input').attr('placeholder','Search for patients..');
    } else {
        $(".filter-table").toggle("on");
        $('input').attr('placeholder','Search for Patients..');
    }
    
   
    var element3 = document.querySelector("#submenuEmvs");
    var element2 = document.querySelector("#submenuPa");
    var element1 = document.querySelector("#submenuHos");



    if (element2.classList.contains("active")){
        element2.classList.replace("active", "newClass");
    } 
    
    if (element1.classList.contains("newClass")){
        element1.classList.replace("newClass", "active");
    }
    if (element3.classList.contains("newClass")){
        element3.classList.replace("newClass", "active");
    }
    
    //make hos unclickable: pointer-events: none;
    document.getElementById("pa").style.pointerEvents = "none";
     //make pat lickable: pointer-events: auto;
    document.getElementById("hos").style.pointerEvents = "auto";
    document.getElementById("emvs").style.pointerEvents = "auto";

    if ($(".table-striped").is(":visible")) {
        $(".table-striped").toggle("off");
    }
    $(".table-striped-pat").toggle("on");



    
    // Create Patients table:

    
    //get <table class="table-striped"> and update it's content with column: Name, Latitude, Longitude, Alerts
}

//get all the properties of the td inside table class="table-striped-pat" id="table-hosp-pat"

function get_patients(){
    // get the tr of class="table-striped-pat"
    var tr = document.getElementsByClassName("table-striped-pat")[0];
    if (!tr){
        return [];
    }
    ids = []
    for (var i=0; i<tr.children[1].rows.length; i++){
        ids.push(tr.children[1].rows[i].getAttribute("id"));
        var data = $("#"+tr.children[1].rows[i].getAttribute("id")).data('value');
        if (data){
            console.log(data);
        }
    }
    return ids;
}

function get_data(){
    get_patients();
}