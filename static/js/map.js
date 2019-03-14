"use strict";


// $.get('/get_latest_map_coords.json', (latest_results) => {

//       $("#map_form").submit(function(){
//     ;
//   })
//  });

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
                        // '<img src="/static/img/polarbear.jpg" alt="polarbear" style="width:150px;" class="thumbnail">' +
                        // '<h2><b>' + results[location].business_name+ '</b></h2>' +
                        '<p><a href=' + new_url + '>' + new_url + '</a></p>' +
                           `${new_recommended_by
                              ?`<p><b>Recommended by: </b>${new_recommended_by}</p>`
                               : ''
                          }` +
                        // '<p>' + results[location].formatted_address + '</p>' +
                        // '<p><i>(saved ' + results[location].date_stamp + ')</i></p>' +
                  '</div>');
      bindInfoWindow(marker, map, infoWindow, html);
      marker.setMap(map)
      map.setCenter({ lat, lng });
      map.setZoom(7);
       }
    });
  });
}



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
          //icon: "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAABHNCSVQICAgIfAhkiAAAAAlwSFlzAAABuwAAAbsBOuzj4gAAABl0RVh0U29mdHdhcmUAd3d3Lmlua3NjYXBlLm9yZ5vuPBoAAAFZSURBVEiJ7ZS/SsNQFIe/k6hQEV06NI6ODi4FF6Pg4NRYqBpcHLWCL9BX8Bmq+AIREVt0KShYXIqDi7Mu/TMJCk42x8FG25hUQQWH/rZ7fh/3u2e5MMgXkbiivpweFU2sg2yBmoh6mMOH1vHFXRyrsCnCg1WqOrGCVnZ+xvc1r8KGKBOhWoFaIDP89ngUa5Wr7/f2CJqOfaSQ06AQblGmAUQoqrICJMPGMNstMEJw7o2VE8OQHYFC0KVK1e1UwkoZypIIxY8Xfma7MxQ1FNE91Yi557WBClBpOHa+Hxu5wV9kIBgIBoJ+ApExlGxwbGTsQitjT32H7am6Dw3H1s70HHROVEYifoFrFA9hN5qVmlW+nA3gyL8IZRHEVzhTkaKBPCr+GsoqkEZIx7HWk1nut8ENkBQ48H1/f/L06r7H67pm87m+gCFuR/YSx/446rqmuq75q5f+y7wCHwCLEN3o+6gAAAAASUVORK5CYII="
          icon: "https://img.icons8.com/doodle/48/000000/marker.png"
          //<a href="https://icons8.com/icon/30567/map-pin">Map Pin icon by Icons8</a>
        });

        let url_display_text = results[location].url_title || results[location].url
        let source_display_text = results[location].url_site_name || results[location].url_head_title || results[location].url_author || results[location].url_twitter

        const html = ('<div class="window-content">' +
                        `${results[location].url_img
                              ?`<img src=${results[location].url_img} alt="" align="right" style="width:100px;margin: 0px 8px 20px 2px;" class="thumbnail">`
                               : ''
                          }` +
                        //'<img src="https://static01.nyt.com/images/2017/11/14/t-magazine/tmag-capferret-slide-KFLI/tmag-capferret-slide-KFLI-facebookJumbo.jpg" alt="polarbear" style="width:150px;" class="thumbnail">' +
                        `<h2><b>${results[location].business_name}</b></h2>
                        ${results[location].formatted_address}<br><br>` +
                        `<a href=${results[location].url}>${url_display_text}</a> - ${source_display_text}<br><br>`+
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
    // let lastLatLng = new google.maps.LatLng(results[results.length -1]["lat"], results[results.length -1]["lng"]);
    // $("#map_form").submit(function() {map.setCenter(lastLatLng)});
    attachAddLocationHandler(map);

  });

    // function changeCenter(lastLatLng,map) {
    //   $("#map_form").submit(function() {
    //   map.setCenter(lastLatLng)
    //   })
    // }

// google.maps.event.addListener(marker,'click',function() {
//   map.setZoom(9);
//   map.setCenter(marker.getPosition());
// });





//     $("#link1").click(function(){
//     changeMarkerPos(3.165759, 101.611416);
// });


 //make get request to new return from distance matrix
     // $.get('/calculate_trips', () => {
     // });
//      google.maps.event.addListenerOnce(map, 'idle', function(){
//     jQuery('.gm-style-iw').prev('div').remove();
// });
}

function bindInfoWindow(marker, map, infoWindow, html) {
  google.maps.event.addListener(marker, 'click', () => {
    infoWindow.close();
    infoWindow.setContent(html);
    infoWindow.open(map, marker);
    // map.setCenter(marker.getPosition());;
  });
}

    


 



