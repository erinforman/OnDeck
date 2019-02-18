"use strict";

function initMap() {
  
$.get('/get_map_coords.json', (results) => {
        let locations = results['coords']

  const sfBayCoords = { lat: 37.601773, lng: -122.202870 };

  const map = new google.maps.Map(document.getElementById('map'), {
    zoom: 3,
    center: sfBayCoords,
    //center: new google.maps.LatLng(41.976816, -87.659916),
  });

  //const infowindow = new google.maps.InfoWindow({});

  let marker, i;

  for (i = 0; i < locations.length; i+=1) {

    let position = new google.maps.LatLng(locations[i][0], locations[i][1])
    
    marker = new google.maps.Marker({
      position: position,
      map: map
    });

    // google.maps.event.addListener(marker, 'click', (function (marker, i) {
    //   return function () {
    //     infowindow.setContent(locations[i][0]);
    //     infowindow.open(map, marker);
    //   }
    // })(marker, i));
  }
   });
}








// function initMap() {

// $.get('/get_map_coords.json', function (results) {
//     let locations = results['coords'];

//     const markers = locations.map(location => {
//     return addMarker(new google.maps.LatLng(location[0][0]), map);

//     markers.forEach(marker => {
//     addInfoWindowToMarker(marker, map);
//   });
//   });
//     });
// }


// function addMarker(position, map) {
//   const marker = new google.maps.Marker({ position, map});

//   return marker;
// }






