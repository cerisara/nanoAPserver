# Apache settings

This server creates a Flask (python) mini server that listens on http://127.0.0.1:5000

So you should configure the main web server (apache or nginx) to proxy the requests:

- to .well-known/ into http://127.0.0.1:5000 (for the webfinger)
- to nanoAP/ also into http://127.0.0.1:5000 (for ActivityPub)

This can be done as follows with Apache:

    ProxyPass "/.well-known/" "http://127.0.0.1:5000/.well-known/"
    ProxyPass "/nanoAP/" "http://127.0.0.1:5000/nanoAP/"

to force a JSON response from a mastodon endpoint:
curl -i -H "Accept: application/json"

