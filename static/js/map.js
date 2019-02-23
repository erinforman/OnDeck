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

      let  position, html, html2
      let i = 1
  
      for (let location in results) {

          //Add pin animation and drop delay
          window.setTimeout(function() {  
            

              let marker = new google.maps.Marker({  
                  position: new google.maps.LatLng(results[location].lat, results[location].lng), 
                  map: map,  
                  animation: google.maps.Animation.DROP,
                  icon: 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAB4AAAAeCAYAAAA7MK6iAAAABHNCSVQICAgIfAhkiAAAAAlwSFlzAAAB2wAAAdsBV+WHHwAAABl0RVh0U29mdHdhcmUAd3d3Lmlua3NjYXBlLm9yZ5vuPBoAAAKuSURBVEiJ7ZZdSBRRFMf/586uq60fWUbqVvb9ENiTEOqu+lDgrmsgERQ9BhUVRREJhRRB0EPQQ9FT0UsQUVixWxIESk5GqBD4UCGSteaukVp+rB+7c08vamvujuPO4pN/GGY4c875zb137rkHWJFBhTwVxSFPRXGy8ZakyUJem3mqMw0OeEsdaazYdHlRmlj3ujXIZj56FswAhbyuuwCfkKQfIK2MscbHN8NNzzZpwb7vSYMZoND+ituQfDzr6GlYN2/TjxAC1l3FF6a7OmEKHKp1NUDyyZwz9ZSxrybZPEuWYGAUYJLjY8sGBQBLoa/1VsjrXDN6/85lOTxISsEG3QCy2ZBeXmUeDAD5frWh3+tSxhsf1QMQ+mTISKD3fKTnyyEz4EX+4cQKel3dAG834PqTGZ7Cl2pnrFF/dPr6YdAvTxCa+z3lJSkC86hBR8GAXQhq7vM4d6YAvBQxAKQriswxDWYg3aCrJIIGQl2Br63dNJiAHcYcOcpS1OX7VH+sOWGh73a7bVnW8AOA55UzFmJqVe3Bc5NvXgW0kT+fI8BhPa7IkJMbn7yb+N8eF9ztdtsyLeONUJRq+4Ejgmwxs6oIZOyteaj1fYNsb/MX+dVhPXAixQVnWsNPSVD16kvXha2kNJm8i2rBGnNVlQWE3SI3jy1bjNSHFIGppSUKokpt6Fdw6OKpyFTHe0x/7Ph3feoCpDQNTlgy+z1lRZSWpiIaXXBqZB87ey/c9KI8GujtKfCrtSkFA8Cge0/2lLDO2zaSpeawO7pCE8HnAJAsWLdvWtv0YQRAZ7x3Qa8zGd6clqlkroANNgIDNc6tknAVNO9gmF1kdc7CmCQSV/J9b78OeMtKmURlvk+9ES+noaacWdiJeL1kjp2h3zP33JhRaJBROwBohCxiciTK+ReCDuoEmNtNsAAAAABJRU5ErkJggg=='
                  //<a href="https://icons8.com/icon/30567/map-pin">Map Pin icon by Icons8</a>
                  });  
          
              html = ('<div class="window-content">' +
                            '<img src="/static/img/polarbear.jpg" alt="polarbear" style="width:150px;" class="thumbnail">' +
                            '<p><b>Name: </b>' + results[location].business_name+ '</p>' +
                            '<p><b>URL: </b><a href=' + results[location].url + '>' + results[location].url + '</a></p>' +
                            // <a href="https://www.w3schools.com/html/">Visit our HTML tutorial</a>
                            //TODO: ADD IF EXISTS FOR RECOMMENDED BY
                            `${results[location].recommended_by 
                                  ?`<p><b>Recommended by: </b>${results[location].recommended_by}</p>`
                                   : ''
                              }` +
                            '<p><b>Address: </b>' + results[location].formatted_address + '</p>' +
                            '<p><i><b>Saved: </b>' + results[location].date_stamp + '</i></p>' +
                      '</div>');
              bindInfoWindow(marker, map, infoWindow, html);
        
        }, i * 50);  

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





    


 



