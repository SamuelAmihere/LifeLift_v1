// display <table class="table-striped"> on the right side of the page
// when clicks on  <li class="hos"> 
// and hide the table when clicks on <li class="hos"> again
// $('.hosp').toggle('on')
$(".table-striped").toggle("off");
$(document).ready(function(){
    $(".hosp").click(function(){
        ///change title in h1 to "Hospitals"
        document.getElementById("tit").innerHTML = "Hospitals"; 

        var element2 = document.querySelector("#submenuPa");
        var element1 = document.querySelector("#submenuHos");

        if (element1.classList.contains("active")){
            element1.classList.replace("active", "newClass");
        }
        if (element2.classList.contains("newClass")){
            element2.classList.replace("newClass", "active");
        }
        
        //make hos unclickable: pointer-events: none;
        document.getElementById("hos").style.pointerEvents = "none";
         //make pat lickable: pointer-events: auto;
        document.getElementById("pa").style.pointerEvents = "auto";


        $(".table-striped").toggle("on");

        //turn off hos

        
        // if (element1.classList.contains("newClass")){
        //     element1.classList.replace("newClass", "active");
        // }


        

        //get <table class="table-striped"> and update it's content with column: Name, Latitude, Longitude, Alerts
    }
    );
});

$(document).ready(function(){
    $(".pat").click(function(){

        //change title in h1 to "Patients"
        document.getElementById("tit").innerHTML = "Patients";

        var element2 = document.querySelector("#submenuPa");
        var element1 = document.querySelector("#submenuHos");


        if (element2.classList.contains("active")){
            element2.classList.replace("active", "newClass");
        } 
        
        if (element1.classList.contains("newClass")){
            element1.classList.replace("newClass", "active");
        }
        
        //make hos unclickable: pointer-events: none;
        document.getElementById("pa").style.pointerEvents = "none";
         //make pat lickable: pointer-events: auto;
        document.getElementById("hos").style.pointerEvents = "auto";

        $(".table-striped").toggle("on");
        
        //get <table class="table-striped"> and update it's content with column: Name, Latitude, Longitude, Alerts
    }
    );
});

// display <table class="table-striped"> on the right side of the page
// when clicks on  <li class="pat"> 
// and hide the table when clicks on <li class=""> again

// $(document).ready(function(){
//     $(".hosp").click(function(){
//         //create table for hospital and place it on the right side of the page
        


//         $(document).ready(function(){
//             $(".table-striped").click(function(){
//                 $(".table-striped").toggle();
//             });
//         });

//     });
// });

// var hosdata = JSON.parse(document.getElementById('hos').dataset.hospitals);