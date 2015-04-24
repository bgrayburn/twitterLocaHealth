import os
import random
import string
from tornado.ioloop import IOLoop
from tornado.web import RequestHandler, Application, url
from tornado.gen import coroutine
from tornado.auth import TwitterMixin
import tornado

class IndexHandler(RequestHandler):
    @tornado.web.authenticated
    @tornado.gen.coroutine
    def get(self):
        #self.render("index.html", user = self.current_user, tweets=[])
        print(self.current_user.toString())
        self.render("index.html", user = self.current_user, tweets=[])
        #use put to send location back to server

class TwitterLoginHandler(RequestHandler, TwitterMixin):
    @tornado.gen.coroutine
    def get(self):
        if self.get_argument('oauth_token', None):
            print('need to get authenticated user')
            self.get_authenticated_user(self._on_auth)
            #user = yield self.get_authenticated_user()
            # Save the user using e.g. set_secure_cookie()
        print('redirecting for oauth')
        self.authenticate_redirect()
        return

    def _on_auth(self, user):
        print("auth callback time")
        if not user:
            raise tornado.web.HTTPError(500, "Twitter auth failed")
        self.set_secure_cookie("user", tornado.escape.json_encode(user))
        self.redirect("/")

class TweetHandler(RequestHandler,TwitterMixin):
    @tornado.gen.coroutine
    @tornado.web.authenticated
    def get(self, topic='', location='0,0'):
        print(topic)
        print(location)
        response = yield self.twitter_request(
            "/search/tweets",
             access_token=self.get_secure_cookie("user")["access_token"]
             )

def make_app():
    return Application([
        url(r"/", IndexHandler),
        #url(r"/login[?]?[A-Za-z0-9=%.]*",TwitterLoginHandler),
        url(r"/login",TwitterLoginHandler),
        url(r"/tweets/[a-zA-Z0-9.%-]+/[a-zA-Z0-9.,%-]+/?",TweetHandler)
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