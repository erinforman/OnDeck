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
  // $("#itinerary_time_left").empty();
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

  $('#email_itinerary').html('<button id="email_itinerary_btn" class="btn btn-secondary">Email Itinerary</button>')
  $('#itinerary_duration').html(`<center>Itinerary duration: <strong>${secondsToDhm(results[4])}</strong><img src="https://img.icons8.com/material-sharp/50/000000/sort-down.png"><strong>${secondsToDhm(results[3])}</strong> of free time<img src="https://img.icons8.com/material-sharp/50/000000/sort-down.png"><strong>${((results[4]/results[2])*100).toFixed(1)}%</strong> of available time planned</strong></center>`)
  // $('#itinerary_time_left').html(secondsToDhm(results[3]) + ' time left')

 $("#legs").empty();
//Origin
 $('#legs').append(`
    <h5><strong>Start    </strong></h5>
    ${results[1][0][4]
        ?`<img id = "profile_img_0" src=${results[1][0][4]} alt="" class="profile_img">`
                               : ''
                          }
    <div id=itinerary_destination_business_name_0 style= 'display: inline-block; padding: 5px;'></div>${results[1][0][10]}: ${results[1][0][11]}
    <div id=itinerary_destination_urlhyper_0 style= 'display: inline-block; padding: 5px;'></div><a href= '${results[1][0][3]}'>${url_display_text} </a> - ${source_display_text}<br>
    <div align="center"><div id=itinerary_duration_0 style= 'display: inline-block; padding: 5px;'></div> ${secondsToDhm(results[1][0][1])}</div>
    <div align="center"><div align="center"><div id=itinerary_arrow_0 style= 'display: inline-block; padding: 5px;'></div><img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAFAAAABQCAYAAACOEfKtAAAABHNCSVQICAgIfAhkiAAAAAlwSFlzAAAFxAAABcQBm3m1AAAAABl0RVh0U29mdHdhcmUAd3d3Lmlua3NjYXBlLm9yZ5vuPBoAAAUUSURBVHic7ZpPbxtFGMafGa/tWEUlVYQIGCHKH4GaQ2jEoUojoZAIkUhRw6EpRUJNGoL6MXrph+hX6CUQVxZFOAaELKi2TUGol0gIIVrEobJaqRDHzgwH/4nXXq9nd9/ZtZv5nRJn592ZJ+87+876AQwGg8FgMBgMBoPBYDhaMB1Bcz9vTwqGezpiB0aIyXNn5n+lDsupAwKA4OyKjrih4FzLnMgz8EaplElbew8BjIaJ88rYi5h6/RQA4O7v9/HXo3/CTYyhXKmOZFemp/8LF8gJeQaOWJULCCkeAFgJy/XnwEicSCcqK+EDOSEXUEJ+ThHHSiRcfw4HzdzaIRVw6/b2BICzkOFjWbwtAzmRgAwzX/707SmaYHVIBZQMlwGQ7KzODCQo4QYswdfJgoFQwPxuPg2JS1Tx9JQwAIlL+d18miocmYD75cwygDGqeI6HCFUJ1xmrlUfOUQUjE5ARb9DtolGWMABIMLK5kgj41Z3imwDmKGI10VbCAAA5v2kX3qCIRCIgE2IVxE15kroPdMK44KskgcIGuG7byXHx5E8A4wTziZK/jz9lr87OztbCBAmdgePyyQKGTzwAeOnxMbEQNkhoAZmk25CjhhE8TEKVcK5UyAqL/QEJS8+LMY1IAAw1XpOvLU3PPQgaJtTuLCysAfTipawkPjo94/js650fsV+r0t2kPmfrIMFXAVwLGiZwCV+VVznALgcd74Vb20LfytRhTK7X1xKMwANP2zNzAE4GHe+FW9tCfBpp5+S79vsfBB0c/CEiubaHh5tYGnrBFlwGP0UFEjB/94cXACwHvWk/XDNQUwkDgAQ+bqzJN4EErFZrnwFIBRmrgvseqC8DAaQaa/KNbwGllAwMXwS5mSquAurbA+swbEgpffcTvgW8eee7swDe9jvOD+1vo1ufaSzhBu9s2cVpv4N8CygE/fcKncRQwgAAGeBh4kvAzZ3iKIAViu88vIilhCXAwC401qiMLwF5VVwEkNF9bHNvY7TvgQCQ4fviEz/DfJZwNC8O3NsYzSXcrCrGNvwMUxYwZxemAExprl4A0R7lWrCWhlONtSqhLKCQfKNxH+1EfJRr0VybEOqVpqTHrV9uHdurJB8COB5kYkPIY86fvrz03tK//S5UysBKJXUeR0c8AHheHDx3XuVCJQGp/C7Dhdqa+5bw1u3tCQn81niDe6SQQkwsn5m/73VN3wyk9LsMGyo+Gk9Z8rv5dLU88gCElo0h41HyxF528a3FSq8LPLvT/XJmmUFGKt5IKo0PJ93P9N/cK2Gv2nMtOmj6aG70usCzhKn9Lip49XsRvJHpop+PpqeAOvwuKngd2eIQsJ+PpqeAOvwuKniJFMUrLRc8fTSuAl637aSUjNTJqYpnCUdwnHNHrheLRdf/nquAcfpdvDMwLgF7+2hcBYzT7+K9B8ZSwgB6+2i6BMyVClkJuaD7rXMvPDMwrhKua7GYKxWynX/qElCX30WVQWtjAHT6aBw4BNTpd1Fl8NqYQ9x8NI5fdPpdVBnANqadLh+Ns4Q1+l1U8czA2NqYQzp9NC0BdftdVPHeA2PPwC4fTUtA3X4XVQa0D2zH4aPhQDR+F1UGvYQBOHw0HIjG76LKoJdwg5aPhgOAOJBr8c7nkCEo4SZrAMA3d4qjYLgY18mjk6EQUAKQ+HRzpzhq1f0uTLvfRZWb9vdxT6E/bT4aHpXf5ZnEp4/GYDAYDAaDwWAwGAyGZ4H/AV/bQw38/hixAAAAAElFTkSuQmCC"></div><br>

    </div>
  `);
