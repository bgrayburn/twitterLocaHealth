#step one - define query
$.stepOneBegin = ->
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
  $.stepTwoBegin(form_vals)
  false

#step two - query results
$.stepTwoBegin = (fv)->
  $('#query-results').show()
  twit_list = $("ul#tweets")
  twit_list.empty()
  $.tweets = getTweets(fv)
  wait_for_statuses = ()->
    if ($.tweets!=undefined)&&($.tweets.responseText!=undefined)
      rspTxt = JSON.parse($.tweets.responseText)
      statuses = rspTxt['statuses']
      $.statuses = statuses
      _.each(
        $.statuses,
        (t) -> twit_list.append(twitWidget(t['user'], t['text'], t['place'].toString(), t['id_str']))
      )
    else
      setTimeout(wait_for_statuses,100)
  wait_for_statuses()


getTweets = (fv)->
  tweet_req = "/tweets/"+_.collect(fv, (v)-> encodeURIComponent(v)).join('/')
  #$.get(tweet_req, {}, (d)-> tweets = tweets.concat([d]) )
  #console.log("i'm about to print your tweets")
  $.get(tweet_req, {}, (d)-> 
    #console.log()
    d
   )

$.getTweetTest = ()->getTweets(['ravens',39.3313.toString(),-76.613.toString()])  

twitWidget = (name='', tweet='', location='', tweet_id = '999999999999999999')->
  "<li>" + name + " - " + tweet + " - " + location + "<a href='https://twitter.com/intent/retweet?tweet_id="+tweet_id+"' ><img src='static/img/retweet.png'></a><a href='https://twitter.com/intent/tweet?in_reply_to="+tweet_id+"' ><img src='static/img/reply.png'></a></li>"

$.stepOneBegin()
$('#create-query').show()
$('#query-results').hide()