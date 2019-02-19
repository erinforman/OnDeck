"use strict";

function initMap() {
  
$.get('/get_map_coords.json', (results) => {
    let locations = results

    const sfBayCoords = { lat: 37.601773, lng: -122.202870 };

    const map = new google.maps.Map(document.getElementById('map'), {
      zoom: 3,
      center: sfBayCoords,
      //center: new google.maps.LatLng(41.976816, -87.659916),
    });

    const infowindow = new google.maps.InfoWindow({});

    let marker, i;

    for (i = 0; i < locations.length; i+=1) {

      let position = new google.maps.LatLng(locations[i].lat, locations[i].lng)
      
      marker = new google.maps.Marker({position: position,map: map});

      google.maps.event.addListener(marker, 'click', (function (marker, i) {
        return function () {
          infowindow.setContent(locations[i].url);
          infowindow.open(map, marker);
        }
      }) (marker, i));
      // function bindInfoWindow(marker, map, infoWindow, html) {
      // google.maps.event.addListener(marker, 'click', (marker,i) => {
      //       infoWindow.close();
      //       infoWindow.setContent(locations[i].url);
      //       infoWindow.open(map, marker);
      //   });
    }
   });
}






