import {get_hospitals} from "./hospitals.js";
import {emergencyRequest} from "./request.js";

export function initMap() {
    var myLatLng = {lat: 5.6310532, lng: -0.3260097};

    var map = new google.maps.Map(document.getElementById('map'), {
    zoom: 12,
    center: myLatLng
    });

    var marker = new google.maps.Marker({
    position: myLatLng,
    map: map,
    title: 'Accra'
    });

    // create a DirectionsService object to use the route method and get a result for our request
    var directionsService = new google.maps.DirectionsService();

    // create a DirectionsRenderer object which we will use to display the route
    var directionsDisplay = new google.maps.DirectionsRenderer();

    // bind the DirectionsRenderer to the map
    directionsDisplay.setMap(map);

    // define calcRoute function
    function calcRoute() {

        // create request
        var request = {
            origin: document.getElementById("from").value,
            destination: document.getElementById("to").value,
            travelMode: google.maps.TravelMode.DRIVING, //WALKING, BYCYCLING, TRANSIT
            unitSystem: google.maps.UnitSystem.IMPERIAL
        }

        // pass the request to the route method
        directionsService.route(request, function(result, status) {
            if (status == google.maps.DirectionsStatus.OK) {
                // Get distance and time
                $("#output").html("<div class='alert-info'>From: " + document.getElementById("from").value + ".<br />To: " + document.getElementById("to").value + ".<br /> Driving distance: " + result.routes[0].legs[0].distance.text + ".<br />Duration: " + result.routes[0].legs[0].duration.text + ".</div>");
                // display route
                directionsDisplay.setDirections(result);
            } else {
                // delete route from map
                directionsDisplay.setDirections({routes: []});
                // center map
                map.setCenter(myLatLng);
                // show error message
                $("#output").html("<div class='alert-danger'>Could not retrieve driving distance.</div>");
            }
        });
    }

    // get_hospitals(map);
    // console.log(hosdata);

    // create autocomplete objects for all inputs
    // emergencyRequest(map);

    // window.onload = function () { initialize() };
}



// //restores the right pane of the contentContainer
// function restoreRightPane(){
//   var rightPane = document.createElement('div');
//   rightPane.setAttribute('class', 'split right');
//   //remove form from contentContainer and add rightPane
//   document.getElementsByClassName('contentContainer')[0].removeChild(document.getElementsByClassName('form-container')[0]);
//   document.getElementsByClassName('contentContainer')[0].appendChild(rightPane);
// }
