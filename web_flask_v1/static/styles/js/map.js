function initMap() {
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
}