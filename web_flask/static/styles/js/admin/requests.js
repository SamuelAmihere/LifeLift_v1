function get_requests(map, lat, lng, data){
    hosps = data.hospitals;
    num = data.No
    console.log(hosps);
    var myLatLng = {lat: parseFloat(lat), lng: parseFloat(lng)};
        
    var icon = {
        url: "../static/images/emergency-call.png", // url
        scaledSize: new google.maps.Size(30, 30), // scaled size
        // origin: new google.maps.Point(0,0), // origin
        // anchor: new google.maps.Point(0, 0) // anchor
    };
    title = "#"+num.toString()+"\n";
    for (var i = 0; i < hosps.length; i++) {
        if (i == hosps.length-1) {
            title += (i+1).toString()+". "+hosps[i].name.toString();
        } else {
            title += (i+1).toString()+". "+hosps[i].name.toString() + "\n";
        }
    }
    if (title == "") {
        title = num.toString();
    }

    var marker = new google.maps.Marker({
    position: myLatLng,
    map: map,
    title: title,
    icon: icon
    });

    // Add a spining circle of radius 2 to the caller's location
    var circle = new google.maps.Circle({
        map: map,
        radius: 800,    // 10 miles in metres
        fillColor: '#AA0000'
    });
    circle.bindTo('center', marker, 'position');
    // Add a spining circle of radius 2 to the caller's location
    // animate the circle with constant rotation, and transparency
    var rotate = 0;
    window.setInterval(function() {
        rotate += 3;
        circle.setOptions({
        strokeColor: '#0000FF',
        //change the color intensity by changing the fill color
        fillColor: (function() {
            var color = '#';
            for (var i = 0; i < 6; i++) {
            color += (Math.random() * 16 | 0).toString(16);
            }
            return color;
        })(Math.floor(Math.random() * 16777215).toString(16)),

        fillOpacity: 0.4,
        strokeOpacity: 0.8,
        strokeWeight: 2,
        animation: google.maps.Animation.BOUNCE,
        center: myLatLng,
        radius: 800,
        editable: true,
        draggable: true,
        visible: true,
        clickable: true,
        zIndex: 1,
        rotation: rotate
        });
    }, 1000);
} //END OF EMERGENCY REQUEST FUNCTION