//Trips
  $.each( results[1].slice(1), function( i,l ){

  url_display_text = l[5] || l[3]
  source_display_text = l[8] || l[6] || l[7] || l[9]

  $('#legs').append(`
    <h5><div class="numberCircle" style='display: inline-block;'><strong>${i+1}</strong></div></h5>
    ${l[4]
        ?`<img id="profile_img_${i}" src=${l[4]} alt="" class="profile_img" style='display: inline-block;'>`
                               : ''
                          }
    <div class="business_name" id="itinerary_destination_business_name_${i}" style='display: inline-block; padding-left: 5px;'></div>${l[10]}: ${l[11]}
    <div id=itinerary_destination_urlhyper_${i} style= 'display: inline-block; padding: 5px;'></div><a href= '${l[3]}'>${url_display_text} </a> - ${source_display_text}<br>
    
    <div align="center"><div id=itinerary_duration_${i} style='display: inline-block;'></div>${secondsToDhm(l[1])}</div>
    <div align="center"><div id=itinerary_arrow_${i} style='display: inline-block;'></div><img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAFAAAABQCAYAAACOEfKtAAAABHNCSVQICAgIfAhkiAAAAAlwSFlzAAAFxAAABcQBm3m1AAAAABl0RVh0U29mdHdhcmUAd3d3Lmlua3NjYXBlLm9yZ5vuPBoAAAUUSURBVHic7ZpPbxtFGMafGa/tWEUlVYQIGCHKH4GaQ2jEoUojoZAIkUhRw6EpRUJNGoL6MXrph+hX6CUQVxZFOAaELKi2TUGol0gIIVrEobJaqRDHzgwH/4nXXq9nd9/ZtZv5nRJn592ZJ+87+876AQwGg8FgMBgMBoPBYDhaMB1Bcz9vTwqGezpiB0aIyXNn5n+lDsupAwKA4OyKjrih4FzLnMgz8EaplElbew8BjIaJ88rYi5h6/RQA4O7v9/HXo3/CTYyhXKmOZFemp/8LF8gJeQaOWJULCCkeAFgJy/XnwEicSCcqK+EDOSEXUEJ+ThHHSiRcfw4HzdzaIRVw6/b2BICzkOFjWbwtAzmRgAwzX/707SmaYHVIBZQMlwGQ7KzODCQo4QYswdfJgoFQwPxuPg2JS1Tx9JQwAIlL+d18miocmYD75cwygDGqeI6HCFUJ1xmrlUfOUQUjE5ARb9DtolGWMABIMLK5kgj41Z3imwDmKGI10VbCAAA5v2kX3qCIRCIgE2IVxE15kroPdMK44KskgcIGuG7byXHx5E8A4wTziZK/jz9lr87OztbCBAmdgePyyQKGTzwAeOnxMbEQNkhoAZmk25CjhhE8TEKVcK5UyAqL/QEJS8+LMY1IAAw1XpOvLU3PPQgaJtTuLCysAfTipawkPjo94/js650fsV+r0t2kPmfrIMFXAVwLGiZwCV+VVznALgcd74Vb20LfytRhTK7X1xKMwANP2zNzAE4GHe+FW9tCfBpp5+S79vsfBB0c/CEiubaHh5tYGnrBFlwGP0UFEjB/94cXACwHvWk/XDNQUwkDgAQ+bqzJN4EErFZrnwFIBRmrgvseqC8DAaQaa/KNbwGllAwMXwS5mSquAurbA+swbEgpffcTvgW8eee7swDe9jvOD+1vo1ufaSzhBu9s2cVpv4N8CygE/fcKncRQwgAAGeBh4kvAzZ3iKIAViu88vIilhCXAwC401qiMLwF5VVwEkNF9bHNvY7TvgQCQ4fviEz/DfJZwNC8O3NsYzSXcrCrGNvwMUxYwZxemAExprl4A0R7lWrCWhlONtSqhLKCQfKNxH+1EfJRr0VybEOqVpqTHrV9uHdurJB8COB5kYkPIY86fvrz03tK//S5UysBKJXUeR0c8AHheHDx3XuVCJQGp/C7Dhdqa+5bw1u3tCQn81niDe6SQQkwsn5m/73VN3wyk9LsMGyo+Gk9Z8rv5dLU88gCElo0h41HyxF528a3FSq8LPLvT/XJmmUFGKt5IKo0PJ93P9N/cK2Gv2nMtOmj6aG70usCzhKn9Lip49XsRvJHpop+PpqeAOvwuKngd2eIQsJ+PpqeAOvwuKniJFMUrLRc8fTSuAl637aSUjNTJqYpnCUdwnHNHrheLRdf/nquAcfpdvDMwLgF7+2hcBYzT7+K9B8ZSwgB6+2i6BMyVClkJuaD7rXMvPDMwrhKua7GYKxWynX/qElCX30WVQWtjAHT6aBw4BNTpd1Fl8NqYQ9x8NI5fdPpdVBnANqadLh+Ns4Q1+l1U8czA2NqYQzp9NC0BdftdVPHeA2PPwC4fTUtA3X4XVQa0D2zH4aPhQDR+F1UGvYQBOHw0HIjG76LKoJdwg5aPhgOAOJBr8c7nkCEo4SZrAMA3d4qjYLgY18mjk6EQUAKQ+HRzpzhq1f0uTLvfRZWb9vdxT6E/bT4aHpXf5ZnEp4/GYDAYDAaDwWAwGAyGZ4H/AV/bQw38/hixAAAAAElFTkSuQmCC"></div><br>
  `);
  $('#itinerary').append('Origin: ' + results[4]);
});
//Final Destination
  url_display_text = results[1][results[1].length-1][15] || results[1][results[1].length-1][13]
  source_display_text = results[1][results[1].length-1][18] || results[1][results[1].length-1][16] || results[1][results[1].length-1][17] || results[1][results[1].length-1][19]
 
  $('#legs').append(`
    <h5><strong>End</strong></h5>
    ${results[1][results[1].length-1][14]
        ?`<img id = "profile_img_${results[1].length-1}" src=${results[1][results[1].length-1][14]} alt="" class="profile_img" style='display: inline-block;'>`
                               : ''
                          }
    
    <div id=itinerary_destination_business_name_${results[1].length-1} style= 'display: inline-block; padding: 5px;'></div>${results[1][results[1].length-1][20]}: ${results[1][results[1].length-1][21]}
    <div id=itinerary_destination_urlhyper_${results[1].length-1} style= 'display: inline-block; padding: 5px;'></div><a href= '${results[1][results[1].length-1][13]}'>${url_display_text} </a> - ${source_display_text}<br>
  <br>
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


