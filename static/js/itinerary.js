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

  $("#email_itinerary").empty();
  $("#itinerary_duration").empty();
  $("#itinerary_time_left").empty();
  $("#itinerary_alert").empty();
  $("#legs").empty();

  if (results[0] === 'need_more_time' || results[3] === 0) {
    $('#itinerary_alert').html(`<div class="alert alert-primary ">
      <strong>Extend</strong> your trip by <strong>${secondsToDhm(results[1][1]-results[2])}</strong> 
      to get to <strong>${results[1][20]} </div>
      `);
    }

  else if (results[0] === 'no_trips') {

    $('#itinerary_alert').html(`<div class="alert alert-warning ">
      <strong>Yikes</strong> You cannot drive from this origin to any of your saved locations. Save more locations 
      or select a different origin.</div>
    `);

  }

  else {

  let url_display_text = results[1][0][5] || results[1][0][3]
  let source_display_text = results[1][0][8] || results[1][0][6] || results[1][0][7] || results[1][0][9]


  $('#itinerary').html('');

  $('#email_itinerary').html('<button id="email_itinerary_btn">Email Itinerary</button>')
  $('#itinerary_duration').html('Itinerary length: ' + secondsToDhm(results[4])+ '<br>'+((results[4]/results[2])*100).toFixed(1) + '% of available time used')
  $('#itinerary_time_left').html(secondsToDhm(results[3]) + ' time left')

 $("#legs").empty();
//Origin
 $('#legs').append(`
    <strong>Origin) </strong><div id=itinerary_destination_business_name_0 style= 'display: inline-block; padding: 5px;'></div>${results[1][0][10]}: ${results[1][0][11]}<br>
    <div id=itinerary_destination_urlhyper_0 style= 'display: inline-block; padding: 5px;'></div><a href= '${results[1][0][3]}'>${url_display_text} </a> - ${source_display_text}<br>
    ${results[1][0][4]
        ?`<img id = "profile_img" src=${results[1][0][4]} alt="" class="thumbnail"><br>`
                               : ''
                          }

    <div id=itinerary_duration_0 style= 'display: inline-block; padding: 5px;'></div> ${secondsToDhm(results[1][0][1])}<br>
  `);
//Trips
  $.each( results[1].slice(1), function( i,l ){

  url_display_text = l[5] || l[3]
  source_display_text = l[8] || l[6] || l[7] || l[9]

  $('#legs').append(`
    <strong>${i+1})</strong>: <div id=itinerary_destination_business_name_${i} style= 'display: inline-block; padding: 5px;'></div>${l[10]}: ${l[11]}<br>
    <div id=itinerary_destination_urlhyper_${i} style= 'display: inline-block; padding: 5px;'></div><a href= '${l[3]}'>${url_display_text} </a> - ${source_display_text}<br>
    ${l[4]
        ?`<img id = "profile_img" src=${l[4]} alt="" class="thumbnail"><br>`
                               : ''
                          }
    <div id=itinerary_duration_${i} style= 'display: inline-block; padding: 5px;'></div> ${secondsToDhm(l[1])}<br>
  `);
  $('#itinerary').append('Origin: ' + results[4]);
});
//Final Destination
console.log(results)
console.log(results[1])
console.log(results[1].length)

url_display_text = results[1][results[1].length-1][15] || results[1][results[1].length-1][13]
source_display_text = results[1][results[1].length-1][18] || results[1][results[1].length-1][16] || results[1][results[1].length-1][17] || results[1][results[1].length-1][19]
  $('#legs').append(`
    <strong>Final Destination) </strong>: <div id=itinerary_destination_business_name_${results[1].length-1} style= 'display: inline-block; padding: 5px;'></div>${results[1][results[1].length-1][20]}: ${results[1][results[1].length-1][21]}<br>
    <div id=itinerary_destination_urlhyper_${results[1].length-1} style= 'display: inline-block; padding: 5px;'></div><a href= '${results[1][results[1].length-1][13]}'>${url_display_text} </a> - ${source_display_text}<br>
    ${results[1][results[1].length-1][14]
        ?`<img id = "profile_img" src=${results[1][results[1].length-1][14]} alt="" class="thumbnail"><br>`
                               : ''
                          }

  `);

}

}


$("#itinerary_form").on("submit", getItinerary);




$("#email_itinerary").click(function () {
  $("#myModal").css("display", "block");
});

$(".close").click(function () {
  $("#myModal").css("display", "none");
});