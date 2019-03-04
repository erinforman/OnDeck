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

  $('#email_itinerary').html('<button id="email_itinerary_btn">Email Itinerary</button>')
  $('#itinerary_duration').html('Itinerary length: ' + secondsToDhm(results[4])+ '<br>'+((results[4]/results[2])*100).toFixed(1) + '% of available time used')
  $('#itinerary_time_left').html(secondsToDhm(results[3]) + ' time left')
  // $('#content').val(results[1])

$.each( results[1], function( i,l ){

  // $('#itinerary_origin_' + i).append('Origin: ' + l[4]);
  // $('#itinerary_origin_url_' + i).append(l[3]);
  $('#itinerary_origin_urlhyper_' + i).append('Leg ' + Number(i+1)+': ' + '<a href="'+l[3]+'">'+l[4]+'</a>  >> ');
  $('#itinerary_destination_urlhyper_' + i).append('<a href="'+l[6]+'">'+l[7]+'</a>');
  $('#itinerary_duration_' + i).append(secondsToDhm(l[1]));
  // $('#itinerary_destination_' + i).append('Destination: ' + l[7]);
  // $('#itinerary_destination_url_' + i).append(l[6]);
});

}


$("#itinerary_form").on("submit", getItinerary);


// function emailItinerary() {

// // Get the modal
// var modal = document.getElementById('myModal');

// // Get the button that opens the modal
// // var btn = document.getElementById("email_itinerary");

// // Get the <span> element that closes the modal
// var span = document.getElementsByClassName("close")[0];

// // When the user clicks the button, open the modal 

// modal.style.display = "block";

// // When the user clicks on <span> (x), close the modal
// span.onclick = function() {
//   modal.style.display = "none";
// }



// }


// $("#email_itinerary").on("click", emailItinerary)


$("#email_itinerary").click(function () {
  $("#myModal").css("display", "block");
});

$(".close").click(function () {
  $("#myModal").css("display", "none");
});