// "use strict";
function initMap() {
  // The location of Uluru
  var uluru = {lat: -25.344, lng: 131.036};
  // The map, centered at Uluru
  const map = new google.maps.Map(document.getElementById('map'), {zoom: 4, center: uluru});
  // The marker, positioned at Uluru
  var marker = new google.maps.Marker({position: uluru, map: map});
}



///https://stackoverflow.com/questions/3059044/google-maps-js-api-v3-simple-multiple-marker-example


  // Loop over hackbrightLocations to make lots of markers
  // const markers = [];
  // for (let hbLocation of hackbrightLocations) {
  //   markers.push(addMarker('static/imgs/marker.png', hbLocation.coords, hbLocation.name, map));
  // }


