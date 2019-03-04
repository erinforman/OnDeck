'use strict';


function getItinerary(evt){
  evt.preventDefault();

  const form = $(evt.target);
  const formValues = {
    origin_place_id: $('select[name="origin_place_id"]').val(),
    hours: $('input[name="hours"]').val(),
    days: $('input[name="days"]').val()
  };
  $.get('/itinerary.json', formValues, showResults);

}
// //results = itinerary details
// function showResults(results) {

//     console.log(results[1][0])

//     $('#itinerary').html(results);

// }








// function showResults(results) {

//   for (let i = 0; i < results[1].length; i+=1) {
//     console.log(results[1][i])
//     console.log(results[1][i][4])
//     // console.log(location)
//     let origin = results[1][i][4]
//     let origin_url = results[1][i][3]
//     let destination = results[1][i][7]
//     let destination_url = results[1][i][6]

//     let trip = origin + ' ' + origin_url


//     $('#itinerary').html(trip);
//   }

//     //console.log(results[1][0])

    

//}

function secondsToDhm(seconds) {
seconds = Number(seconds);
var d = Math.floor(seconds / (3600*24));
var h = Math.floor(seconds % (3600*24) / 3600);
var m = Math.floor(seconds % 3600 / 60);

var dDisplay = d > 0 ? d + ("d ") : "";
var hDisplay = h > 0 ? h + ("h ") : "";
var mDisplay = m > 0 ? m + ("m ") : "";
return dDisplay + hDisplay + mDisplay;
}


function showResults(results) {


  $('#itinerary_duration').html('Itinerary length: ' + secondsToDhm(results[4])+ '<br>'+((results[4]/results[2])*100).toFixed(1) + '% of available time used')
  $('#itinerary_time_left').html(secondsToDhm(results[3]) + ' time left')

$.each( results[1], function( i,l ){

  console.log(results)

  // $('#itinerary_origin_' + i).append('Origin: ' + l[4]);
  // $('#itinerary_origin_url_' + i).append(l[3]);
  $('#itinerary_origin_urlhyper_' + i).append('Leg ' + Number(i+1)+': ' + '<a href="'+l[3]+'">'+l[4]+'</a>  >> ');
  $('#itinerary_destination_urlhyper_' + i).append('<a href="'+l[6]+'">'+l[7]+'</a>');
  $('#itinerary_duration_' + i).append(secondsToDhm(l[1]));
  // $('#itinerary_destination_' + i).append('Destination: ' + l[7]);
  // $('#itinerary_destination_url_' + i).append(l[6]);
});

}

// Alternate
// function showResults(results){
//     for (let result in results) {
//       $('#' + result).html(results[result]);
//     }
// }

$("#itinerary_form").on("submit", getItinerary);
