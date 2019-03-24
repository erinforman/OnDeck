"use strict";
const userId = $('input[name="user_id"]').val();

function attachAddLocationHandler(map) {
  $("#map_form").on("submit", evt => {
    evt.preventDefault();

    const form = $(evt.target);
    let new_url = $('input[name="url"]').val()
    let new_helper_search_terms = $('input[name="helper_search_terms"]').val()
    let new_recommended_by = $('input[name="recommended_by"]').val()
    const formValues = {
      url: new_url,
      helper_search_terms: new_helper_search_terms,
      recommended_by: new_recommended_by
    };

    $.post(`/map/${userId}`, formValues, results => {
      if ((typeof results) === "string"){
        alert("We couldn't find an exact location for that URL. Try adding a city, state, or business name to the search.")
        window.stop()}

      else if ('geometry' in results) {
        let lat = results['geometry']['location']['lat'];
        let lng = results['geometry']['location']['lng'];
        let lastLatLng = new google.maps.LatLng(parseInt(lat), Number(lat));
        let marker = new google.maps.Marker({
          position: { lat, lng },
          map: map,
          animation: google.maps.Animation.DROP,
          icon: "https://img.icons8.com/doodle/48/000000/marker.png"
        });
        const infoWindow = new google.maps.InfoWindow({ maxWidth: 350 });     
        const html = ('<div class="window-content">' +
          '<p><a href=' + new_url + '>' + new_url + '</a></p>' +
          `${new_recommended_by
            ?`<p><b>Recommended by: </b>${new_recommended_by}</p>`
            : ''
          }` +
          '</div>');
        bindInfoWindow(marker, map, infoWindow, html);
        marker.setMap(map)
        map.setCenter({ lat, lng });
        map.setZoom(7);
      }
    });
  });
}

// Google Map Styling
const styles = [
  {
    "elementType": "geometry",
    "stylers": [
    {
      "color": "#ebe3cd"
    }
    ]
  },
  {
    "elementType": "labels.text.fill",
    "stylers": [
      {
        "color": "#523735"
      }
    ]
  },
  {
    "elementType": "labels.text.stroke",
    "stylers": [
      {
        "color": "#f5f1e6"
      }
    ]
  },
  {
    "featureType": "administrative",
    "elementType": "geometry.stroke",
    "stylers": [
      {
        "color": "#c9b2a6"
      }
    ]
  },
  {
    "featureType": "administrative.land_parcel",
    "elementType": "geometry.stroke",
    "stylers": [
      {
        "color": "#dcd2be"
      }
    ]
  },
  {
    "featureType": "administrative.land_parcel",
    "elementType": "labels.text.fill",
    "stylers": [
      {
        "color": "#ae9e90"
      }
    ]
  },
  {
    "featureType": "landscape.natural",
    "elementType": "geometry",
    "stylers": [
      {
        "color": "#dfd2ae"
      }
    ]
  },
  {
    "featureType": "poi",
    "elementType": "geometry",
    "stylers": [
      {
        "color": "#dfd2ae"
      }
    ]
  },
  {
    "featureType": "poi",
    "elementType": "labels.text.fill",
    "stylers": [
      {
        "color": "#93817c"
      }
    ]
  },
  {
    "featureType": "poi.park",
    "elementType": "geometry.fill",
    "stylers": [
      {
        "color": "#a5b076"
      }
    ]
  },
  {
    "featureType": "poi.park",
    "elementType": "labels.text.fill",
    "stylers": [
      {
        "color": "#447530"
      }
    ]
  },
  {
    "featureType": "road",
    "elementType": "geometry",
    "stylers": [
      {
        "color": "#f5f1e6"
      }
    ]
  },
  {
    "featureType": "road.arterial",
    "elementType": "geometry",
    "stylers": [
      {
        "color": "#fdfcf8"
      }
    ]
  },
  {
    "featureType": "road.highway",
    "elementType": "geometry",
    "stylers": [
      {
        "color": "#f8c967"
      }
    ]
  },
  {
    "featureType": "road.highway",
    "elementType": "geometry.stroke",
    "stylers": [
      {
        "color": "#e9bc62"
      }
    ]
  },
  {
    "featureType": "road.highway.controlled_access",
    "elementType": "geometry",
    "stylers": [
      {
        "color": "#e98d58"
      }
    ]
  },
  {
    "featureType": "road.highway.controlled_access",
    "elementType": "geometry.stroke",
    "stylers": [
      {
        "color": "#db8555"
      }
    ]
  },
  {
    "featureType": "road.local",
    "elementType": "labels.text.fill",
    "stylers": [
      {
        "color": "#806b63"
      }
    ]
  },
  {
    "featureType": "transit.line",
    "elementType": "geometry",
    "stylers": [
      {
        "color": "#dfd2ae"
      }
    ]
  },
  {
    "featureType": "transit.line",
    "elementType": "labels.text.fill",
    "stylers": [
      {
        "color": "#8f7d77"
      }
    ]
  },
  {
    "featureType": "transit.line",
    "elementType": "labels.text.stroke",
    "stylers": [
      {
        "color": "#ebe3cd"
      }
    ]
  },
  {
    "featureType": "transit.station",
    "elementType": "geometry",
    "stylers": [
      {
        "color": "#dfd2ae"
      }
    ]
  },
  {
    "featureType": "water",
    "elementType": "geometry.fill",
    "stylers": [
      {
        "color": "#b9d3c2"
      }
    ]
  },
  {
    "featureType": "water",
    "elementType": "labels.text.fill",
    "stylers": [
      {
        "color": "#92998d"
      }
    ]
  }
];

function initMap() {

  //Retrieve user locations with AJAX
  const map = new google.maps.Map(document.getElementById('map'), {
    zoom: 2,
    center: { lat: 39, lng: -98 },
    styles: styles,
  });

  $.get('/get_map_coords.json', (results) => {
    let  position, html2;
    let i = 1;

    for (let location in results) {
      window.setTimeout(() => {
        const infoWindow = new google.maps.InfoWindow({ maxWidth: 2000 });
        const marker = new google.maps.Marker({  
          position: new google.maps.LatLng(results[location].lat, results[location].lng), 
          map: map,  
          animation: google.maps.Animation.DROP,
          icon: "https://img.icons8.com/doodle/48/000000/marker.png"
        });

        // Populate url details based on what is retrieved with beautiful soup
        let url_display_text = results[location].url_title || results[location].url
        let source_display_text = results[location].url_site_name || results[location].url_head_title || results[location].url_author || results[location].url_twitter

        const html = ('<div class="window-content">' +
          `${results[location].url_img
            ?`<img src=${results[location].url_img} alt="" align="right" style="width:100px;margin: 0px 8px 20px 2px;" class="thumbnail">`
            : ''
          }` +
          `<h2><b>${results[location].business_name}</b></h2>
          ${results[location].formatted_address}
          <br>
          <br>
          <a href=${results[location].url}>${url_display_text}</a> - ${source_display_text}<br><br>`+
          `${results[location].recommended_by 
            ?`<b>Recommended by: </b>${results[location].recommended_by}<br><br>`
            : ''
          }` +
          `<small>(saved ${results[location].date_stamp})</small> 
          </div>`);
        bindInfoWindow(marker, map, infoWindow, html);
      }, i * 10);  
      i += 1;
    }
    attachAddLocationHandler(map);
  });
}

function bindInfoWindow(marker, map, infoWindow, html) {
  google.maps.event.addListener(marker, 'click', () => {
    infoWindow.close();
    infoWindow.setContent(html);
    infoWindow.open(map, marker);
  });
}
