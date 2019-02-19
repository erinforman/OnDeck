"use strict";

function initMap() {

  let myCenter = { lat: 37.601773, lng: -122.202870 };

  let map = new google.maps.Map(document.getElementById('map'), {
      zoom: 3,
      center: myCenter,
      //center: new google.maps.LatLng(41.976816, -87.659916),
  });
  
  let infoWindow = new google.maps.InfoWindow({
        width: 150
  });

  //Retrieve user locations with AJAX
  $.get('/get_map_coords.json', (results) => {

    let marker, position, html
  
    for (let location in results) {


      
     marker = new google.maps.Marker({
                          position: new google.maps.LatLng(results[location].lat, results[location].lng),
                          map: map,
                          animation: google.maps.Animation.DROP});



     
      html = ('<div class="window-content">' +
                    '<img src="/static/img/polarbear.jpg" alt="polarbear" style="width:150px;" class="thumbnail">' +
                    '<p><b>Name: </b>' + '**Put the name here**'+ '</p>' +
                    '<p><b>URL: </b>' + results[location].url + '</p>' +
                    '<p><b>Recommended by: </b>' + results[location].recommended_by + '</p>' +
                    '<p><b>Address: </b>' + results[location].formatted_address + '</p>' +
                    '<p><b>Saved: </b>' + results[location].date_stamp + '</p>' +
              '</div>');

        bindInfoWindow(marker, map, infoWindow, html);
    }
  });

    function bindInfoWindow(marker, map, infoWindow, html) {
        google.maps.event.addListener(marker, 'click', function () {
            infoWindow.close();
            infoWindow.setContent(html);
            infoWindow.open(map, marker);
        });
    }
}





    


 



