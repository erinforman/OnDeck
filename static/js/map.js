"use strict";

function initMap() {

  let myCenter = { lat: 37.601773, lng: -122.202870 };
  //TODO: CHANGE CENTER DYNAMICALLY DEPENDING ON USER

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

      let  position, html
      let i = 1
  
      for (let location in results) {

          //Add pin animation and drop delay
          window.setTimeout(function() {  
            

              let marker = new google.maps.Marker({  
                  position: new google.maps.LatLng(results[location].lat, results[location].lng), 
                  map: map,  
                  animation: google.maps.Animation.DROP,
                  icon: 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACgAAAAoCAYAAACM/rhtAAAABHNCSVQICAgIfAhkiAAAAAlwSFlzAAACeQAAAnkBrK5NVQAAABl0RVh0U29mdHdhcmUAd3d3Lmlua3NjYXBlLm9yZ5vuPBoAAAGdSURBVFiF7Zi9SgNBFEbP3TUSxErwZ8VCX8PgAyg2NkoUBBVLQUHxIRQULFNYSbQQG5M8QNBCgvgEVkIUsZIEMclcCxsJiJuZJaDO6RbufN9hYGZgBUce5yaHaAQbBlkQNAJQpIpwKk2OolL52SVfXBY/zWaWDJIDEVTTbWlvgBF0deTy6qzrgtWZzDyBHAN9P4zW1Zjl0eL1uU2PlWB1emqQUO+B/pglr83U+8TYxc1Lp11Bx3aAhGyh9MSdN0qqp9G7adNlJahqskA67rwIaVSzNl2xd6GtMep0iREZs6my2sFuYieoWu24SPXBpsrukEiQ5/Oei7viDZG8TZfdIWlxgNCMOy9oo5l6P7TpshKMSuVnWroG1GOM140xKzZ3IPyCp87pFA9fXp1IyowLul8LBzCEGEJqwQAqskdLxl3kwHEHv5LLFvXr93p+JpHsP3oPdhEv6IoXdMULuuIFXfGCrnhBV7ygK17QFS/oyr8SvBNQQBFukwpNTFAl2FGogdSUYDep3ETJLRYqucVCJclMux+Y32GC7UTzgA+szH+ow1LTpgAAAABJRU5ErkJggg=='
                  //<a href="https://icons8.com/icon/30567/map-pin">Map Pin icon by Icons8</a>
                  });  
          
              html = ('<div class="window-content">' +
                            '<img src="/static/img/polarbear.jpg" alt="polarbear" style="width:150px;" class="thumbnail">' +
                            '<p><b>Name: </b>' + '**Put the name here**'+ '</p>' +
                            '<p><b>URL: </b>' + results[location].url + '</p>' +
                            //TODO: ADD IF EXISTS FOR RECOMMENDED BY
                            '<p><b>Recommended by: </b>' + results[location].recommended_by + '</p>' +
                            '<p><b>Address: </b>' + results[location].formatted_address + '</p>' +
                            '<p><b>Saved: </b>' + results[location].date_stamp + '</p>' +
                      '</div>');

              bindInfoWindow(marker, map, infoWindow, html);
        
        }, i * 200);  

      i+=2
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





    


 



