from flask import Flask
app = Flask(__name__)

@app.route('/.well-known/webfinger?resource=acct:<user>')
def webfinger(user):
    return "Hello fediverse user "+user


