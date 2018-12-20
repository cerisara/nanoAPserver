# Apache settings

This server creates a Flask (python) mini server that listens on http://127.0.0.1:5000

So you should configure the main web server (apache or nginx) to proxy the requests:

- to .well-known/ into http://127.0.0.1:5000 (for the webfinger)
- to nanoAP/ also into http://127.0.0.1:5000 (for ActivityPub)

