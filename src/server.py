from flask import Flask
from flask import request
from flask import jsonify
from flask import make_response

# app = Flask(__name__)
app = Flask("nanoAP")
users = []
domain = 'uldocs.atilf.fr'

def setup_app(app):
	print("setup app")
	global users
	# All initialization code
	with open("users.txt") as f: lines=f.readlines()
	users = [s.strip() for s in lines]
	print("nusers "+str(len(users)))

@app.route('/nanoAP/users/<nom>/following.json')
def following(nom):
	nom=str(nom)
	s = '{ \
	  "@context": "https://www.w3.org/ns/activitystreams", \
	  "id": "https://uldocs.atilf.fr/nanoAP/users/'+nom+'/following.json", \
	  "summary": "following of '+nom+'", \
	  "type": "OrderedCollection", \
	  "totalItems": 0, \
	  "orderedItems": [] \
	}'
	resp = make_response(s)
	resp.mimetype="application/json"
	return resp

@app.route('/nanoAP/users/<nom>/followers.json')
def followers(nom):
	nom=str(nom)
	s = '{ \
	  "@context": "https://www.w3.org/ns/activitystreams", \
	  "id": "https://uldocs.atilf.fr/nanoAP/users/'+nom+'/followers.json", \
	  "summary": "followers of '+nom+'", \
	  "type": "OrderedCollection", \
	  "totalItems": 0, \
	  "orderedItems": [] \
	}'
	resp = make_response(s)
	resp.mimetype="application/json"
	return resp

@app.route('/nanoAP/users/<nom>/inbox.json')
def inbox(nom):
	nom=str(nom)
	s = '{ \
	  "@context": "https://www.w3.org/ns/activitystreams", \
	  "id": "https://uldocs.atilf.fr/nanoAP/users/'+nom+'/inbox.json", \
	  "summary": "inbox of '+nom+'", \
	  "type": "OrderedCollection", \
	  "totalItems": 0, \
	  "orderedItems": [] \
	}'
	resp = make_response(s)
	resp.mimetype="application/json"
	return resp

@app.route('/nanoAP/users/<nom>/outbox.json')
def outbox(nom):
	nom=str(nom)
	s = '{ \
	  "@context": "https://www.w3.org/ns/activitystreams", \
	  "id": "https://uldocs.atilf.fr/nanoAP/users/'+nom+'/outbox.json", \
	  "summary": "outbox of '+nom+'", \
	  "type": "OrderedCollection", \
	  "totalItems": 0, \
	  "orderedItems": [] \
	}'
	resp = make_response(s)
	resp.mimetype="application/json"
	return resp


@app.route('/nanoAP/users/<nom>')
def handleusers(nom):
	nom=str(nom)
	if nom.endswith('.json'): nom=nom[:-5]
	if not nom in users: return "user unknown"

	s='{ \
	"@context": [ \
		"https://www.w3.org/ns/activitystreams", \
		"https://w3id.org/security/v1" \
	], \
	"id": "https://uldocs.atilf.fr/nanoAP/users/'+nom+'.json", \
	"type": "Person", \
	"preferredUsername": "'+nom+'", \
	"name": "'+nom+'", \
	"inbox": "https://uldocs.atilf.fr/nanoAP/users/'+nom+'/inbox.json", \
	"outbox": "https://uldocs.atilf.fr/nanoAP/users/'+nom+'/outbox.json", \
        "followers": "https://uldocs.atilf.fr/nanoAP/users/'+nom+'/followers.json", \
        "following": "https://uldocs.atilf.fr/nanoAP/users/'+nom+'/following.json", \
        "summary": "<p>OLKi user '+nom+'</p>", \
	"tag": [], \
        "manuallyApprovesFollowers": false, \
        "attachment": [], \
	"publicKey": { \
		"id": "https://uldocs.atilf.fr/nanoAP/users/'+nom+'.json#main-key", \
		"owner": "https://uldocs.atilf.fr/nanoAP/users/'+nom+'.json", \
		"publicKeyPem": "-----BEGIN PUBLIC KEY-----\\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAyQSLIz/yqOifVsQ9JQ72\\nZWqYOF9H4hhFbLqGHq/rqtM3NsKnZrczeRAHmcgFd+SJ9VrJPqNvIi7J5yhqHmYF\\nshNDuoqJMAH4sNpHZtvh/+3FmsvTbYx1lpGwzb4OmaWvaVnuL1O1M4bSIBKY3w4a\\nxGvCVVKmZHVvA0Wx4ixxaWA4lPxaTJ2KBPQgV2nmtHOJZmv4Cx7tFo3s2e1q2LU+\\nrArmxyemsb0ZiBOW/vNJxf43hpl+xjxVBj9soo3MhH83lFTEvi1iv4igIHB4Kjn9\\nnoxKHuwMz+sXZ4qUC4+QKZPcM1cEjicHQFV4AHN+XNIX7xTqSxx2lL+jZ8KOMhXB\\nxwIDAQAB\\n-----END PUBLIC KEY-----\\n" \
	} \
	}'

	print("UUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUU got user request "+nom)
	resp = make_response(s)
	resp.mimetype="application/json"
	return resp
	# request.url for the full URL
	# request.args.get('resource') for argument resource
	# parms = request.query_string
	# user = str(request.url)
	# i = user.find('/nanoAP/users/')
	# user=user[i+14:]

@app.route('/.well-known/<cmd>')
def webfinger(cmd):
    cmd=str(cmd)
    print("inwebfinger "+cmd)
    if cmd.startswith('webfinger'):
	qs = str(request.query_string)
	i=qs.find('acct:')
	if i>=0:
		user=qs[i+5:]+'F'
		for u in users:
			if user.startswith(u):
				user=u
				break
		if user.endswith('F'): return "no such user"
		s='{ \
			"subject": "acct:'+user+'@'+domain+'", \
			"links": [ \
				{ \
					"rel": "self", \
					"type": "application/activity+json", \
					"href": "https://'+domain+'/nanoAP/users/'+user+'.json" \
				} \
			] \
		}'
		resp = make_response(s)
		resp.mimetype="application/json"
		return resp
    elif cmd.find('nodeinfo')>=0:
		s='{ \
		  "version": "0.0", \
		  "software": { \
		    "name": "nanoAP", \
		    "version": "0.0.0" \
		  }, \
		  "protocols": ["activitypub"], \
		  "services": { \
		    "inbound": [], \
		    "outbound": [] \
		  }, \
		  "openRegistrations": false, \
		  "usage": { \
		    "users": { \
		      "total": '+str(len(users))+' \
		    }, \
		    "localPosts": 0, \
		    "localComments": 0 \
		  }, \
		  "metadata": {} \
		}'
		resp = make_response(s)
		resp.mimetype="application/json"
		return resp
    return "unsupported"

# ==============================

setup_app(app)

if __name__ == '__main__':
    app.run()


