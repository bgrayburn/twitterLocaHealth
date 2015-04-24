import os
import random
import string
from tornado.ioloop import IOLoop
from tornado.web import RequestHandler, Application, url
from tornado.gen import coroutine
from tornado.auth import TwitterMixin
import tornado
import time
import urlparse

class BaseHandler(RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("user")

class IndexHandler(BaseHandler):
    @tornado.gen.coroutine
    def get(self):
        #print(self.current_user.toString())
        if self.get_secure_cookie("access_token", None):
            self.render("index.html",
                name=self.get_secure_cookie("name",None).split(' ')[0][1:],
                tweets=[])
        else:
            self.redirect("/login")
        #use put to send location back to server

class TwitterLoginHandler(BaseHandler, TwitterMixin):
    @tornado.gen.coroutine
    def get(self):
        if self.get_argument('oauth_token', None):
            print('need to get authenticated user')
            #self.get_authenticated_user(self._on_auth)
            yield self.get_authenticated_user(self._auth_callback)
            # Save the user using e.g. set_secure_cookie()
        else:
            yield self.authenticate_redirect(callback_uri="/login")
        return

    def _auth_callback(self,user):
        print("hello " + user['name'])
        if not user:
            raise tornado.web.HTTPError(500, "Twitter auth failed")
        #self.set_secure_cookie("user", str(tornado.escape.json_encode(user)))
        self.set_secure_cookie("name", tornado.escape.json_encode(user['name']))
        self.set_secure_cookie("access_token", str(user['access_token']))
        print("access_token: " + str(self.get_secure_cookie("access_token", None)))
        print("sending you to the main page")
        self.redirect("/")
        return


class TweetHandler(BaseHandler,TwitterMixin):
    @tornado.gen.coroutine
    def get(self, topic='', lat="0.", lng="0."):
        if self.get_secure_cookie("access_token", None):
            print("topic:"+topic)
            twit_req = "/search/tweets?q="+topic+",geocode="+str(lat)+','+str(lng) + ',5mi'
            print(twit_req)
            yield self.twitter_request(
                 twit_req,
                 access_token=self.get_secure_cookie("access_token", None)
                 )
        else:
            yield self.redirect("/login")

def make_app():
    return Application([
        url(r"/", IndexHandler),
        url(r"/login[?]?[A-Za-z0-9=%_.]*",TwitterLoginHandler),
        #url(r"/login",TwitterLoginHandler),
        url(r"/tweets/([a-zA-Z0-9.%-]+)/([0-9.,%-]+)/([0-9.,%-]+)/?",TweetHandler)
        ],
        twitter_consumer_key = "DWndiNB6JG1JaXHh82B1AgdFC",
        twitter_consumer_secret = "Icf8a4KMfcI6F9rOu4aqdYzsikpVBmBhlBTuNaHJJPJirNw3Za",
        login_url = "/login",
        cookie_secret = (lambda: ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10)))(),
        static_path = os.path.join(os.path.dirname(__file__), "static")
        )

def main():
    app = make_app()
    app.listen(80)
    IOLoop.current().start()


if __name__ == '__main__':
    main()