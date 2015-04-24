#step one - define query
$.step_one_begin = ->
  #geolocate
  success = (position)->
    console.log("Latitude: " + position.coords.latitude + " Longitude: " + position.coords.longitude)
    $.position=[position.coords.latitude, position.coords.longitude]
    $("input#query_location").val(_.each($.position, (n)-> n.toString()).join(","))
  if (navigator.geolocation)
    navigator.geolocation.getCurrentPosition(success)
  else
    console.log("geolocation not supported by this browser")
      
$("#submit_query").click (e)->
  e.preventDefault()
  console.log("")
  form_vals = _.collect($('input:text'), (i)-> $(i).val())
  $.get("/tweets/"+_.collect(form_vals, (v)-> encodeURIComponent(v)).join("/"))
  $.step_two_begin()
  false

#step two - query results
$.step_two_begin = ->
  $('#query-results').show()
  twit_list = $("ul#tweets")
  twit_list.empty()
  _.each(getTweets("test"), (t) -> twit_list.append(twitWidget()))

getTweets = (q)->
  [1]

twitWidget = ()->
  "<li>Bob - Stuff</li>"

$.step_one_begin()
$('#create-query').show()
$('#query-results').hide()