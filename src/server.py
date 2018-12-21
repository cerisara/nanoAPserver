from flask import Flask
from flask import request
from flask import jsonify
from flask import make_response
from datetime import datetime, tzinfo, timedelta
from email.utils import formatdate

from Crypto.PublicKey import RSA 
from Crypto.Signature import PKCS1_v1_5 
from Crypto.Hash import SHA256 
from base64 import b64encode, b64decode 

import requests

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
	  "id": "https://'+domain+'/nanoAP/users/'+nom+'/following.json", \
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
	  "id": "https://'+domain+'/nanoAP/users/'+nom+'/followers.json", \
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
	  "id": "https://'+domain+'/nanoAP/users/'+nom+'/inbox.json", \
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
	  "id": "https://'+domain+'/nanoAP/users/'+nom+'/outbox.json", \
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
	"id": "https://'+domain+'/nanoAP/users/'+nom+'.json", \
	"type": "Person", \
	"preferredUsername": "'+nom+'", \
	"name": "'+nom+'", \
	"inbox": "https://'+domain+'/nanoAP/users/'+nom+'/inbox.json", \
	"outbox": "https://'+domain+'/nanoAP/users/'+nom+'/outbox.json", \
        "followers": "https://'+domain+'/nanoAP/users/'+nom+'/followers.json", \
        "following": "https://'+domain+'/nanoAP/users/'+nom+'/following.json", \
        "summary": "<p>OLKi user '+nom+'</p>", \
	"tag": [], \
        "manuallyApprovesFollowers": false, \
        "attachment": [], \
	"publicKey": { \
		"id": "https://'+domain+'/nanoAP/users/'+nom+'.json#main-key", \
		"owner": "https://'+domain+'/nanoAP/users/'+nom+'.json", \
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

class simple_utc(tzinfo):
    def tzname(self,**kwargs):
        return "UTC"
    def utcoffset(self, dt):
        return timedelta(0)

def sign_data(private_key_loc, data):
    '''
    param: private_key_loc Path to your private key
    param: package Data to be signed
    return: base64 encoded signature
    '''
    key = open(private_key_loc, "r").read() 
    rsakey = RSA.importKey(key) 
    signer = PKCS1_v1_5.new(rsakey) 
    digest = SHA256.new() 
    # It's being assumed the data is base64 encoded, so it's decoded before updating the digest 
    # digest.update(b64decode(data)) 
    digest.update(data) 
    sign = signer.sign(digest) 
    return b64encode(sign)

def sendMsg(txt, msgid, sender):
	print("sending msg...")
	tgturl = "mastodon.etalab.gouv.fr"
	tgtbox = "/users/cerisara/inbox"
	dat = datetime.utcnow().replace(tzinfo=simple_utc()).isoformat()
	s = '{ \
		"@context": "https://www.w3.org/ns/activitystreams", \
		"id": "https://'+domain+'/nanoAP/msgs/create-'+msgid+'", \
		"type": "Create", \
		"actor": "https://'+domain+'/nanoAP/users/'+sender+'.json", \
		"object": { \
			"id": "https://'+domain+'/nanoAP/msgs/'+msgid+'", \
			"type": "Note", \
			"published": "'+dat+'", \
			"attributedTo": "https://'+domain+'/nanoAP/users/'+sender+'.json", \
			"inReplyTo": "", \
			"content": "'+txt+'", \
			"to": "https://www.w3.org/ns/activitystreams#Public" \
		} \
	}'
	print("string",s)
	dathtml = formatdate(timeval=None, localtime=False, usegmt=True)
	print("dathtml",dathtml)
	tobesigned = "(request-target): post "+tgtbox+'\\nhost: '+tgturl+'\\ndate: '+dathtml
	print("tobesigned",tobesigned)
	signature = sign_data("private.pem", tobesigned)
	header = 'keyId="https://'+domain+'/nanoAP/users/'+sender+'.json#main-key",headers="(request-target) host date",signature="'+signature+'"'
	headers = {'Host':tgturl, 'Date':dathtml, 'Signature': header}
	print("headers",headers)
	print("posting...")
	r = requests.post("https://"+tgturl+tgtbox, json=s, headers=headers)
	print("post response ",r)

setup_app(app)

if __name__ == '__main__':
    app.run()

