// Generated by CoffeeScript 1.8.0
(function() {
  var getTweets, twitWidget;

  $.stepOneBegin = function() {
    var success;
    success = function(position) {
      console.log("Latitude: " + position.coords.latitude + " Longitude: " + position.coords.longitude);
      $.position = [position.coords.latitude, position.coords.longitude];
      return $("input#query_location").val(_.each($.position, function(n) {
        return n.toString();
      }).join(","));
    };
    if (navigator.geolocation) {
      return navigator.geolocation.getCurrentPosition(success);
    } else {
      return console.log("geolocation not supported by this browser");
    }
  };

  $("#submit_query").click(function(e) {
    var form_vals;
    e.preventDefault();
    form_vals = _.collect($('input:text'), function(i) {
      return $(i).val();
    });
    form_vals[2] = form_vals[1].split(",")[1].slice(0, 7);
    form_vals[1] = form_vals[1].split(",")[0].slice(0, 7);
    $.stepTwoBegin(form_vals);
    return false;
  });

  $.stepTwoBegin = function(fv) {
    var twit_list, wait_for_statuses;
    $('#query-results').show();
    twit_list = $("table#tweets");
    twit_list.empty();
    $.tweets = getTweets(fv);
    wait_for_statuses = function() {
      var rspTxt, statuses;
      if (($.tweets !== void 0) && ($.tweets.responseText !== void 0)) {
        rspTxt = JSON.parse($.tweets.responseText);
        statuses = rspTxt['statuses'];
        $.statuses = statuses;
        return _.each($.statuses, function(t) {
          return twit_list.append(twitWidget(t['user']['name'], t['text'], t['user']['location'].toString(), t['id_str']));
        });
      } else {
        return setTimeout(wait_for_statuses, 100);
      }
    };
    return wait_for_statuses();
  };

  getTweets = function(fv) {
    var tweet_req;
    tweet_req = "/tweets/" + _.collect(fv, function(v) {
      return encodeURIComponent(v);
    }).join('/');
    return $.get(tweet_req, {}, function(d) {
      return d;
    });
  };

  $.getTweetTest = function() {
    return getTweets(['ravens', 39.3313.toString(), -76.613.toString()]);
  };

  twitWidget = function(name, tweet, location, tweet_id) {
    if (name == null) {
      name = '';
    }
    if (tweet == null) {
      tweet = '';
    }
    if (location == null) {
      location = '';
    }
    if (tweet_id == null) {
      tweet_id = '999999999999999999';
    }
    return "<tr style='outline: thin solid lightgray;'><td><strong>" + name + "</strong> " + tweet + " <i>" + location + "</i><a href='https://twitter.com/intent/retweet?tweet_id=" + tweet_id + "' ><img src='static/img/retweet.png'></a><a href='https://twitter.com/intent/tweet?in_reply_to=" + tweet_id + "' ><img src='static/img/reply.png'></a></td></tr>";
  };

  $.stepOneBegin();

  $('#create-query').show();

  $('#query-results').hide();

}).call(this);
