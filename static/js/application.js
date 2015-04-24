// Generated by CoffeeScript 1.8.0
(function() {
  var getTweets, twitWidget;

  $.step_one_begin = function() {
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
    var form_vals, tweet_req;
    e.preventDefault();
    form_vals = _.collect($('input:text'), function(i) {
      return $(i).val();
    });
    form_vals[2] = form_vals[1].split(",")[1].slice(0, 7);
    form_vals[1] = form_vals[1].split(",")[0].slice(0, 7);
    tweet_req = "/tweets/" + _.collect(form_vals, function(v) {
      return encodeURIComponent(v);
    }).join("/");
    $.tweets = [];
    $.get(tweet_req, {}, function(d) {
      return $.tweets = $.tweets.concat([d]);
    });
    $.step_two_begin();
    return false;
  });

  $.step_two_begin = function() {
    var twit_list;
    $('#query-results').show();
    twit_list = $("ul#tweets");
    twit_list.empty();
    return _.each(getTweets("test"), function(t) {
      return twit_list.append(twitWidget());
    });
  };

  getTweets = function(q) {
    return [1];
  };

  twitWidget = function() {
    return "<li>Bob - Stuff - <a href='#'>retweet</a> - <a href='#'> reply</a></li>";
  };

  $.step_one_begin();

  $('#create-query').show();

  $('#query-results').hide();

}).call(this);
