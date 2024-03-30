function get_hospitals(map){
  
    // var hosdata = get_data('localhost:5005/api/v1/hospitals');

    // place markers on the map
    for (var i = 0; i < hosdata.length; i++) {
      var lat = hosdata[i].latitude;
      var lng = hosdata[i].longitude;
      var name = hosdata[i].name;
      var myLatLng = {lat: parseFloat(lat), lng: parseFloat(lng)};
      var marker = new google.maps.Marker({
        position: myLatLng,
        map: map,
        title: name
      });
  
      // Add a spining circle of radius 2 to the caller's location
      var circle = new google.maps.Circle({
        map: map,
        radius: 200,    // 10 miles in metres
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
          radius: 400,
          editable: true,
          draggable: true,
          visible: true,
          clickable: true,
          zIndex: 1,
          rotation: rotate
        });
      }, 1000);
    }
  }

// function get_data(ur){
//   //use jquery
//   var data = [];
//   $.ajax({
//     url: ur,
//     type: 'GET',
//     async: false,
//     success: function(response){
//       data = response;
//       console.log(data);
//     }
//   });
//   return data;
// }