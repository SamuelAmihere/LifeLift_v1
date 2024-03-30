
// Add event listener to class="hospitals-distance"

document.addEventListener('DOMContentLoaded', function() {
  var hp = document.getElementById('hospitals-distance')
  create_table(hp);
});



function emergencyRequest(map){
    // Event listener to call generateRoute random latitudes and longitudes pairs
    // within a city on the map when the button (call-199) is clicked

    // first check if the form is already on the page, if so remove it

    document.getElementById('req-btn').addEventListener('click', function() {
      // get hospitals: lat, lng
      var lat = (Math.random() * (5.7 - 5.5) + 5.5).toFixed(6);
      var lng = (Math.random() * (-0.2 - -0.4) + -0.4).toFixed(6);
      var myLatLng = {lat: parseFloat(lat), lng: parseFloat(lng)};
      console.log(lat, lng);
      // get hospitals close to the caller's location

      var hospitals = retrive_close_hosps(lat, lng, top=3).hospitals;
      if (hospitals == undefined) {
        hospitals = [{name: 'Korle Bu', distance: '2.3km'}];
      }
      console.log(hospitals);

      table = document.getElementsByClassName('hosp-tb');
      if (table) {
        fill_table(hospitals);
      }

      // create table and append to the div: 'hospitals-distance'
      

      console.log(myLatLng)
      // First Give a caller a suspended form at center of window to fill for emergency request
      // The form will be submitted to the server for ambulance to pick up

      //create dive
      //set the form container

      var formContainer = document.createElement('div');
      formContainer.setAttribute('class', 'emergency-form-container');

      //create form and add to div: emergency-form-container
      var form = document.createElement('form');
      form.setAttribute('method', 'post');
      form.setAttribute('action', '/emergency_request');
      form.setAttribute('id', 'emergency-form');
      form.setAttribute('class', 'form-container');
      form.innerHTML = `
      <div class="request_container">
        <div id="request-header">
            <h2> Request for emergency service</h1>
         </div>
            <input type="text" id="location" name="location" value="Accra" readonly>
          <hr>
  
          <div class="col-md-6 req-inp">
            <input type="text" class="form-control" id="fname" name="fname" 
            placeholder="First Name">
          </div>
          <div class="col-md-6 req-inp">
            <input type="text" class="form-control" id="lname" name="lname" 
            placeholder="Last Name">
          </div>
          <div class="col-md-6 req-inp">
            <input type="email" class="form-control" id="email"  name="email" 
            placeholder="Email">
          </div>
          <div class="col-md-6 req-inp">
            <input type="text" class="form-control" id="phone" name="phone" 
            placeholder="Phone Number">
          </div>
  
          <div class="col-md-6 req-inp">
            <input type="text" class="form-control" id="street" name="street" 
            placeholder="Street">
          </div>
          <div class="col-md-6 req-inp">
            <input type="text" class="form-control" id="relative_phone" name="relative_phone" 
            placeholder="Relative Phone">
          </div>
  
          <div class="col-md-4">
              <select id="incident_type" name="incident_type" class="form-select">
                  {% for o in incident_type %}
                  <option value="{{ o }}" >{{ o }}</option>
                  {% endfor %} 
              </select>
          </div><br>
  
          <div class="col-md-2" style="width:15px; height: 10px;">
                  <select id="gender" name="gender" class="form-select">
                    <option>gender...</option>
                      <option value="male" >male</option>
                      <option value="female" >female</option>
                      <option value="other" >other</option>
                  </select>
          </div><br>
  
          <div class="row-md-4">
            <textarea id="incident_description" name="incident_description"rows="4" cols="50" placeholder="Describe here..."></textarea> 
          </div>
          <button type="submit" class="btn">Submit</button>
          <br>
      </div>
      `;
      //add + and - to form (at top right corner) for maximizing and minimizing the form


      //add event listener to the plus and minus buttons

      form = add_min_max(form);



      formContainer.appendChild(form);
      document.body.appendChild(formContainer);
       
  
  
      // update the existing map passed as the paraameter the caller's location
  
      map.setCenter(myLatLng);
      map.setZoom(14);
      //set title
      map.setOptions({title: 'Accra'});
        
      var marker = new google.maps.Marker({
        position: myLatLng,
        map: map,
        title: 'Accra'
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
  
  
    // authenticate the request form: 'emergency-form'
      // prevent empty fields from being submitted
      var em_form = document.getElementById('req-btn');
      if (em_form) {
        em_form.addEventListener('submit', function(e) {
        e.preventDefault();
        var fname = document.getElementById('fname').value;
        var lname = document.getElementById('lname').value;
        var email = document.getElementById('email').value;
        var phone = document.getElementById('phone').value;
        var street = document.getElementById('street').value;
        var relative_phone = document.getElementById('relative_phone').value;
        var incident_type = document.getElementById('incident_type').value;
        var incident_description = document.getElementById('incident_description').value;
  
        var fields = {fname: 'fname', lname: 'lname', email: 'email', phone: 'phone', street: 'street', relative_phone: 'relative_phone', incident_type: 'incident_type', incident_description: 'incident_description'};
        
        // highlight empty fields and stop form submission
  
        // check if any of the fields is empty
        // for (var i = 0; i < fields.length; i++) {
        //   if (fields[i] == '') {
        //     fields[i].style.border = '1px solid red';
        //     fields[i].style.backgroundColor = 'rgba(255, 0, 0, 0.1)';
  
        //     // highlight the empty field
        //     fields[i].focus();
        //     return false;
  
        //   } 
        // }
        // if all fields are filled, submit the form
        if (fname != '' && lname != '' && email != '' && phone != '' && street != '' && relative_phone != '' && incident_type != '' && incident_description != '') {
          document.getElementById('emergency-form').submit();
        } else {
          highlightEmptyFields(fields);
        }
  
      }); //END OF EVENT LISTENER: 'emergency-form'
  
      }

  
      if (em_form) {
      // disable call button until form is submitted
      em_form.disabled = true;
      }
    });//END OF EVENT LISTENER
  
    
  } //END OF EMERGENCY REQUEST FUNCTION



function highlightEmptyFields(fields)
{
  for (var i = 0; i < fields.length; i++) {
    if (fields[i] == '') {
      fields[i].style.border = '1px solid red';
      fields[i].style.backgroundColor = 'rgba(255, 0, 0, 0.1)';
      console.log(fields[i]);

      // highlight the empty field
      fields[i].focus();
      return false;

    } 
  }
}

function retrive_close_hosps(lat, lng, top){
  // Retrieve hospitals close to the caller's location
  
  //use jquery
  var data = [];

  ur = 'http://127.0.0.1:5005/api/v1/incident/hospitals/';
  req_data = {
    lat: lat,
    lng: lng,
    top: top
  };

  $.ajax({
    url: ur,
    type: 'GET',
    async: false,
    data: req_data,
    success: function(response){
      data = response;
    }
  });
  return data;
}


function create_table(div_to_append) {
  // Create table and append to the div passed as the parameter
  // fill table with data: {{name:..., distance:...},...}
  
  // var div_to_append = document.getElementById(append);


  var table = document.createElement('table'); //table class="hosp-tb"
  table.setAttribute('class', 'hosp-tb');
  var thead = document.createElement('thead');
  var tbody = document.createElement('tbody');
  tbody.setAttribute('id', 'tbodyy');
  var tr = document.createElement('tr');
  var th1 = document.createElement('th');
  var th2 = document.createElement('th');
  var th3 = document.createElement('th');
  th1.innerHTML = 'Hospital';
  th2.innerHTML = 'Distance';
  th3.innerHTML = 'Location';
  tr.appendChild(th1);
  tr.appendChild(th2);
  tr.appendChild(th3);
  thead.appendChild(tr);
  table.appendChild(thead);
  table.appendChild(tbody);
  
  div_to_append.appendChild(table);
}

function fill_table(data){
  // Fill the table with data
  // table: {name:..., distance:...}
  var tbody = document.getElementById('tbodyy');

  if (tbody){
    for (var j = 0; j < data.length; j++) {
      var tr = document.createElement('tr');
      var td1 = document.createElement('td');
      var td2 = document.createElement('td');
      var td3 = document.createElement('td');
      td3.setAttribute('id', 'hosp-loc');
      //add name, lat and lng to the td3 as attributes
      td3.setAttribute('data-lng', data[j].longitude);
      td3.setAttribute('data-lat', data[j].latitude)
      td3.setAttribute('data-name', data[j].name)
      // create link child for td3
      var a = document.createElement('a');
      a.setAttribute('href', '#');
      //add font awesome icon to the link
      var i = document.createElement('i');
      i.setAttribute('class', 'fa-solid fa-location-dot');
      a.appendChild(i);
      td3.appendChild(a);
      
      //add class name to the td for names and distance
      td1.setAttribute('class', 'hosp-name');
      td2.setAttribute('class', 'hosp-dist');

      td1.innerHTML = data[j].name;
      td2.innerHTML = data[j].distance;
      tr.appendChild(td1);
      tr.appendChild(td2);
      tr.appendChild(td3);
      tbody.appendChild(tr);
    }
  }

}


function add_min_max(form){
  //
    var plus = document.createElement('button');
    plus.setAttribute('class', 'plus');
    plus.innerHTML = '+';
    var minus = document.createElement('button');
    minus.setAttribute('class', 'minus');
    minus.innerHTML = '-';
    form.appendChild(plus);
    form.appendChild(minus);

    plus.addEventListener('click', function() {
      if (form.style.display == 'none') {
        form.style.display = 'block';
        form.style.width = '100%';
        form.style.height = '100%';
        form.style.position = 'absolute';
        form.style.top = '0';
        form.style.left = '0';
        form.style.zIndex = '1000';
        form.style.backgroundColor = 'rgba(0, 0, 0, 0.5)';
        form.style.color = 'white';
        form.style.overflow = 'auto';
        form.style.padding = '20px';
        form.style.border = '1px solid white';
        form.style.borderRadius = '10px';
        form.style.boxShadow = '0 0 10px 5px rgba(0, 0, 0, 0.5)';
        form.style.transition = 'all 0.5s';
        form.style.transitionTimingFunction = 'ease-in-out';
        form.style.transitionDelay = '0.5s';
        form.style.transitionDuration = '0.5s';
        form.style.transitionProperty = 'all';
  
        plus.style.display = 'none';
        minus.style.display = 'block';
      }
  });
  minus.addEventListener('click', function() {
    if (form.style.display == 'block') {
      form.style.display = 'none';
      plus.style.display = 'block';
      minus.style.display = 'none';

      // prevent submit
    }
  }
  );
  return form
}