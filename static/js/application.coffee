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
  form_vals = _.collect($('input:text'), (i)-> $(i).val())
  form_vals[2] = form_vals[1].split(",")[1].slice(0,7)
  form_vals[1] = form_vals[1].split(",")[0].slice(0,7)
  tweet_req = "/tweets/"+_.collect(form_vals, (v)-> encodeURIComponent(v)).join("/")
  $.tweets = []
  $.get(tweet_req, {}, (d)-> $.tweets = $.tweets.concat([d]) )
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
  "<li>Bob - Stuff - <a href='#'>retweet</a> - <a href='#'> reply</a></li>"

$.step_one_begin()
$('#create-query').show()
$('#query-results').hide()